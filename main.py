import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Sesmaria do Cerro", layout="wide")

# Estilo para colunas no telemóvel
st.markdown("<style>[data-testid='column']{width:50% !important; flex:1 1 50% !important; min-width:50% !important;}</style>", unsafe_allow_html=True)

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# Lista de produtos e imagens
produtos_info = {
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

def carregar_dados():
    try:
        # Tenta ler a aba Sheet1
        df = conn.read(worksheet="Sheet1", ttl=0)
        if df is not None and not df.empty:
            # Limpa os nomes para evitar erros de digitação
            df.columns = [c.strip().capitalize() for c in df.columns]
            df['Produto'] = df['Produto'].str.strip().str.capitalize()
            return df.set_index("Produto")["Quantidade"].to_dict()
    except:
        pass
    return {p: 0 for p in produtos_info.keys()}

def atualizar_planilha():
    try:
        # Prepara os dados para salvar
        df_save = pd.DataFrame(list(st.session_state.estoque.items()), columns=["Produto", "Quantidade"])
        # Força a gravação na Sheet1
        conn.update(worksheet="Sheet1", data=df_save)
        st.toast("✅ Salvo com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

# Inicializa o estoque
if 'estoque' not in st.session_state:
    st.session_state.estoque = carregar_dados()

st.title("🚜 Sesmaria do Cerro")

# Exibição do Estoque com as Imagens
st.header("📦 Estoque Atual")
col1, col2 = st.columns(2)
itens = list(st.session_state.estoque.items())

for i, (item, qtd) in enumerate(itens):
    caixa = col1 if i < 10 else col2
    with caixa:
        st.image(produtos_info[item], width=40)
        st.write(f"**{item}:** {qtd}")
        st.write("---")

st.divider()

# Operações de Doação e Retirada
c1, c2 = st.columns(2)
with c1:
    st.subheader("➕ Doar")
    p_doar = st.selectbox("Item", list(produtos_info.keys()), key="d")
    q_doar = st.number_input("Qtd", min_value=0, step=1, key="qd")
    if st.button("Confirmar Doação"):
        st.session_state.estoque[p_doar] += q_doar
        atualizar_planilha()
        st.rerun()

with c2:
    st.subheader("➖ Retirar")
    p_ret = st.selectbox("Item", list(produtos_info.keys()), key="r")
    q_ret = st.number_input("Qtd", min_value=0, step=1, key="qr")
    if st.button("Confirmar Retirada"):
        if st.session_state.estoque[p_ret] >= q_ret:
            st.session_state.estoque[p_ret] -= q_ret
            atualizar_planilha()
            st.rerun()
        else:
            st.error("Sem estoque!")
        
