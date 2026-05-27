"""
Benchmark dos algoritmos de busca de strings com arquivos reais.

Uso:
    python run_benchmark.py                          # usa texto de exemplo embutido
    python run_benchmark.py texts/war_and_peace.txt  # usa arquivo externo
    python run_benchmark.py texts/war_and_peace.txt --output resultados.csv

Saída:
    - Tabela no terminal
    - Arquivo CSV com todos os resultados
"""
import sys
import csv
import time
import pathlib
import argparse

# Adiciona o diretório pai ao path para importar os algoritmos
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from algorithms import NaiveSearch, RabinKarpSearch, KMPSearch, BoyerMooreSearch

ALGORITHMS = {
    "naive":       NaiveSearch,
    "kmp":         KMPSearch,
    "rabin_karp":  RabinKarpSearch,
    "boyer_moore": BoyerMooreSearch,
}

# Padrões variados: curto, médio, longo, não encontrado
DEFAULT_PATTERNS = [
    "the",           # muito curto, alta frequência
    "and",           # muito curto, alta frequência
    "algorithm",     # médio
    "string search", # com espaço
    "XYZNOTFOUND",   # não existe no texto (pior caso)
]

# Texto de exemplo embutido (caso nenhum arquivo seja fornecido)
SAMPLE_TEXT = """
It was the best of times, it was the worst of times, it was the age of wisdom,
it was the age of foolishness, it was the epoch of belief, it was the epoch of
incredulity, it was the season of Light, it was the season of Darkness, it was
the spring of hope, it was the winter of despair, we had everything before us,
we had nothing before us, we were all going direct to Heaven, we were all going
direct the other way. The quick brown fox jumps over the lazy dog. String search
algorithms are fundamental to computer science. The naive algorithm is simple but
slow. The KMP algorithm uses a failure function. Boyer-Moore uses bad character
heuristic. Rabin-Karp uses rolling hash for string search and pattern matching.
""" * 500  # repete para ter um texto razoável


def format_number(n):
    return f"{n:,}".replace(",", ".")


def run_benchmark(text: str, patterns: list, output_csv: str = "benchmark_results.csv"):
    print(f"\n{'='*70}")
    print(f"  STRING SEARCH BENCHMARK")
    print(f"{'='*70}")
    print(f"  Tamanho do texto : {format_number(len(text))} caracteres")
    print(f"  Padrões testados : {len(patterns)}")
    print(f"  Algoritmos       : {', '.join(ALGORITHMS.keys())}")
    print(f"{'='*70}\n")

    rows = []
    header = f"{'Algoritmo':<15} {'Padrão':<18} {'Ocorr.':>7} {'Compar.':>12} {'Tempo (ms)':>12}"
    separator = "-" * len(header)

    for pattern in patterns:
        print(f"Padrão: {pattern!r}")
        print(separator)
        print(header)
        print(separator)

        for alg_id, AlgClass in ALGORITHMS.items():
            alg = AlgClass()
            result = alg.search(text, pattern)

            row = {
                "algorithm":    alg_id,
                "pattern":      pattern,
                "text_size":    len(text),
                "occurrences":  len(result.occurrences),
                "comparisons":  result.total_comparisons,
                "duration_ms":  result.execution_time_ms,
            }
            rows.append(row)

            print(
                f"  {alg_id:<13} {pattern!r:<18} "
                f"{format_number(len(result.occurrences)):>7} "
                f"{format_number(result.total_comparisons):>12} "
                f"{result.execution_time_ms:>11.4f}ms"
            )

        print()

    # ── Salva CSV ─────────────────────────────────────────────────────────────
    output_path = pathlib.Path(__file__).parent / output_csv
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n{'='*70}")
    print(f"  Resultados salvos em: {output_path}")
    print(f"{'='*70}\n")

    # ── Resumo: melhor algoritmo por padrão ───────────────────────────────────
    print("RESUMO — Mais rápido por padrão:")
    print(separator)
    for pattern in patterns:
        pattern_rows = [r for r in rows if r["pattern"] == pattern]
        fastest = min(pattern_rows, key=lambda r: r["duration_ms"])
        fewest = min(pattern_rows, key=lambda r: r["comparisons"])
        print(
            f"  Padrão {pattern!r:<18} "
            f"→ mais rápido: {fastest['algorithm']:<12} ({fastest['duration_ms']:.4f}ms) "
            f"| menos comparações: {fewest['algorithm']}"
        )

    return rows


def main():
    parser = argparse.ArgumentParser(description="Benchmark de algoritmos de busca de strings")
    parser.add_argument("text_file", nargs="?", help="Arquivo .txt para usar como texto de busca")
    parser.add_argument("--output", default="benchmark_results.csv", help="Nome do arquivo CSV de saída")
    parser.add_argument("--patterns", nargs="+", default=DEFAULT_PATTERNS, help="Padrões para buscar")
    args = parser.parse_args()

    if args.text_file:
        text_path = pathlib.Path(args.text_file)
        if not text_path.exists():
            print(f"Erro: arquivo '{text_path}' não encontrado.")
            print("Dica: baixe um livro do Projeto Gutenberg em https://www.gutenberg.org")
            sys.exit(1)
        text = text_path.read_text(encoding="utf-8", errors="ignore")
        print(f"Texto carregado: {text_path.name}")
    else:
        text = SAMPLE_TEXT
        print("Usando texto de exemplo embutido (passe um arquivo .txt como argumento para usar texto real)")

    run_benchmark(text, args.patterns, args.output)


if __name__ == "__main__":
    main()
