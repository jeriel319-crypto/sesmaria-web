import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Sesmaria do Cerro - Doações", layout="wide")

# Estilo para colunas lado a lado no celular
st.markdown("""
    <style>
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Lista de produtos e imagens (O visual que você gosta)
produtos_info = {
    "Beterraba": {"un": "kg", "img": "https://img.icons8.com/color/144/beet.png"},
    "Abacaxi": {"un": "unid", "img": "https://img.icons8.com/color/144/pineapple.png"},
    "Cebola": {"un": "kg", "img": "https://img.icons8.com/color/144/onion.png"},
    "Batata": {"un": "kg", "img": "https://img.icons8.com/color/144/potato.png"},
    "Laranja": {"un": "kg", "img": "https://img.icons8.com/color/144/orange.png"},
    "Maçã": {"un": "kg", "img": "https://img.icons8.com/color/144/apple.png"},
    "Banana": {"un": "kg", "img": "https://img.icons8.com/color/144/banana.png"},
    "Melancia": {"un": "unid", "img": "https://img.icons8.com/color/144/watermelon.png"},
    "Mamão": {"un": "unid", "img": "https://img.icons8.com/color/144/papaya.png"},
    "Cenoura": {"un": "kg", "img": "https://img.icons8.com/color/144/carrot.png"},
    "Tomate": {"un": "unid", "img": "https://img.icons8.com/color/144/tomato.png"},
    "Alface": {"un": "unid", "img": "https://img.icons8.com/color/144/lettuce.png"},
    "Repolho": {"un": "unid", "img": "https://img.icons8.com/color/144/cabbage.png"},
    "Abóbora": {"un": "unid", "img": "https://img.icons8.com/color/144/pumpkin.png"},
    "Pimentão": {"un": "unid", "img": "https://img.icons8.com/color/144/paprika.png"},
    "Alho": {"un": "kg", "img": "https://img.icons8.com/color/144/garlic.png"},
    "Milho": {"un": "unid", "img": "https://img.icons8.com/color/144/corn.png"},
    "Amendoim": {"un": "kg", "img": "https://img.icons8.com/color/144/peanuts.png"},
    "Limão": {"un": "kg", "img": "https://img.icons8.com/color/144/citrus.png"},
    "Uva": {"un": "kg", "img": "https://img.icons8.com/color/144/grapes.png"}
}

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        if df is not None and not df.empty:
            return df.set_index("Produto")["Quantidade"].to_dict()
    except:
        pass
    return {p: 0 for p in produtos_info.keys()}

def atualizar_planilha():
    df_save = pd.DataFrame(list(st.session_state.estoque.items()), columns=["Produto", "Quantidade"])
    try:
        # Tenta atualizar especificando a aba Sheet1
        conn.update(worksheet="Sheet1", data=df_save)
        st.toast("✅ Sincronizado com a Planilha!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

if 'estoque' not in st.session_state:
    st.session_state.estoque = carregar_dados()

st.title("🚜 Sesmaria do Cerro")

# Exibição do Estoque com Imagens
st.header("📦 Estoque Atual")
col1, col2 = st.columns(2)
itens = list(st.session_state.estoque.items())

for i, (item, qtd) in enumerate(itens):
    caixa = col1 if i < 10 else col2
    with caixa:
        st.image(produtos_info[item]["img"], width=40)
        st.write(f"**{item}:** {qtd} {produtos_info[item]['un']}")
        st.write("---")

st.divider()

# Doação e Retirada
c_doar, c_retirar = st.columns(2)
with c_doar:
    st.subheader("➕ Doação")
    p_doar = st.selectbox("Item", list(produtos_info.keys()), key="d")
    q_doar = st.number_input("Qtd", min_value=0, step=1, key="qd")
    if st.button("Confirmar Doação", use_container_width=True):
        st.session_state.estoque[p_doar] += q_doar
        atualizar_planilha()
        st.rerun()

with c_retirar:
    st.subheader("➖ Retirada")
    p_ret = st.selectbox("Item", list(produtos_info.keys()), key="r")
    q_ret = st.number_input("Qtd", min_value=0, step=1, key="qr")
    if st.button("Confirmar Retirada", use_container_width=True):
        if st.session_state.estoque[p_ret] >= q_ret:
            st.session_state.estoque[p_ret] -= q_ret
            atualizar_planilha()
            st.rerun()
        else:
            st.error("Estoque insuficiente!")
            
