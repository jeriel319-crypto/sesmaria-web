import streamlit as st
import requests

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

# ==============================================================================
# CONFIGURAÇÃO SEGURA DO AIRTABLE (PUXANDO DOS SECRETS DO STREAMLIT)
# ==============================================================================
AIRTABLE_TOKEN = st.secrets["AIRTABLE_TOKEN"]
BASE_ID = st.secrets["BASE_ID"]
TABLE_NAME = "Estoque"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}
URL_AIRTABLE = f"https://api.airtable.com/v1/{BASE_ID}/{TABLE_NAME}"
# ==============================================================================

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

# Funções de Comunicação com a Nuvem (API)
def carregar_dados_airtable():
    try:
        response = requests.get(URL_AIRTABLE, headers=HEADERS)
        if response.status_code == 200:
            records = response.json().get("records", [])
            estoque_nuvem = {}
            mapeamento_ids = {}
            
            for r in records:
                fields = r.get("fields", {})
                prod_nome = fields.get("Produto", "").strip().capitalize()
                qtd = fields.get("Quantidade", 0)
                if prod_nome:
                    estoque_nuvem[prod_nome] = qtd
                    mapeamento_ids[prod_nome] = r.get("id")
            
            estoque_final = {p: 0 for p in produtos_info.keys()}
            estoque_final.update(estoque_nuvem)
            
            return estoque_final, mapeamento_ids
        else:
            st.error(f"Erro ao ler Airtable: {response.status_code}")
    except Exception as e:
        st.error(f"Falha de conexão: {e}")
    return {p: 0 for p in produtos_info.keys()}, {}

def atualizar_quantidade_airtable(produto, nova_qtd, record_id=None):
    try:
        if record_id:
            url_item = f"{URL_AIRTABLE}/{record_id}"
            dados = {"fields": {"Quantidade": int(nova_qtd)}}
            res = requests.patch(url_item, headers=HEADERS, json=dados)
        else:
            dados = {"fields": {"Produto": produto, "Quantidade": int(nova_qtd)}}
            res = requests.post(URL_AIRTABLE, headers=HEADERS, json=dados)
        
        if res.status_code in [200, 201]:
            st.toast("✅ Sincronizado na Nuvem com sucesso!")
            return True
        else:
            st.error(f"Erro ao salvar: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"Falha ao enviar dados: {e}")
    return False

# Inicialização do estado
if 'estoque' not in st.session_state or 'ids' not in st.session_state:
    st.session_state.estoque, st.session_state.ids = carregar_dados_airtable()

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

# Operações de Doação e Retirada
c1, c2 = st.columns(2)
with c1:
    st.subheader("➕ Doar")
    p_doar = st.selectbox("Item", list(produtos_info.keys()), key="sel_doar")
    q_doar = st.number_input("Qtd", min_value=0, step=1, key="num_doar")
    if st.button("Confirmar Doação", use_container_width=True):
        nova_qtd = st.session_state.estoque[p_doar] + q_doar
        rec_id = st.session_state.ids.get(p_doar)
        if atualizar_quantidade_airtable(p_doar, nova_qtd, rec_id):
            st.session_state.estoque, st.session_state.ids = carregar_dados_airtable()
            st.rerun()

with c2:
    st.subheader("➖ Retirar")
    p_ret = st.selectbox("Item", list(produtos_info.keys()), key="sel_ret")
    q_ret = st.number_input("Qtd", min_value=0, step=1, key="num_ret")
    if st.button("Confirmar Retirada", use_container_width=True):
        if st.session_state.estoque[p_ret] >= q_ret:
            nova_qtd = st.session_state.estoque[p_ret] - q_ret
            rec_id = st.session_state.ids.get(p_ret)
            if atualizar_quantidade_airtable(p_ret, nova_qtd, rec_id):
                st.session_state.estoque, st.session_state.ids = carregar_dados_airtable()
                st.rerun()
        else:
            st.error("Quantidade insuficiente em estoque!")

st.divider()

if st.button("🔄 Sincronizar e Puxar Dados do Banco Nuvem", use_container_width=True):
    st.session_state.estoque, st.session_state.ids = carregar_dados_airtable()
    st.rerun()
