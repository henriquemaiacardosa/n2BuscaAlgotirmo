import os
import logging

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Tenta importar exporters opcionais (OTLP e Prometheus)
try:
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    OTLP_AVAILABLE = True
except ImportError:
    OTLP_AVAILABLE = False

try:
    from opentelemetry.exporter.prometheus import PrometheusMetricReader
    from prometheus_client import start_http_server
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False


def setup_otel(app):
    """
    Inicializa TracerProvider e MeterProvider do OpenTelemetry.
    - Traces: exporta para Jaeger via OTLP gRPC (ou console se não disponível)
    - Métricas: expõe via Prometheus no /metrics (ou console se não disponível)
    """
    resource = Resource.create({
        "service.name": os.getenv("OTEL_SERVICE_NAME", "string-search-explorer"),
        "service.version": "2.0.0",
    })

    # ── Traces ────────────────────────────────────────────────────────────────
    tracer_provider = TracerProvider(resource=resource)

    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "")
    if OTLP_AVAILABLE and otlp_endpoint:
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        app.logger.info(f"[OTEL] Traces → Jaeger em {otlp_endpoint}")
    else:
        # Fallback: imprime spans no console (útil para dev local sem Docker)
        tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
        app.logger.info("[OTEL] Traces → Console (Jaeger não configurado)")

    trace.set_tracer_provider(tracer_provider)

    # ── Métricas ──────────────────────────────────────────────────────────────
    if PROMETHEUS_AVAILABLE:
        reader = PrometheusMetricReader()
        meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
        app.logger.info("[OTEL] Métricas → Prometheus em /metrics")
    else:
        from opentelemetry.sdk.metrics.export import ConsoleMetricExporter
        reader = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=30000)
        meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
        app.logger.info("[OTEL] Métricas → Console (Prometheus não configurado)")

    metrics.set_meter_provider(meter_provider)

    # ── Instrumentação automática do Flask ────────────────────────────────────
    FlaskInstrumentor().instrument_app(app)
    app.logger.info("[OTEL] Flask instrumentado com sucesso")
