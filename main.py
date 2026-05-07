import streamlit as st

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Sesmaria do Cerro", page_icon="🍎")

# PRODUTOS E ÍCONES
PRODUTOS_DADOS = {
    "Abacaxi": "🍍", "Abóbora": "🎃", "Alho": "🧄", "Amendoim": "🥜",
    "Batata": "🥔", "Bergamota": "🍊", "Beterraba": "🥗", "Brócolis": "🥦", 
    "Cebola": "🧅", "Couve-flor": "🥬", "Goiaba": "🍈", "Laranja": "🍊", 
    "Mel": "🍯", "Melancia": "🍉", "Milho": "🌽", "Pão": "🍞",
    "Pepino": "🥒", "Tomate": "🍅", "Uva": "🍇"
}

# Inicializar estoque
if 'estoque' not in st.session_state:
    st.session_state.estoque = {p: 0 for p in PRODUTOS_DADOS.keys()}

st.title("🍎 Sesmaria do Cerro")
st.subheader("Sistema de Doação Comunitária")

# EXIBIÇÃO DO ESTOQUE
st.write("### 🛒 Estoque Atual")
cols = st.columns(3)
for i, (nome, icone) in enumerate(PRODUTOS_DADOS.items()):
    qtd = st.session_state.estoque[nome]
    with cols[i % 3]:
        st.metric(label=f"{i+1}. {icone} {nome}", value=f"{qtd}")

st.divider()

# BOTÕES DE AÇÃO
aba1, aba2 = st.tabs(["🧺 RETIRAR", "➕ DOAR"])

with aba1:
    num_r = st.number_input("Número do produto (Retirar):", min_value=1, max_value=19, step=1, key="n_ret")
    qtd_r = st.number_input("Quantidade para retirar:", min_value=1, step=1, key="q_ret")
    if st.button("Confirmar Retirada", key="btn_ret"):
        nome_p = list(PRODUTOS_DADOS.keys())[num_r-1]
        if st.session_state.estoque[nome_p] >= qtd_r:
            st.session_state.estoque[nome_p] -= qtd_r
            st.success(f"Retirada de {nome_p} realizada!")
            st.rerun()
        else:
            st.error("Estoque insuficiente!")

with aba2:
    num_d = st.number_input("Número do produto (Doar):", min_value=1, max_value=19, step=1, key="n_doa")
    qtd_d = st.number_input("Quantidade para doar:", min_value=1, step=1, key="q_doa")
    if st.button("Confirmar Doação", key="btn_doa"):
        nome_p = list(PRODUTOS_DADOS.keys())[num_d-1]
        st.session_state.estoque[nome_p] += qtd_d
        st.success(f"Obrigado! {nome_p} adicionado.")
        st.rerun()
      
