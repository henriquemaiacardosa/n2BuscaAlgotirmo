"""
Definição centralizada de todas as métricas do String Search Explorer.
Importe este módulo em qualquer lugar do projeto para registrar métricas.
"""
from opentelemetry import metrics

meter = metrics.get_meter("string-search-explorer", version="2.0.0")

# ── Contador: total de buscas por algoritmo ───────────────────────────────────
search_counter = meter.create_counter(
    name="search_executions_total",
    description="Total de buscas executadas, separadas por algoritmo",
    unit="1",
)

# ── Histograma: tempo de execução em ms ───────────────────────────────────────
search_duration = meter.create_histogram(
    name="search_duration_ms",
    description="Tempo de execução da busca em milissegundos",
    unit="ms",
)

# ── Histograma: número de comparações de caracteres ───────────────────────────
search_comparisons = meter.create_histogram(
    name="search_comparisons_total",
    description="Número de comparações de caracteres realizadas por execução",
    unit="1",
)

# ── Histograma: tamanho do texto de entrada ───────────────────────────────────
search_text_size = meter.create_histogram(
    name="search_text_size_chars",
    description="Tamanho do texto de entrada em caracteres",
    unit="chars",
)

# ── Contador: ocorrências encontradas ─────────────────────────────────────────
search_occurrences = meter.create_counter(
    name="search_occurrences_total",
    description="Total de ocorrências do padrão encontradas",
    unit="1",
)
