# Textos para Benchmark

Coloque aqui arquivos `.txt` para usar nos benchmarks.

## Textos recomendados (domínio público)

| Arquivo              | Link de download                                      | Tamanho |
|----------------------|-------------------------------------------------------|---------|
| `war_and_peace.txt`  | https://www.gutenberg.org/ebooks/2600                 | ~3.2 MB |
| `dom_casmurro.txt`   | https://www.gutenberg.org/ebooks/55752                | ~460 KB |
| `bible.txt`          | https://www.gutenberg.org/ebooks/10                   | ~4.0 MB |
| `sherlock.txt`       | https://www.gutenberg.org/ebooks/1661                 | ~580 KB |

## Como baixar

No terminal:
```bash
curl -o texts/war_and_peace.txt https://www.gutenberg.org/files/2600/2600-0.txt
curl -o texts/dom_casmurro.txt  https://www.gutenberg.org/files/55752/55752-0.txt
```

## Como rodar o benchmark

```bash
# Com texto embutido (sem precisar baixar nada)
python benchmarks/run_benchmark.py

# Com arquivo real
python benchmarks/run_benchmark.py benchmarks/texts/war_and_peace.txt

# Com padrões personalizados
python benchmarks/run_benchmark.py benchmarks/texts/war_and_peace.txt --patterns "the" "Napoleon" "NOTFOUND"
```
