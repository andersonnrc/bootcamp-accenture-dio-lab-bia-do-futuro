import streamlit as st
import pandas as pd
import json
import os
from dotenv import load_dotenv
from groq import Groq

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E VARIÁVEIS DE ESTADO
# ---------------------------------------------------------
st.set_page_config(page_title="MetaFlow - GPS Financeiro", page_icon="🧭", layout="centered")

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o estado para guardar o histórico oculto e a interação atual visível
if "messages_history" not in st.session_state:
    st.session_state.messages_history = []
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "current_a" not in st.session_state:
    st.session_state.current_a = None

# Inicializa o cliente Groq (Exige a variável de ambiente GROQ_API_KEY)
# Recomendo usar a biblioteca python-dotenv para carregar o .env localmente
client = Groq(api_key=os.environ.get("KEY_API_CURSO_DIO"))

# ---------------------------------------------------------
# 2. ORQUESTRAÇÃO DE DADOS (PANDAS + JSON)
# ---------------------------------------------------------
@st.cache_data
def load_financial_context():
    """
    Simula o processo de ETL: Lê os arquivos, processa as métricas 
    e retorna uma string estruturada para o System Prompt.
    """
    try:
        # Tenta carregar os dados reais da pasta data/
        df_transacoes = pd.read_csv("data/transacoes.csv")
        
        with open("data/perfil_investidor.json", "r", encoding="utf-8") as f:
            perfil = json.load(f)
            
        with open("data/produtos_financeiros.json", "r", encoding="utf-8") as f:
            produtos = json.load(f)

        # Exemplo de processamento Pandas: agrupamento de gastos
        # df_transacoes['valor'] = pd.to_numeric(df_transacoes['valor'])
        # gastos_por_categoria = df_transacoes.groupby('categoria')['valor'].sum().to_dict()
        
        # Para este protótipo, vamos montar o texto consolidado
        contexto = f"""
        [CONTEXTO FINANCEIRO DO USUÁRIO]
        - Nome: Anderson
        - Perfil de Risco: {perfil.get('perfil', 'Moderado')}
        - Capacidade de Poupança Atual: R$ 850,00/mês
        
        [CATÁLOGO DE PRODUTOS PERMITIDOS]
        {json.dumps(produtos, indent=2, ensure_ascii=False)}
        """
        return contexto

    except Exception as e:
        # Fallback caso os arquivos ainda não existam no caminho correto
        return f"""
        [CONTEXTO FINANCEIRO DO USUÁRIO]
        - Nome: Anderson
        - Perfil de Risco: Moderado
        - Capacidade de Poupança Atual: R$ 850,00/mês
        - Mês de Referência: Abril/2026
        
        [CATÁLOGO DE PRODUTOS PERMITIDOS]
        1. Tesouro Selic (Baixo Risco)
        2. CDB 110% CDI (Baixo Risco)
        3. Fundo Multimercado Alpha (Médio Risco)
        """

# ---------------------------------------------------------
# 3. CONFIGURAÇÃO DO PROMPT
# ---------------------------------------------------------
financial_context = load_financial_context()

system_prompt = f"""
Você é o MetaFlow, um agente financeiro inteligente especializado em planejamento de metas.
Seu tom é profissional, encorajador e direto. Não use formatação matemática complexa.

{financial_context}

REGRAS:
1. Baseie-se apenas no contexto acima.
2. Não realize cálculos complexos de juros compostos, apenas utilize a capacidade de poupança informada para estimar prazos simples.
3. Recomende apenas os produtos listados.
4. Se o usuário perguntar sobre investimentos externos (como ações e cripto), redirecione para o foco do planejamento.
"""

# Injeta o system prompt inicial no histórico oculto se estiver vazio
if not st.session_state.messages_history:
    st.session_state.messages_history.append({"role": "system", "content": system_prompt})

# ---------------------------------------------------------
# 4. INTERFACE DE USUÁRIO (FRONTEND ENXUTO)
# ---------------------------------------------------------
st.title("🧭 MetaFlow - Seu GPS Financeiro")
st.markdown("Bem-vindo! Qual é o nosso objetivo financeiro de hoje?")

# Captura a entrada do usuário
user_input = st.chat_input("Digite sua pergunta ou meta...")

if user_input:
    # 1. Atualiza as variáveis de estado com a nova pergunta
    st.session_state.current_q = user_input
    
    # 2. Adiciona a pergunta ao histórico oculto (para a IA ter contexto)
    st.session_state.messages_history.append({"role": "user", "content": user_input})
    
    # 3. Chama a API do Groq usando o modelo definido
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages_history,
            temperature=0.3, # Temperatura baixa para respostas mais exatas e menos criativas
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        
        # 4. Salva a resposta atual e atualiza o histórico oculto
        st.session_state.current_a = answer
        st.session_state.messages_history.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.session_state.current_a = f"Erro ao conectar com o motor de inteligência: {e}"

# ---------------------------------------------------------
# 5. RENDERIZAÇÃO CONDICIONAL (Apenas a interação atual)
# ---------------------------------------------------------
if st.session_state.current_q:
    with st.chat_message("user"):
        st.write(st.session_state.current_q)
        
    with st.chat_message("assistant"):
        st.write(st.session_state.current_a)