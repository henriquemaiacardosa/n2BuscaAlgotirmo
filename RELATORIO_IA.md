# Relatório de Uso de Inteligência Artificial

Disciplina: Análise de Algoritmos | Equipe: Henrique Maia Cardosa | Data: 27/05/2026

---

## Instruções de Preenchimento

Para cada uso de IA (ChatGPT, Claude, Copilot, Gemini, etc.), preencha uma entrada
seguindo o modelo abaixo. Seja honesto — o objetivo é demonstrar pensamento crítico
sobre o uso da ferramenta, não esconder que ela foi usada.

---

## Entrada 1

| Campo              | Resposta |
|--------------------|----------|
| **Ferramenta**     | Gemini |
| **Data**           | 15/05/2026 |
| **Tarefa**         | Estruturação da interface e visualização passo a passo no Frontend |

**Prompt utilizado:**
> Preciso de ajuda para criar um frontend com HTML, CSS e JavaScript puro para visualizar algoritmos de busca de strings passo a passo. Como posso estruturar o DOM para atualizar a interface a cada 'SearchStep' que o meu backend Flask me retornar sem recarregar a página?

**Resumo da resposta obtida:**
A IA sugeriu o uso da Fetch API no JavaScript para consumir a rota do Flask de forma assíncrona. Recomendou a criação de um contêiner no HTML onde o texto seria renderizado dinamicamente, dividindo o texto e o padrão em elementos `<span>` para aplicar classes CSS específicas de destaque (match/mismatch) a cada passo da execução.

**O que foi aproveitado:**
- A lógica de iteração assíncrona sobre o array de passos retornado pelo backend.
- A ideia de separar as responsabilidades visuais utilizando classes CSS manipuladas via JavaScript.

**O que foi descartado / adaptado:**
- A IA sugeriu inicialmente a criação de um projeto em React. A sugestão foi descartada para não adicionar complexidade desnecessária ao escopo do trabalho, e o código foi adaptado para Vanilla JS (JavaScript puro) mantendo a leveza do frontend.
---

## Entrada 2

| Campo              | Resposta |
|--------------------|----------|
| **Ferramenta**     | Gemini |
| **Data**           | 22/05/2026 |
| **Tarefa**         | Instrumentação com OpenTelemetry, Docker e integração Prometheus/Grafana |

**Prompt utilizado:**
> Como configuro o OpenTelemetry SDK em uma aplicação Flask para exportar métricas customizadas para o Prometheus e traces para o Jaeger? Preciso entender a arquitetura e construir um docker-compose.yml que orquestre o Flask, Jaeger, Prometheus e Grafana juntos para análise de performance de algoritmos.

**Resumo da resposta obtida:**
Forneceu uma explicação detalhada sobre a diferença entre TracerProvider (para rastreabilidade) e MeterProvider (para métricas). Gerou o código base para o arquivo `otel_setup.py` inicializando o FlaskInstrumentor e criou a estrutura do `docker-compose.yml` mapeando as portas padrão das quatro ferramentas.

**O que foi aproveitado:**
- A estrutura orquestrada do `docker-compose.yml` foi aproveitada quase integralmente.
- O método de abertura de spans customizados (`tracer.start_as_current_span`) e a injeção de atributos (ex: nome do algoritmo) dentro do `app.py`.

**O que foi descartado / adaptado:**
- A IA sugeriu gerar métricas complexas de uso de CPU e memória. Descartei essa abordagem e adaptei a instrumentação para focar estritamente no contexto de Análise de Algoritmos, criando apenas 5 métricas essenciais (como histogramas para contagem de comparações de caracteres e duração em ms).

**Avaliação crítica:**
A IA funcionou perfeitamente como um "tutor" para o ecossistema do OpenTelemetry, cuja documentação oficial é bastante densa. A solução de infraestrutura estava correta, porém exigiu *troubleshooting* manual posterior para resolver conflitos de versões no `requirements.txt` e entender a sintaxe de provisionamento automático de dashboards no Grafana.

---

## Resumo Geral

| Ferramenta | Nº de interações | Principal uso |
|------------|------------------|---------------|
| Gemini     | ~15 interações   | Aprendizado do OpenTelemetry, orquestração de infraestrutura (Docker) e lógica de integração do frontend com a API. |

**Conclusão:** 
O uso da Inteligência Artificial impactou positivamente o desenvolvimento do projeto, atuando como um facilitador técnico em tecnologias que estavam fora do escopo central de programação (como a configuração de redes Docker, Prometheus e Jaeger). Isso permitiu focar o esforço cognitivo na lógica e eficiência dos algoritmos da N1 e na instrumentação assertiva do código na N2, reduzindo o tempo de pesquisa em documentações de ferramentas externas e garantindo a entrega do escopo completo de observabilidade no prazo.
