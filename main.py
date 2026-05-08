import streamlit as st

# Configuração da página
st.set_page_config(page_title="Sesmaria do Cerro - Doações", layout="wide")

# Força as colunas a ficarem lado a lado no telemóvel (50% para cada)
st.markdown("""
    <style>
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# AJUDA PARA OS MORADORES (Manual de Instalação)
with st.expander("📲 CLIQUE AQUI PARA COLOCAR O APP NA SUA TELA", expanded=True):
    st.info("""
    Para abrir este sistema sem precisar de link:
    1. No topo do seu celular, clique nos **3 pontinhos** do navegador.
    2. Clique em: **'Adicionar à tela inicial'** ou **'Instalar aplicativo'**.
    3. Confirme em 'Adicionar'.
    """)

st.title("🚜 Sesmaria do Cerro - Sistema de Doações")

# Lista de produtos (20 itens)
produtos_info = {
    "Beterraba": "kg", "Abacaxi": "unid", "Cebola": "kg", "Batata": "kg", 
    "Laranja": "kg", "Maçã": "kg", "Banana": "kg", "Melancia": "unid", 
    "Mamão": "unid", "Cenoura": "kg", "Tomate": "unid", "Alface": "unid", 
    "Repolho": "unid", "Abóbora": "unid", "Pimentão": "unid", "Alho": "kg", 
    "Milho": "unid", "Amendoim": "kg", "Limão": "kg", "Uva": "kg"
}

if 'estoque' not in st.session_state:
    st.session_state.estoque = {produto: 0 for produto in produtos_info.keys()}

imagens = {
    "Beterraba": "https://img.icons8.com/color/144/beet.png",
    "Abacaxi": "https://img.icons8.com/color/144/pineapple.png",
    "Cebola": "https://img.icons8.com/color/144/onion.png",
    "Batata": "https://img.icons8.com/color/144/potato.png",
    "Laranja": "https://img.icons8.com/color/144/orange.png",
    "Maçã": "https://img.icons8.com/color/144/apple.png",
    "Banana": "https://img.icons8.com/color/144/banana.png",
    "Melancia": "https://img.icons8.com/color/144/watermelon.png",
    "Mamão": "https://img.icons8.com/color/144/papaya.png",
    "Cenoura": "https://img.icons8.com/color/144/carrot.png",
    "Tomate": "https://img.icons8.com/color/144/tomato.png",
    "Alface": "https://img.icons8.com/color/144/lettuce.png",
    "Repolho": "https://img.icons8.com/color/144/cabbage.png",
    "Abóbora": "https://img.icons8.com/color/144/pumpkin.png",
    "Pimentão": "https://img.icons8.com/color/144/paprika.png",
    "Alho": "https://img.icons8.com/color/144/garlic.png",
    "Milho": "https://img.icons8.com/color/144/corn.png",
    "Amendoim": "https://img.icons8.com/color/144/peanuts.png",
    "Limão": "https://img.icons8.com/color/144/citrus.png",
    "Uva": "https://img.icons8.com/color/144/grapes.png"
}

st.header("📦 Estoque Atual")
itens = list(st.session_state.estoque.items())

# Criamos as 2 colunas principais (Metade em cada uma)
col1, col2 = st.columns(2)

for i, (item, qtd) in enumerate(itens):
    # Divide os 20 produtos: 10 na primeira, 10 na segunda
    caixa = col1 if i < 10 else col2
    
    unidade = produtos_info[item]
    with caixa:
        st.image(imagens[item], width=50)
        st.write(f"**{item}**")
        st.write(f"{qtd} {unidade}")
        st.write("---")

st.divider()

# Área de Transações
col_doar, col_retirar = st.columns(2)

with col_doar:
    st.subheader("➕ Doação")
    item_doar = st.selectbox("Item:", list(produtos_info.keys()), key="doar")
    qtd_doar = st.number_input(f"Qtd ({produtos_info[item_doar]}):", min_value=0, step=1, key="n_doar")
    if st.button("Confirmar Doação"):
        st.session_state.estoque[item_doar] += qtd_doar
        st.rerun()

with col_retirar:
    st.subheader("➖ Retirada")
    item_retirar = st.selectbox("Item:", list(produtos_info.keys()), key="retirar")
    qtd_retirar = st.number_input(f"Qtd ({produtos_info[item_retirar]}):", min_value=0, step=1, key="n_retirar")
    if st.button("Confirmar Retirada"):
        if st.session_state.estoque[item_retirar] >= qtd_retirar:
            st.session_state.estoque[item_retirar] -= qtd_retirar
            st.rerun()
        else:
            st.error("Sem estoque!")

# Linha final personalizada
st.sidebar.success("🌱 Projeto Sesmaria do Cerro")
