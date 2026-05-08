import streamlit as st

# Configuração da página
st.set_page_config(page_title="Sesmaria do Cerro - Doações", layout="wide")

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
col1, col2, col3 = st.columns(3)

for i, (item, qtd) in enumerate(itens):
    if i < 7: caixa = col1
    elif i < 14: caixa = col2
    else: caixa = col3
    unidade = produtos_info[item]
    with caixa:
        c_img, c_txt = st.columns([1, 3])
        with c_img: st.image(imagens[item], width=45)
        with c_txt:
            st.write(f"**{item}**")
            st.write(f"{qtd} {unidade}")
        st.write("---")

st.divider()
col_doar, col_retirar = st.columns(2)

with col_doar:
    st.subheader("➕ Registrar Doação")
    item_doar = st.selectbox("Selecione o item:", list(produtos_info.keys()), key="doar")
    unid_d = produtos_info[item_doar]
    qtd_doar = st.number_input(f"Quantidade ({unid_d}):", min_value=0, step=1, key="n_doar")
    if st.button("Confirmar Doação"):
        st.session_state.estoque[item_doar] += qtd_doar
        st.success(f"Adicionado {qtd_doar} {unid_d} de {item_doar}!")
        st.rerun()

with col_retirar:
    st.subheader("➖ Registrar Retirada")
    item_retirar = st.selectbox("Selecione o item:", list(produtos_info.keys()), key="retirar")
    unid_r = produtos_info[item_retirar]
    qtd_retirar = st.number_input(f"Quantidade ({unid_r}):", min_value=0, step=1, key="n_retirar")
    if st.button("Confirmar Retirada"):
        if st.session_state.estoque[item_retirar] >= qtd_retirar:
            st.session_state.estoque[item_retirar] -= qtd_retirar
            st.warning(f"Retirado {qtd_retirar} {unid_r} de {item_retirar}!")
            st.rerun()
        else:
            st.error("Estoque insuficiente!")
            st.sidebar.success("🌱 Projeto Sesmaria do Cerro")
