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

# 3. Lista de produtos e unidades
produtos_info = {
    "Beterraba": "kg", "Abacaxi": "unid", "Cebola": "kg", "Batata": "kg", 
    "Laranja": "kg", "Maçã": "kg", "Banana": "kg", "Melancia": "unid", 
    "Mamão": "unid", "Cenoura": "kg", "Tomate": "unid", "Alface": "unid", 
    "Repolho": "unid", "Abóbora": "unid", "Pimentão": "unid", "Alho": "kg", 
    "Milho": "unid", "Amendoim": "kg", "Limão": "kg", "Uva": "kg"
}

# 4. Função para carregar dados (Lê da planilha ou gera zeros)
def carregar_dados():
    try:
        df = conn.read(ttl=0)
        if df is None or df.empty:
            return {p: 0 for p in produtos_info.keys()}
        # Converte a planilha em um dicionário
        return df.set_index("Produto")["Quantidade"].to_dict()
    except:
        return {p: 0 for p in produtos_info.keys()}

# 5. Função para salvar dados (Força a gravação no Google)
def atualizar_planilha():
    try:
        # Prepara a tabela com os nomes e valores atuais
        df_save = pd.DataFrame(list(st.session_state.estoque.items()), columns=["Produto", "Quantidade"])
        # Limpa o cache do Streamlit
        st.cache_data.clear()
        # Envia para o Google Sheets
        conn.update(data=df_save)
        st.toast("✅ Gravado na Planilha!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

# Inicializa o estoque se não existir
if 'estoque' not in st.session_state:
    st.session_state.estoque = carregar_dados()

# --- INTERFACE DO USUÁRIO ---

with st.expander("📲 COMO INSTALAR NO CELULAR", expanded=True):
    st.info("Clique nos 3 pontinhos do navegador e escolha 'Adicionar à tela inicial'.")

st.title("🚜 Sesmaria do Cerro")

# Links das imagens
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
col1, col2 = st.columns(2)

itens = list(st.session_state.estoque.items())
for i, (item, qtd) in enumerate(itens):
    caixa = col1 if i < 10 else col2
    with caixa:
        st.image(imagens[item], width=40)
        st.write(f"**{item}:** {qtd} {produtos_info[item]}")
        st.write("---")

st.divider()

# Painel de Doação e Retirada
c_doar, c_retirar = st.columns(2)

with c_doar:
    st.subheader("➕ Doar")
    p_doar = st.selectbox("O que vai doar?", list(produtos_info.keys()), key="sel_doar")
    q_doar = st.number_input(f"Qtd ({produtos_info[p_doar]}):", min_value=0, step=1, key="num_doar")
    if st.button("Confirmar Doação", use_container_width=True):
        st.session_state.estoque[p_doar] += q_doar
        atualizar_planilha()
        st.rerun()

with c_retirar:
    st.subheader("➖ Retirar")
    p_ret = st.selectbox("O que vai retirar?", list(produtos_info.keys()), key="sel_ret")
    q_ret = st.number_input(f"Qtd ({produtos_info[p_ret]}):", min_value=0, step=1, key="num_ret")
    if st.button("Confirmar Retirada", use_container_width=True):
        if st.session_state.estoque[p_ret] >= q_ret:
            st.session_state.estoque[p_ret] -= q_ret
            atualizar_planilha()
            st.rerun()
        else:
            st.error("Estoque insuficiente!")

st.sidebar.write("🌱 **Sesmaria do Cerro**")
        
