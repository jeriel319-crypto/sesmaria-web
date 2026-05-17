import streamlit as st
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

# --- ABA DE INSTRUÇÕES (PASSO A PASSO PARA INSTALAR NA TELA) ---
st.info("""
    **📱 Como instalar este sistema no seu celular:**
    1. Abra este link pelo navegador do seu celular (como o **Google Chrome**).
    2. Toque nos **três pontinhos (⋮)** no canto superior direito do navegador.
    3. Selecione a opção **"Adicionar à tela inicial"** ou **"Instalar aplicativo"**.
    4. Pronto! Ele ficará na sua tela igual a um aplicativo instalado.
""")

# 2. Configuração do LINK DIRETO de exportação (Método Nativo e Sem Erros)
# Convertemos o link para formato CSV, eliminando qualquer chance de erro 404 da biblioteca antiga
URL_BASE = "https://docs.google.com/spreadsheets/d/1G9YlN3jMTe1ewSk8wBhGPfiwqMf61l0IiXpOZTsoivA"
URL_CSV = f"{URL_BASE}/export?format=csv&gid=0"

# 3. Dicionário de Produtos
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

# 4. Função para Carregar Dados (Usando Pandas Direto)
def carregar_dados():
    try:
        df = pd.read_csv(URL_CSV)
        if df is not None and not df.empty:
            df.columns = df.columns.str.strip()
            df["Produto"] = df["Produto"].str.strip().str.capitalize()
            dados_planilha = df.set_index("Produto")["Quantidade"].to_dict()
            
            estoque_final = {p: 0 for p in produtos_info.keys()}
            estoque_final.update(dados_planilha)
            return estoque_final
    except Exception as e:
        st.error(f"Erro ao ler dados da planilha: {e}")
    return {p: 0 for p in produtos_info.keys()}

# 5. Função para Atualizar Planilha
def atualizar_planilha():
    st.warning("⚠️ Para salvar alterações permanentes na nuvem, configure as credenciais de escrita do gsheets ou use o formulário integrado.")
    # Mantém a atualização local no session_state para a interface funcionar perfeitamente em tempo real
    st.toast("🔄 Atualizado localmente na tela!")

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
            st.error("Sem estoque!")
