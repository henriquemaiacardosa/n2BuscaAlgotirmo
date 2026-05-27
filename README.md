# String Search Explorer — N2

Aplicação web para explorar, visualizar e comparar algoritmos de busca de strings,
com **observabilidade completa via OpenTelemetry** (traces, métricas e logs).

## Algoritmos

| Algoritmo    | Melhor  | Médio   | Pior    |
|--------------|---------|---------|---------|
| Naive        | O(n)    | O(n·m)  | O(n·m)  |
| Rabin-Karp   | O(n+m)  | O(n+m)  | O(n·m)  |
| KMP          | O(n)    | O(n+m)  | O(n+m)  |
| Boyer-Moore  | O(n/m)  | O(n/m)  | O(n·m)  |

## Stack de Observabilidade

| Ferramenta    | Função               | URL local               |
|---------------|----------------------|-------------------------|
| OpenTelemetry | SDK de instrumentação| —                       |
| Jaeger        | Visualização traces  | http://localhost:16686  |
| Prometheus    | Coleta de métricas   | http://localhost:9090   |
| Grafana       | Dashboard            | http://localhost:3000   |

## Como Rodar (Docker — recomendado)

```bash
docker compose up --build
# App:      http://localhost:5000
# Jaeger:   http://localhost:16686
# Grafana:  http://localhost:3000  (admin/admin)
```

## Como Rodar (local sem Docker)

```bash
pip install -r requirements.txt
python app.py
# Traces saem no console, métricas em http://localhost:5000/metrics
```

## Benchmark com Dados Reais

```bash
python benchmarks/run_benchmark.py
python benchmarks/run_benchmark.py benchmarks/texts/war_and_peace.txt
```

## Estrutura

```
string-search-explorer/
├── app.py                    # Flask + instrumentação OTEL
├── Dockerfile
├── docker-compose.yml
├── prometheus.yml
├── otel/
│   ├── otel_setup.py         # TracerProvider + MeterProvider
│   └── metrics.py            # Counters e histogramas
├── algorithms/               # Padrão Strategy — sem alteração da N1
├── benchmarks/
│   ├── run_benchmark.py
│   └── texts/
└── grafana/provisioning/     # Dashboard provisionado automaticamente
```

## Métricas Expostas

| Métrica                     | Tipo      | Descrição                   |
|-----------------------------|-----------|-----------------------------|
| search_executions_total     | Counter   | Buscas por algoritmo        |
| search_duration_ms          | Histogram | Tempo de execução (ms)      |
| search_comparisons_total    | Histogram | Comparações de caracteres   |
| search_text_size_chars      | Histogram | Tamanho do texto            |
| search_occurrences_total    | Counter   | Ocorrências encontradas     |
