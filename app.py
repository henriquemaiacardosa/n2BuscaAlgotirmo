import os
import json
import logging
import dataclasses

from flask import Flask, request, jsonify, render_template, Response
from werkzeug.utils import secure_filename
from opentelemetry import trace

from algorithms import NaiveSearch, RabinKarpSearch, KMPSearch, BoyerMooreSearch
from otel import (
    setup_otel,
    search_counter,
    search_duration,
    search_comparisons,
    search_text_size,
    search_occurrences,
)

# ── Logging estruturado ───────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger("string-search-explorer")

# ── App Flask ─────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

# ── OpenTelemetry ─────────────────────────────────────────────────────────────
setup_otel(app)
tracer = trace.get_tracer("string-search-explorer.app")

# ── Configuração ──────────────────────────────────────────────────────────────
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MAX_STEPS = 2000

ALGORITHMS = {
    "naive":       NaiveSearch,
    "rabin_karp":  RabinKarpSearch,
    "kmp":         KMPSearch,
    "boyer_moore": BoyerMooreSearch,
}


# ── Utilitários ───────────────────────────────────────────────────────────────
def dataclass_to_dict(obj):
    if dataclasses.is_dataclass(obj):
        return {k: dataclass_to_dict(v) for k, v in dataclasses.asdict(obj).items()}
    elif isinstance(obj, list):
        return [dataclass_to_dict(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    return obj


def run_algorithm(alg_id: str, text: str, pattern: str):
    """
    Executa um algoritmo de busca e registra traces, métricas e logs.
    """
    AlgClass = ALGORITHMS.get(alg_id)
    if not AlgClass:
        return None

    attrs = {
        "algorithm": alg_id,
        "pattern_length": str(len(pattern)),
        "text_length": str(len(text)),
    }

    with tracer.start_as_current_span(f"search.{alg_id}") as span:
        span.set_attribute("algorithm", alg_id)
        span.set_attribute("text.length", len(text))
        span.set_attribute("pattern", pattern)
        span.set_attribute("pattern.length", len(pattern))

        alg = AlgClass()
        result = alg.search(text, pattern)

        span.set_attribute("result.occurrences", len(result.occurrences))
        span.set_attribute("result.comparisons", result.total_comparisons)
        span.set_attribute("result.duration_ms", result.execution_time_ms)

        # ── Métricas ──────────────────────────────────────────────────────────
        search_counter.add(1, attrs)
        search_duration.record(result.execution_time_ms, attrs)
        search_comparisons.record(result.total_comparisons, attrs)
        search_text_size.record(len(text), attrs)
        search_occurrences.add(len(result.occurrences), attrs)

        # ── Log estruturado com trace_id ──────────────────────────────────────
        ctx = span.get_span_context()
        logger.info(
            "search_completed | alg=%s pattern=%r text_len=%d "
            "duration_ms=%.4f comparisons=%d occurrences=%d trace_id=%s",
            alg_id, pattern, len(text),
            result.execution_time_ms, result.total_comparisons,
            len(result.occurrences),
            format(ctx.trace_id, "032x") if ctx.is_valid else "none",
        )

        result_dict = dataclass_to_dict(result)
        if len(result_dict["steps"]) > MAX_STEPS:
            result_dict["steps"] = result_dict["steps"][:MAX_STEPS]
            result_dict["steps_truncated"] = True

        return result_dict


# ── Rotas ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/algorithms", methods=["GET"])
def list_algorithms():
    return jsonify([
        {"id": "naive",       "name": "Naive (Brute Force)"},
        {"id": "rabin_karp",  "name": "Rabin-Karp"},
        {"id": "kmp",         "name": "Knuth-Morris-Pratt (KMP)"},
        {"id": "boyer_moore", "name": "Boyer-Moore"},
    ])


@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "files" not in request.files:
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist("files")
    uploaded = []

    for file in files:
        if file.filename == "":
            continue
        if file and file.filename.endswith(".txt"):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            uploaded.append({"filename": filename, "content": content, "size": len(content)})
            logger.info("file_uploaded | filename=%s size=%d", filename, len(content))

    if not uploaded:
        return jsonify({"error": "No valid .txt files uploaded"}), 400

    return jsonify({"files": uploaded})


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    text         = data.get("text", "")
    pattern      = data.get("pattern", "")
    algorithm_id = data.get("algorithm", "naive")
    all_algs     = data.get("all_algorithms", False)

    if not text or not pattern:
        return jsonify({"error": "Text and pattern are required"}), 400

    if len(text) > 500_000:
        return jsonify({"error": "Text too large (max 500,000 characters)"}), 400

    with tracer.start_as_current_span("api.search") as span:
        span.set_attribute("request.all_algorithms", all_algs)
        span.set_attribute("request.algorithm", algorithm_id)

        if all_algs:
            results = {}
            for alg_id in ALGORITHMS:
                results[alg_id] = run_algorithm(alg_id, text, pattern)
            return jsonify({"results": results, "mode": "compare"})
        else:
            result = run_algorithm(algorithm_id, text, pattern)
            if result is None:
                return jsonify({"error": f"Unknown algorithm: {algorithm_id}"}), 400
            return jsonify({"result": result, "mode": "single"})


@app.route("/metrics")
def metrics_endpoint():
    """Endpoint para o Prometheus coletar métricas."""
    try:
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    except ImportError:
        return jsonify({"error": "prometheus_client not installed"}), 501


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "string-search-explorer"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
