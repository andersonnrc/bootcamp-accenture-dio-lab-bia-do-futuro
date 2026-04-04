# Base de Conhecimento

## Dados Utilizados

O agente utiliza exclusivamente os dados fornecidos na pasta `data` do repositório para garantir precisão e evitar alucinações. Cada arquivo possui um papel específico na construção do contexto financeiro:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Recuperar o histórico de dúvidas do cliente para adaptar a complexidade das respostas (ex: se o cliente já perguntou sobre liquidez, o agente usa termos mais técnicos). |
| `perfil_investidor.json` | JSON | Definir a tolerância ao risco do usuário (Conservador, Moderado, Arrojado) para balizar a escolha dos ativos para as metas. |
| `produtos_financeiros.json` | JSON | Atuar como o "catálogo fechado" de investimentos. O agente só pode recomendar ativos que existam neste documento. |
| `transacoes.csv` | CSV | Fornecer a base bruta para o cálculo de capacidade de poupança, média de gastos por categoria e identificação de gargalos no orçamento. |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os arquivos brutos em si (CSV e JSON) não foram alterados ou expandidos fisicamente. No entanto, durante o tempo de execução (runtime), os dados de `transacoes.csv` sofrem transformações via Pandas (um processo de ETL em memória). O script agrupa as transações por categoria, soma entradas/saídas e calcula a "capacidade de poupança mensal". O modelo de linguagem consome apenas essas métricas consolidadas, e não as linhas brutas, otimizando o uso de tokens e prevenindo erros matemáticos.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos são lidos localmente pelo backend em Python utilizando as bibliotecas `pandas` e `json+` no exato momento em que o aplicativo (Streamlit) é iniciado. Para garantir performance, o carregamento dos arquivos é armazenado em cache (utilizando recursos como @st.cache_data), evitando leituras repetidas no disco a cada nova mensagem do chat.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são injetados dinamicamente no System Prompt, mas nunca em seu estado bruto. A camada de orquestração em Python converte os DataFrames processados em uma string estruturada (um resumo financeiro). Sempre que o usuário envia uma nova mensagem, o orquestrador atualiza esse "bloco de contexto" no prompt do sistema enviado para a API do `Groq`, garantindo que o LLM (Llama 3.1) tenha a fotografia financeira atualizada antes de formular a resposta.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
[CONTEXTO FINANCEIRO DO USUÁRIO]
- Nome: Anderson
- Perfil de Risco: Moderado
- Capacidade de Poupança Atual: R$ 850,00/mês
- Mês de Referência: Abril/2026

[RESUMO DE GASTOS DO ÚLTIMO MÊS]
- Habitação: R$ 1.500,00
- Alimentação: R$ 900,00
- Lazer & Assinaturas: R$ 450,00 (Alerta: 15% acima da média histórica)

[CATÁLOGO DE PRODUTOS PERMITIDOS (PERFIL MODERADO)]
1. CDB Banco XYZ (Liquidez Diária) - 100% CDI
2. Tesouro IPCA+ 2029 - Inflação + 5.5%
3. Fundo Multimercado Alpha - Risco Médio

[REGRA ESTRITA]: Baseie seu planejamento de metas EXCLUSIVAMENTE nos números acima. Não realize cálculos de juros compostos por conta própria.
...
```
