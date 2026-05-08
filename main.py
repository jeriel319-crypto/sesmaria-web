import streamlit as st
import json
import os
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Sesmaria do Cerro - Validade", layout="wide")

# Definição de Validade (em dias)
VALIDADE = {
    "Beterraba": 4, "Abacaxi": 4, "Cebola": 4, "Batata": 4, 
    "Laranja": 4, "Maçã": 4, "Banana": 3, "Melancia": 3, 
    "Mamão": 2, "Cenoura": 4, "Tomate": 2, "Alface": 2, 
    "Repolho": 3, "Abóbora": 4, "Pimentão": 2, "Alho": 4, 
    "Milho": 2, "Amendoim": 4, "Limão": 4, "Uva": 2
}

DB_FILE = "estoque_lotes.json"

# --- FUNÇÕES DE LÓGICA ---
def carregar_lotes():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {p: [] for p in VALIDADE.keys()}

def salvar_lotes():
    with open(DB_FILE, "w") as f:
        json.dump(st.session_state.lotes, f)

def limpar_vencidos():
    agora = datetime.now()
    houve_mudanca = False
    novo_estoque = {}
    
    for produto, lotes in st.session_state.lotes.items():
        # Filtra apenas lotes que ainda não venceram
        lotes_validos = []
        for lote in lotes:
            data_entrada = datetime.strptime(lote["timestamp"], "%Y-%m-%d %H:%M:%S")
            prazo = VALIDADE[produto]
            if agora <= data_entrada + timedelta(days=prazo):
                lotes_validos.append(lote)
            else:
                houve_mudanca = True
        novo_estoque[produto] = lotes_validos
    
    if houve_mudanca:
        st.session_state.lotes = novo_estoque
        salvar_lotes()

# --- INICIALIZAÇÃO ---
if 'lotes' not in st.session_state:
    st.session_state.lotes = carregar_lotes()

# Limpa vencidos toda vez que o app roda
limpar_vencidos()

# --- INTERFACE ---
st.title("🚜 Controle de Validade - Sesmaria")

# Resumo visual do estoque
st.header("📦 Estoque (Apenas itens na validade)")
col1, col2 = st.columns(2)

for i, produto in enumerate(VALIDADE.keys()):
    caixa = col1 if i % 2 == 0 else col2
    # Soma a quantidade total de todos os lotes válidos daquele produto
    total_qtd = sum(lote["qtd"] for lote in st.session_state.lotes[produto])
    
    with caixa:
        if total_qtd > 0:
            st.write(f"**{produto}**: {total_qtd} (Vence em {VALIDADE[produto]} dias)")
        else:
            st.write(f"~~{produto}~~ (Sem estoque)")

st.divider()

# --- OPERAÇÕES ---
t_doar, t_retirar = st.tabs(["➕ Adicionar Lote", "➖ Retirar Item"])

with t_doar:
    p_doar = st.selectbox("Produto:", list(VALIDADE.keys()), key="p_doar")
    q_doar = st.number_input("Quantidade:", min_value=1, step=1)
    if st.button("Confirmar Entrada"):
        novo_lote = {
            "qtd": q_doar,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.lotes[p_doar].append(novo_lote)
        salvar_lotes()
        st.success(f"Lote de {p_doar} registrado agora: {novo_lote['timestamp']}")
        st.rerun()

with t_retirar:
    p_ret = st.selectbox("Produto:", list(VALIDADE.keys()), key="p_ret")
    q_ret = st.number_input("Quantidade a retirar:", min_value=1, step=1)
    
    if st.button("Confirmar Retirada"):
        total_disponivel = sum(lote["qtd"] for lote in st.session_state.lotes[p_ret])
        
        if total_disponivel >= q_ret:
            # Lógica PEPS: Retira dos lotes mais antigos primeiro
            restante_para_tirar = q_ret
            lotes_atualizados = []
            
            for lote in st.session_state.lotes[p_ret]:
                if restante_para_tirar <= 0:
                    lotes_atualizados.append(lote)
                elif lote["qtd"] <= restante_para_tirar:
                    restante_para_tirar -= lote["qtd"]
                else:
                    lote["qtd"] -= restante_para_tirar
                    restante_para_tirar = 0
                    lotes_atualizados.append(lote)
            
            st.session_state.lotes[p_ret] = lotes_atualizados
            salvar_lotes()
            st.rerun()
        else:
            st.error("Quantidade insuficiente no estoque válido!")
        
