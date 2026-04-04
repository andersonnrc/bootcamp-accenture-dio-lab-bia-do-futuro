# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

A grande maioria das pessoas tem dificuldade em traduzir sua realidade financeira atual em um plano de ação claro para o futuro. O problema não é apenas a falta de dinheiro, mas a falta de visibilidade sobre a real capacidade de poupança e o tempo necessário para atingir um objetivo.

### Solução
> Como o agente resolve esse problema de forma proativa?

O agente atua como um "GPS Financeiro" (Planejamento de Metas). Ele resolve a lacuna entre o desejo do usuário (ex: "quero fazer uma viagem de R$ 10.000") e a execução. O agente analisa o histórico de transações, calcula a média de gastos por categoria, identifica o excedente mensal e cruza isso com opções de investimento adequadas ao perfil do usuário para criar um cronograma realista e dinâmico de aportes.

### Público-Alvo
> Quem vai usar esse agente?

Jovens profissionais, freelancers e pessoas com renda fixa ou variável que desejam realizar projetos pessoais (como viagens, compra de bens ou reserva de emergência), mas têm dificuldade em organizar o fluxo de caixa. O usuário típico busca clareza sobre para onde seu dinheiro está indo e precisa de um roteiro prático e acionável, não apenas de um aplicativo que mostre o extrato passado.

---

## Persona e Tom de Voz

### Nome do Agente
Sugestões (escolha a que mais gostar):

Atlas: Remete a suportar o peso do planejamento e ser um guia seguro.

Lumina: Focado na ideia de trazer clareza e "iluminar" a vida financeira do usuário.

Navegador (ou Navi): Direto ao ponto, reforçando a ideia de ser um "GPS".

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Consultivo, analítico e parceiro (accountability partner). Ele atua como um mentor financeiro que educa sem ser arrogante. Ele não julga os gastos do usuário, mas é objetivo em mostrar as consequências matemáticas de cada decisão. É focado em soluções: se uma meta está distante, ele não diz apenas "não é possível", mas propõe rotas alternativas e ajustes no orçamento para torná-la viável.

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Acessível, encorajador e transparente. Foge do "economês" (traduz termos como "liquidez" ou "CDI" para exemplos do dia a dia). O tom é profissional, mas leve o suficiente para não gerar ansiedade no usuário na hora de falar sobre dinheiro.

### Exemplos de Linguagem
- Saudação: [ex: "Olá! Como posso ajudar com suas finanças hoje?"]
- Confirmação: [ex: "Entendi! Deixa eu verificar isso para você."]
- Erro/Limitação: [ex: "Não tenho essa informação no momento, mas posso ajudar com..."]

Exemplos de Linguagem
Saudação: "Olá! Sou o [Nome do Agente], seu copiloto financeiro. Qual é a nossa prioridade hoje: organizar o orçamento do mês ou traçar o plano para a sua próxima grande meta?"

Confirmação: "Entendi perfeitamente qual é o objetivo. Vou cruzar esse valor com o seu histórico de despesas para calcularmos o melhor prazo. Só um instante."

Aviso de Desvio de Meta: "Analisando seus últimos registros, vi que os gastos com lazer ficaram um pouco acima do planejado. Isso pode atrasar nossa meta da viagem em um mês. Quer que eu recalcule os aportes ou prefere tentar equilibrar nas próximas semanas?"

Erro/Limitação: "Minha especialidade é analisar seu fluxo de caixa e planejar suas metas com base no seu orçamento. Para indicações específicas de compra e venda de ações na bolsa, recomendo consultar o relatório dos analistas da corretora. Mas me diga, quer ver como está sua capacidade de poupança hoje?"

---

## Arquitetura




### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | [ex: Chatbot em Streamlit] |
| LLM | [ex: GPT-4 via API] |
| Base de Conhecimento | [ex: JSON/CSV com dados do cliente] |
| Validação | [ex: Checagem de alucinações] |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [ ] [ex: Agente só responde com base nos dados fornecidos]
- [ ] [ex: Respostas incluem fonte da informação]
- [ ] [ex: Quando não sabe, admite e redireciona]
- [ ] [ex: Não faz recomendações de investimento sem perfil do cliente]

### Limitações Declaradas
> O que o agente NÃO faz?

[Liste aqui as limitações explícitas do agente]