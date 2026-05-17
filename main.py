import streamlit as st

# 1. Configurações da Página
st.set_page_config(page_title="Sesmaria do Cerro - Doações", layout="wide")

# Manter colunas alinhadas no celular
st.markdown("""
    <style>
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ABA RETRÁTIL DE INSTRUÇÕES ---
with st.expander("ℹ️ Clique aqui para ver como instalar no celular"):
    st.write("""
        **📱 Passo a passo:**
        1. Abra este link pelo navegador do seu celular (como o **Google Chrome**).
        2. Toque nos **três pontinhos (⋮)** no canto superior direito.
        3. Selecione **"Adicionar à tela inicial"** ou **"Instalar aplicativo"**.
    """)

# Dicionário fixo de ícones e unidades do seu app
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

# ==============================================================================
# TRUQUE DO VÍDEO (MOCK/SIMULAÇÃO)
# ==============================================================================
# Pega os parâmetros da URL. Se o link terminar com ?maquina=2, ele carrega com as 10 beterrabas.
query_params = st.query_params

if 'estoque' not in st.session_state:
    # Inicializa tudo zerado padrão
    st.session_state.estoque = {p: 0 for p in produtos_info.keys()}
    
    # Se na URL tiver ?maquina=2, o telefone já inicia com as 10 beterrabas prontas!
    if query_params.get("maquina") == "2":
        st.session_state.estoque["Beterraba"] = 10

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

# Operações de Doação e Retirada (Rodando 100% local na memória)
c1, c2 = st.columns(2)
with c1:
    st.subheader("➕ Doar")
    p_doar = st.selectbox("Item", list(produtos_info.keys()), key="sel_doar")
    q_doar = st.number_input("Qtd", min_value=0, step=1, key="num_doar")
    if st.button("Confirmar Doação", use_container_width=True):
        st.session_state.estoque[p_doar] += q_doar
        st.toast("✅ Sincronizado na Nuvem com sucesso!")
        st.rerun()

with c2:
    st.subheader("➖ Retirar")
    p_ret = st.selectbox("Item", list(produtos_info.keys()), key="sel_ret")
    q_ret = st.number_input("Qtd", min_value=0, step=1, key="num_ret")
    if st.button("Confirmar Retirada", use_container_width=True):
        if st.session_state.estoque[p_ret] >= q_ret:
            st.session_state.estoque[p_ret] -= q_ret
            st.toast("✅ Sincronizado na Nuvem com sucesso!")
            st.rerun()
        else:
            st.error("Quantidade insuficiente em estoque!")

st.divider()

# Botão de Sincronizar apenas limpa a tela ou simula um carregamento de sucesso
if st.button("🔄 Sincronizar e Puxar Dados do Banco Nuvem", use_container_width=True):
    st.toast("🔄 Dados atualizados da Nuvem!")
    st.rerun()
    
