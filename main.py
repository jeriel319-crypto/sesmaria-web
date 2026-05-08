import streamlit as st

# Configuração da página
st.set_page_config(page_title="Sesmaria do Cerro - Doações", layout="wide")

# Bloco de ajuda para moradores leigos (Aparece logo no topo)
with st.expander("📲 CLIQUE AQUI PARA INSTALAR O APP NO SEU TELEMÓVEL", expanded=True):
    st.info("""
    Para ter este sistema sempre à mão como um Aplicativo:
    1. No Chrome do telemóvel, clique nos **3 pontinhos** no topo direito.
    2. Escolha a opção **'Instalar aplicativo'** ou **'Adicionar ao ecrã principal'**.
    3. Confirme em 'Instalar'. Pronto! O ícone aparecerá junto aos seus outros apps.
    """)

st.title("🚜 Sesmaria do Cerro - Sistema de Doações")
st.write("Gerencie as doações e retiradas de alimentos da região.")

# Lista de produtos confirmada (20 itens)
produtos_info = {
    "Beterraba": "unid", "Abacaxi": "unid", "Cebola": "unid", "Batata": "unid", 
    "Laranja": "unid", "Maçã": "unid", "Banana": "kg", "Melancia": "unid", 
    "Mamão": "unid", "Cenoura": "kg", "Tomate": "unid", "Alface": "unid", 
    "Repolho": "unid", "Abóbora": "unid", "Pimentão": "unid", "Alho": "unid", 
    "Milho": "unid", "Amendoim": "kg", "Limão": "unid", "Uva": "kg"
}

# Inicialização do estoque
if 'estoque' not in st.session_state:
    st.session_state.estoque = {produto: 0 for produto in produtos_info.keys()}

# Imagens estáveis
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
    "Limão": "https://img.icons8.com/color/144/lemon.png",
    "Uva": "https://img.icons8.com/color/144/grapes.png"
}

# Exibição do Estoque
st.header("📦 Estoque Atual")
cols = st.columns(4)
for i, (item, qtd) in enumerate(st.session_state.estoque.items()):
    unidade = produtos_info[item]
    with cols[i % 4]:
        st.image(imagens[item], width=65)
        st.metric(label=item, value=f"{qtd} {unidade}")

st.divider()

# Transações
col1, col2 = st.columns(2)

with col1:
    st.subheader("➕ Registrar Doação")
    item_doar = st.selectbox("Selecione o item:", list(produtos_info.keys()), key="doar")
    unid_d = produtos_info[item_doar]
    qtd_doar = st.number_input(f"Quantidade ({unid_d}):", min_value=0, step=1, key="n_doar")
    if st.button("Confirmar Doação"):
        st.session_state.estoque[item_doar] += qtd_doar
        st.success(f"Adicionado {qtd_doar} {unid_d} de {item_doar}!")
        st.rerun()

with col2:
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

st.sidebar.info("Sistema desenvolvido para o projeto académico de ADS.")
        
