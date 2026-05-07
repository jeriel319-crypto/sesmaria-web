import streamlit as st

# Configuração da página para visual amplo
st.set_page_config(page_title="Sesmaria do Cerro - Doações", layout="wide")

st.title("🚜 Sesmaria do Cerro - Sistema de Doações")
st.write("Gerencie as doações e retiradas de alimentos de forma profissional.")

# Lista completa de 22 produtos
produtos_iniciais = [
    "Beterraba", "Abacaxi", "Cebola", "Batata", "Mandioca", "Chuchu", "Maracujá",
    "Laranja", "Maçã", "Banana", "Melancia", "Mamão", "Cenoura", "Tomate",
    "Alface", "Repolho", "Abóbora", "Pimentão", "Alho", "Milho", "Feijão", "Arroz"
]

# Inicialização do estoque no estado da sessão
if 'estoque' not in st.session_state:
    st.session_state.estoque = {produto: 0 for produto in produtos_iniciais}

# Dicionário de imagens nítidas (Links estáveis do Icons8)
imagens = {
    "Beterraba": "https://img.icons8.com/color/144/beet.png",
    "Abacaxi": "https://img.icons8.com/color/144/pineapple.png",
    "Cebola": "https://img.icons8.com/color/144/onion.png",
    "Batata": "https://img.icons8.com/color/144/potato.png",
    "Mandioca": "https://img.icons8.com/color/144/tapioca.png",
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
    "Feijão": "https://img.icons8.com/color/144/beans.png",
    "Arroz": "https://img.icons8.com/color/144/rice.png"
}

# Exibição do Estoque em Grid (Grade)
st.header("📦 Estoque Atual")
# Organiza em 4 colunas para não ficar muito apertado no celular
cols = st.columns(4)
for i, (item, qtd) in enumerate(st.session_state.estoque.items()):
    with cols[i % 4]:
        st.image(imagens[item], width=60)
        st.metric(label=item, value=f"{qtd} kg")

st.divider()

# Área de Transações
col1, col2 = st.columns(2)

with col1:
    st.subheader("➕ Registrar Doação")
    item_doar = st.selectbox("Selecione o item:", produtos_iniciais, key="doar")
    qtd_doar = st.number_input("Quantidade (kg):", min_value=0, step=1, key="n_doar")
    if st.button("Confirmar Doação"):
        st.session_state.estoque[item_doar] += qtd_doar
        st.success(f"Adicionado {qtd_doar}kg de {item_doar}!")
        st.rerun()

with col2:
    st.subheader("➖ Registrar Retirada")
    item_retirar = st.selectbox("Selecione o item:", produtos_iniciais, key="retirar")
    qtd_retirar = st.number_input("Quantidade (kg):", min_value=0, step=1, key="n_retirar")
    if st.button("Confirmar Retirada"):
        if st.session_state.estoque[item_retirar] >= qtd_retirar:
            st.session_state.estoque[item_retirar] -= qtd_retirar
            st.warning(f"Retirado {qtd_retirar}kg de {item_retirar}!")
            st.rerun()
        else:
            st.error("Estoque insuficiente!")

st.sidebar.info("Sistema desenvolvido para o projeto acadêmico de ADS.")
        
