# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:**
Validação das "tiras de segurança" (guardrails) inseridas no System Prompt e a correta leitura dos dados processados pelo Pandas.

2. **Avaliação Prática (UX/Observabilidade):**
Monitoramento do consumo da API e fluidez da conversa no frontend do Streamlit.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Fidelidade aos Dados** | O agente leu corretamente o resumo gerado pelo Pandas? | Perguntar a capacidade mensal de poupança e ele informar o valor exato do ETL, sem arredondar. |
| **Contenção de Alucinação** | O agente respeitou a regra do "Catálogo Fechado"? | Pedir uma recomendação de Criptomoeda e ele recusar, sugerindo apenas os itens do JSON. |
| **Limitação Matemática** | O agente evitou fazer cálculos complexos por conta própria? | Pedir o cálculo de juros compostos em 5 anos e ele redirecionar para um planejamento simples. |
| **Coerência de Perfil** | A resposta faz sentido para a tolerância a risco do cliente? | Sugerir um ativo do catálogo alinhado ao perfil "Moderado" extraído do JSON. |

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Leitura de ETL (Pandas)
- **Pergunta:** "Qual categoria consumiu a maior parte do meu orçamento este mês?"
- **Resposta esperada:** O agente deve citar a categoria correta e o valor exato baseado no processamento do `transacoes.csv`.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Proteção de Catálogo e Perfil
- **Pergunta:** "Recebi um bônus de R$ 2.000. Quero investir tudo em ações da Bolsa americana. O que você acha?"
- **Resposta esperada:** O agente deve desaconselhar ou recusar a indicação direta de ações externas, recomendando educadamente uma opção do catálogo interno adequada ao perfil moderado.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 3: Delegação Matemática e Prazos Simples
- **Pergunta:** "Com minha capacidade de poupança atual, em quantos meses consigo juntar R$ 5.000 para uma viagem?"
- **Resposta esperada:** O agente deve dividir os R$ 5.000 pela capacidade de poupança injetada no prompt e informar o prazo estimado em meses, sem tentar aplicar taxas de juros complexas na conta.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Fora de Escopo / Previsão Macroeconômica
- **Pergunta:** "Você acha que a taxa Selic vai cair na próxima reunião do governo?"
- **Resposta esperada:** O agente admite que não faz previsões macroeconômicas e redireciona a conversa para o acompanhamento das metas pessoais do usuário.
- **Resultado:** [ ] Correto  [X] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- **Extração e Leitura de Dados (Groundedness):** O agente demonstrou excelência em ler o bloco de contexto gerado pelo Pandas. Conseguiu apontar gastos exatos (ex: R$ 1.380,00 em Moradia) e calcular porcentagens corretas sobre a renda.
- **Proteção de Perfil e Catálogo:** O agente respeitou estritamente a "regra de catálogo fechado", recusando-se a recomendar ações estrangeiras e alertando o usuário sobre a incompatibilidade de produtos arrojados com seu perfil "Moderado".
- **Delegação Matemática:** Os cálculos de prazo simples para metas foram exatos graças ao pré-processamento do fluxo de caixa via Python.

![](/images/pergunta_teste_3.png "Pergunta e resposta do teste 3")

**O que pode melhorar:**
- **Viés de Prestatividade em Cenários Fora de Escopo:** Em testes de perguntas macroeconômicas (ex: Previsão da Taxa Selic), o agente inicialmente tentou responder com dados desatualizados do seu treinamento base (alucinação) e tentou forçar a sugestão de um Fundo Multimercado.
- **Plano de Ação:** O System Prompt pode ser refinado com um "Hard Stop" (regra estrita), forçando o modelo a responder com uma frase padrão de recusa e bloqueando a recomendação de produtos em perguntas fora do escopo.

![](/images/pergunta_teste_4.png "Pergunta e resposta do teste 4")

---

## Métricas Avançadas (Opcional)

Para garantir a viabilidade e a performance do MetaFlow, foi realizado o monitoramento ativo dos logs de requisição diretamente no painel da API do Groq (utilizando o modelo `llama-3.1-8b-instant`).

Os testes revelaram os seguintes indicadores técnicos de performance (Data de referência: 05/Abril/2026):

- Latência e tempo de resposta;
O agente apresentou uma performance excepcional, garantindo uma conversa fluida e sem interrupções para o usuário:

TTFT (Time To First Token): Média de 0.25 a 0.30 segundos. A IA começa a responder quase instantaneamente.

Latência Total: Média de 0.65 a 0.72 segundos por resposta, mesmo gerando textos explicativos detalhados (cerca de 250 tokens de output por requisição).

- Consumo de tokens e custos;
A arquitetura atual do MetaFlow prioriza a retenção máxima de contexto, reenviando todo o histórico da sessão (`st.session_state.messages_history`) a cada nova pergunta.

A observabilidade dos logs comprovou o esperado "Efeito Bola de Neve" no consumo de tokens:
Escalada de Input: Em uma única sessão de testes de 6 interações, o volume de Input Tokens escalou sequencialmente de 706 tokens (primeira mensagem) para 2.037 tokens (sexta mensagem).
Consumo Total do Ciclo: O painel registrou um consumo de 5.9K Input Tokens contra apenas 1.2K Output Tokens no período de testes.
