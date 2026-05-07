import streamlit as st

# Configuração da página
st.set_page_config(page_title="Sesmaria do Cerro - Doações", layout="wide")

st.title("🚜 Sesmaria do Cerro - Sistema de Doações")
st.write("Gerencie as doações e retiradas de alimentos da região.")

# Lista de produtos regionalizada (Arroz removido)
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

# Dicionário de imagens (Links reforçados para garantir exibição)
imagens = {
    "Beterraba": "https://img.icons8.com/color/144/beet.png",
    "Abacaxi": "https://img.icons8.com/color/144/pineapple.png",
    "Cebola": "https://img.icons8.com/color/144/onion.png",
    "Batata": "https://img.icons8.com/color/144/potato.png",
    "Mandioca": "https://img.icons8.com/color/144/sweet-potato.png", 
    "Chuchu": "https://img.icons8.com/color/144/squash.png",
    "Maracujá": "https://img.icons8.com/color/144/passion-fruit.png",
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
    "Feijão": "https://img.icons8.com/color/144/kidney-beans.png",
    "Amendoim": "https://img.icons8.com/color/144/peanuts.png"
}

# Exibição do Estoque
st.header("📦 Estoque Atual")
cols = st.columns(4)
for i, (item, qtd) in enumerate(st.session_state.estoque.items()):
    unidade = produtos_info[item]
    with cols[i % 4]:
        st.image(imagens.get(item, "https://img.icons8.com/color/144/box.png"), width=65)
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
            
