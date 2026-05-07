import streamlit as st

# Configuração da página
st.set_page_config(page_title="Sesmaria do Cerro - Doações", layout="wide")

st.title("🚜 Sesmaria do Cerro - Sistema de Doações")
st.write("Gerencie as doações e retiradas de alimentos da região.")

# Lista de produtos regionalizada
produtos_info = {
    "Beterraba": "kg", "Abacaxi": "unid", "Cebola": "kg", "Batata": "kg", 
    "Mandioca": "kg", "Chuchu": "unid", "Maracujá": "unid", "Laranja": "kg", 
    "Maçã": "kg", "Banana": "kg", "Melancia": "unid", "Mamão": "unid", 
    "Cenoura": "kg", "Tomate": "unid", "Alface": "unid", "Repolho": "unid", 
    "Abóbora": "unid", "Pimentão": "unid", "Alho": "kg", "Milho": "unid", 
    "Feijão": "kg", "Amendoim": "kg"
}

# Inicialização do estoque
if 'estoque' not in st.session_state:
    st.session_state.estoque = {produto: 0 for produto in produtos_info.keys()}

# Dicionário de imagens - Links substituídos por fontes mais estáveis
imagens = {
    "Beterraba": "https://cdn-icons-png.flaticon.com/512/2909/2909841.png",
    "Abacaxi": "https://cdn-icons-png.flaticon.com/512/2153/2153711.png",
    "Cebola": "https://cdn-icons-png.flaticon.com/512/2316/2316629.png",
    "Batata": "https://cdn-icons-png.flaticon.com/512/1135/1135544.png",
    "Mandioca": "https://cdn-icons-png.flaticon.com/512/6122/6122558.png", # Link reforçado
    "Chuchu": "https://cdn-icons-png.flaticon.com/512/10046/10046903.png",
    "Maracujá": "https://cdn-icons-png.flaticon.com/512/13601/13601614.png", # Link reforçado
    "Laranja": "https://cdn-icons-png.flaticon.com/512/1728/1728739.png",
    "Maçã": "https://cdn-icons-png.flaticon.com/512/415/415733.png",
    "Banana": "https://cdn-icons-png.flaticon.com/512/2909/2909761.png",
    "Melancia": "https://cdn-icons-png.flaticon.com/512/2153/2153724.png",
    "Mamão": "https://cdn-icons-png.flaticon.com/512/2153/2153710.png",
    "Cenoura": "https://cdn-icons-png.flaticon.com/512/1041/1041355.png",
    "Tomate": "https://cdn-icons-png.flaticon.com/512/1202/1202125.png",
    "Alface": "https://cdn-icons-png.flaticon.com/512/2153/2153676.png",
    "Repolho": "https://cdn-icons-png.flaticon.com/512/2347/2347035.png",
    "Abóbora": "https://cdn-icons-png.flaticon.com/512/2153/2153718.png",
    "Pimentão": "https://cdn-icons-png.flaticon.com/512/2153/2153702.png",
    "Alho": "https://cdn-icons-png.flaticon.com/512/2153/2153674.png",
    "Milho": "https://cdn-icons-png.flaticon.com/512/2153/2153664.png",
    "Feijão": "https://cdn-icons-png.flaticon.com/512/8157/8157580.png", # Link reforçado
    "Amendoim": "https://cdn-icons-png.flaticon.com/512/2346/2346944.png"
}

# Exibição do Estoque
st.header("📦 Estoque Atual")
cols = st.columns(4)
for i, (item, qtd) in enumerate(st.session_state.estoque.items()):
    unidade = produtos_info[item]
    with cols[i % 4]:
        # Tenta carregar a imagem, se falhar coloca um ícone de caixa
        url_img = imagens.get(item, "https://cdn-icons-png.flaticon.com/512/679/679821.png")
        st.image(url_img, width=65)
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

st.sidebar.info("Sistema desenvolvido para o projeto acadêmico de ADS.")
