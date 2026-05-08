import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Sesmaria do Cerro - Doações", layout="wide")

# Estilo para manter as colunas lado a lado no celular
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

# 3. Dicionário de Produtos (Unidades e Imagens)
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

# 4. Função para Carregar Dados (TTL=0 força a leitura real)
def carregar_dados():
    try:
        # worksheet="Sheet1" garante que ele olhe para a aba certa
        df = conn.read(worksheet="Sheet1", ttl=0)
        if df is not None and not df.empty:
            # Converte a planilha para o dicionário de estoque
            dados_planilha = df.set_index("Produto")["Quantidade"].to_dict()
            estoque_final = {p: 0 for p in produtos_info.keys()}
            estoque_final.update(dados_planilha)
            return estoque_final
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
    
    return {p: 0 for p in produtos_info.keys()}

# 5. Função para Atualizar Planilha
def atualizar_planilha():
    try:
        df_save = pd.DataFrame(list(st.session_state.estoque.items()), columns=["Produto", "Quantidade"])
        conn.update(worksheet="Sheet1", data=df_save)
        st.toast("✅ Sincronizado com a Planilha!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

# Inicialização do Estoque
if 'estoque' not in st.session_state:
    st.session_state.estoque = carregar_dados()

# --- INTERFACE ---
st.title("🚜 Sesmaria do Cerro")

st.header("📦 Estoque Atual")
col1, col2 = st.columns(2)
itens = list(st.session_state.estoque.items())

for i, (item, qtd) in enumerate(itens):
    caixa = col1 if i < 10 else col2
    with caixa:
        st.image(produtos_info[item]["img"], width=45)
        st.write(f"**{item}:** {qtd} {produtos_info[item]['un']}")
        st.write("---")

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.subheader("➕ Doar")
    p_doar = st.selectbox("Item", list(produtos_info.keys()), key="sel_doar")
    q_doar = st.number_input("Qtd", min_value=0, step=1, key="num_doar")
    if st.button("Confirmar Doação", use_container_width=True):
        st.session_state.estoque[p_doar] += q_doar
        atualizar_planilha()
        st.rerun()

with c2:
    st.subheader("➖ Retirar")
    p_ret = st.selectbox("Item", list(produtos_info.keys()), key="sel_ret")
    q_ret = st.number_input("Qtd", min_value=0, step=1, key="num_ret")
    if st.button("Confirmar Retirada", use_container_width=True):
        if st.session_state.estoque[p_ret] >= q_ret:
            st.session_state.estoque[p_ret] -= q_ret
            atualizar_planilha()
            st.rerun()
        else:
            st.error("Sem estoque suficiente!")
            
