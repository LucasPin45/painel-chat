import streamlit as st
import pandas as pd
from unidecode import unidecode
import time

st.set_page_config(page_title="Painel de Lideranças", layout="wide")
st.image("https://www.consilliumrig.com.br/wp-content/uploads/2022/07/02_Logotipo_Consillium-1024x218.png", width=300)
st.title("📂 Líderes da Câmara dos Deputados")

# === DADOS COMPLEMENTARES DE FOTO E PERFIL ===
dados_complementares = {
    "Adolfo Viana": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204560.jpg", "perfil": "https://www.camara.leg.br/deputados/204560"},
    "Antonio Brito": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/160553.jpg", "perfil": "https://www.camara.leg.br/deputados/160553"},
    "Aureo Ribeiro": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/160512.jpg", "perfil": "https://www.camara.leg.br/deputados/160512"},
    "Doutor Luizinho": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204450.jpg", "perfil": "https://www.camara.leg.br/deputados/204450"},
    "Fred Costa": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204494.jpg", "perfil": "https://www.camara.leg.br/deputados/204494"},
    "Gilberto Abramo": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204491.jpg", "perfil": "https://www.camara.leg.br/deputados/204491"},
    "Isnaldo Bulhões Jr.": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204436.jpg", "perfil": "https://www.camara.leg.br/deputados/204436"},
    "Lindbergh Farias": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/74858.jpg", "perfil": "https://www.camara.leg.br/deputados/74858"},
    "Luis Tibé": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/160510.jpg", "perfil": "https://www.camara.leg.br/deputados/160510"},
    "Marcel van Hattem": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/156190.jpg", "perfil": "https://www.camara.leg.br/deputados/156190"},
    "Mário Heringer": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/74158.jpg", "perfil": "https://www.camara.leg.br/deputados/74158"},
    "Neto Carletto": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220703.jpg", "perfil": "https://www.camara.leg.br/deputados/220703"},
    "Pedro Campos": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220667.jpg", "perfil": "https://www.camara.leg.br/deputados/220667"},
    "Pedro Lucas Fernandes": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/122974.jpg", "perfil": "https://www.camara.leg.br/deputados/122974"},
    "Rodrigo Gambale": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220641.jpg", "perfil": "https://www.camara.leg.br/deputados/220641"},
    "Sóstenes Cavalcante": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/178947.jpg", "perfil": "https://www.camara.leg.br/deputados/178947"},
    "Talíria Petrone": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204464.jpg", "perfil": "https://www.camara.leg.br/deputados/204464"},
    "José Guimarães": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/141470.jpg", "perfil": "https://www.camara.leg.br/deputados/141470"},
    "Arlindo Chinaglia": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/73433.jpg", "perfil": "https://www.camara.leg.br/deputados/73433"},
    "Caroline de Toni": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204369.jpg", "perfil": "https://www.camara.leg.br/deputados/204369"},
    "Zucco": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220552.jpg", "perfil": "https://www.camara.leg.br/deputados/220552"}
}

@st.cache_data
def carregar_dados():
    df = pd.read_excel("liderancas.xlsx")
    df.columns = df.columns.str.strip()
    return df

def criar_link_whatsapp(numero):
    if pd.notna(numero) and "xxxx" not in str(numero):
        numero_limpo = str(numero).replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        return f"https://wa.me/55{numero_limpo}"
    return None

# Carrega os dados
df = carregar_dados()

# Preprocessamento
df["nome_clean"] = df["Nome_Parlamentar"].fillna("").apply(lambda x: unidecode(str(x).lower()))
df["partido_clean"] = df["Partido"].fillna("").apply(lambda x: unidecode(str(x).lower()))
df["rep_clean"] = df["Representacao"].fillna("").apply(lambda x: unidecode(str(x).lower()))

# Filtros
partidos = sorted(df["Partido"].dropna().unique())
ufs = sorted(df["Uf"].dropna().unique())
representacoes = sorted(df["Representacao"].dropna().unique())

partido_sel = st.selectbox("Filtrar por Partido", options=["Todos"] + partidos)
uf_sel = st.selectbox("Filtrar por UF", options=["Todos"] + ufs)
rep_sel = st.selectbox("Filtrar por Representação", options=["Todas"] + representacoes)
nome_busca = st.text_input("🔎 Buscar por Nome, Representação ou Partido")

# Aplicar filtros
df_filtrado = df.copy()
if partido_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Partido"] == partido_sel]
if uf_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Uf"] == uf_sel]
if rep_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Representacao"] == rep_sel]
if nome_busca:
    termo = unidecode(nome_busca.lower())
    df_filtrado = df_filtrado[
        df_filtrado["nome_clean"].str.contains(termo) |
        df_filtrado["partido_clean"].str.contains(termo) |
        df_filtrado["rep_clean"].str.contains(termo)
    ]

# Exibição dos cards individuais
st.markdown(f"### 👥 {len(df_filtrado)} líder(es) encontrado(s)")
for _, row in df_filtrado.iterrows():
    col1, col2 = st.columns([1, 4])
    with col1:
        nome = row["Nome_Parlamentar"]
        if nome in dados_complementares:
            st.image(dados_complementares[nome]["foto"], width=100)
    with col2:
        nome = row["Nome_Parlamentar"]
        if nome in dados_complementares:
            link = dados_complementares[nome]["perfil"]
            st.markdown(f"**[{nome}]({link})**")
        else:
            st.markdown(f"**{nome}**")
        st.markdown(f"{row['Representacao']} — {row['Partido']}/{row['Uf']}")
        st.markdown(f"📧 {row['Correio_Eletronico']}")
        if pd.notna(row['Celular_Deputado']):
            link_dep = criar_link_whatsapp(row['Celular_Deputado'])
            if link_dep:
                st.markdown(f"🟢 [WhatsApp Deputado]({link_dep})")
        if pd.notna(row['Celular_Assessoria']):
            link_ass = criar_link_whatsapp(row['Celular_Assessoria'])
            if link_ass:
                st.markdown(f"💬 [WhatsApp Assessoria]({link_ass})")
        if pd.notna(row['Nome_assessor']):
            st.markdown(f"👤 Assessor(a): {row['Nome_assessor']}")
        st.markdown(f"🏢 Gabinete: {row['Endereco_Gabinete']}")
        st.markdown(f"🏛️ Liderança: {row['Endereco_Lideranca']}")
        st.markdown("---")

# Tabela com endereços
st.markdown("### 🏢 Tabela de Endereços dos Líderes")
st.dataframe(df_filtrado[["Nome_Parlamentar", "Representacao", "Partido", "Uf", "Endereco_Gabinete", "Endereco_Lideranca"]])

from difflib import get_close_matches

# === Chat com IA — Busca Semântica via Embeddings ===
import streamlit as st
import torch
from sentence_transformers import SentenceTransformer, util

# Função para carregar dados e embeddings
@st.cache_data
def carregar_dados_emb():
    import pandas as pd
    with open("embeddings/embeddings.pt", "rb") as f:
        embeddings = torch.load(f)
    dados = pd.read_excel("liderancas.xlsx")
    return embeddings, dados

# Função para busca semântica
def buscar_respostas(pergunta, embeddings, dados, modelo, top_k=5):
    partidos_conhecidos = dados['Partido'].unique().tolist()
    representacoes_conhecidas = dados['Representacao'].dropna().unique().tolist()

    # 1. Verifica se algum partido ou federação está presente na pergunta
    for partido in partidos_conhecidos + representacoes_conhecidas:
        if partido.lower() in pergunta.lower():
            filtro = dados[(dados['Partido'].str.lower() == partido.lower()) |
                           (dados['Representacao'].str.lower() == partido.lower())]
            if not filtro.empty:
                respostas_formatadas = []
                for idx, row in filtro.iterrows():
                    texto = row["Texto_Embedding"]
                    respostas_formatadas.append(f"**Resultado {idx+1}:** {texto}")
                return respostas_formatadas

    # 2. Caso não encontre partido, faz a busca semântica
    emb_pergunta = modelo.encode(pergunta, convert_to_tensor=True)
    similaridades = util.pytorch_cos_sim(emb_pergunta, embeddings)[0]
    top_resultados = torch.topk(similaridades, k=top_k)

    respostas_formatadas = []
    for score, idx in zip(top_resultados.values, top_resultados.indices):
        texto = dados.iloc[idx.item()]["Texto_Embedding"]
        respostas_formatadas.append(f"**Resultado {idx.item()+1}:** {texto}")
    return respostas_formatadas


# Carregamento de dados
modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings, dados = carregar_dados_emb()

# Interface do chat IA
st.markdown("## 🧠 Chat sobre os líderes na Câmara")

pergunta = st.text_input("Digite sua pergunta sobre o contato dos líderes:")

if pergunta:
    # Mapeamento direto por representações especiais
    representacoes_chave = {
        "governo": "Governo na Câmara",
        "oposição": "Oposição na Câmara",
        "minoria": "Minoria na Câmara",
        "maioria": "Maioria na Câmara"
    }

    pergunta_lower = pergunta.lower()
    resposta_direta = None

    for chave, representacao in representacoes_chave.items():
        if f"líder do {chave}" in pergunta_lower or f"líder da {chave}" in pergunta_lower:
            filtro = dados[dados["Representacao"] == representacao]
            if not filtro.empty:
                nome_lider = filtro.iloc[0]["Nome_Parlamentar"]
                resposta_direta = f"O líder da {representacao} é {nome_lider}."
            else:
                resposta_direta = f"Não foi possível localizar o líder da {representacao}."
            break

    if resposta_direta:
        st.markdown(f"**{resposta_direta}**")
    else:
        with st.spinner("Buscando informações..."):
            respostas = buscar_respostas(pergunta, embeddings, dados, modelo)
            for r in respostas:
                st.markdown("----")
                st.markdown(r)






