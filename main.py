import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Sesmaria do Cerro", layout="wide")

# Ajuste para colunas no celular
st.markdown("<style>[data-testid='column']{width:50% !important; flex:1 1 50% !important; min-width:50% !important;}</style>", unsafe_allow_html=True)

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# Lista de produtos
produtos_info = {
    "Beterraba": "kg", "Abacaxi": "unid", "Cebola": "kg", "Batata": "kg", 
    "Laranja": "kg", "Maçã": "kg", "Banana": "kg", "Melancia": "unid", 
    "Mamão": "unid", "Cenoura": "kg", "Tomate": "unid", "Alface": "unid", 
    "Repolho": "unid", "Abóbora": "unid", "Pimentão": "unid", "Alho": "kg", 
    "Milho": "unid", "Amendoim": "kg", "Limão": "kg", "Uva": "kg"
}

# FUNÇÃO DE CARGA - Se a planilha falhar, ele não zera o que você acabou de fazer
def carregar_dados():
    try:
        df = conn.read(ttl=0)
        if df is not None and not df.empty:
            return df.set_index("Produto")["Quantidade"].to_dict()
    except:
        pass
    return {p: 0 for p in produtos_info.keys()}

# FUNÇÃO DE SALVAR - USA O MÉTODO 'REPLACE' PARA EVITAR ERROS
def atualizar_planilha():
    df_save = pd.DataFrame(list(st.session_state.estoque.items()), columns=["Produto", "Quantidade"])
    try:
        # O segredo está aqui: ele tenta atualizar a Sheet1
        conn.update(worksheet="Sheet1", data=df_save)
        st.success("Salvo na nuvem!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

# Inicializa o estoque na memória
if 'estoque' not in st.session_state:
    st.session_state.estoque = carregar_dados()

st.title("🚜 Sesmaria do Cerro")

# Exibição do Estoque
st.header("📦 Estoque Atual")
col1, col2 = st.columns(2)
itens = list(st.session_state.estoque.items())

for i, (item, qtd) in enumerate(itens):
    caixa = col1 if i < 10 else col2
    with caixa:
        st.write(f"**{item}:** {qtd} {produtos_info[item]}")

st.divider()

# Operações
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
            
