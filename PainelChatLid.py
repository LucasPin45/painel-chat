import streamlit as st
import pandas as pd
from unidecode import unidecode

# CONFIG DO APP
st.set_page_config(page_title="Painel de Lideranças", layout="wide")
st.image("https://www.consilliumrig.com.br/wp-content/uploads/2022/07/02_Logotipo_Consillium-1024x218.png", width=300)
st.title("📂 Lista dos líderes com Filtros")



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

# === LEITURA DO CSV PADRONIZADO ===
@st.cache_data
def carregar_dados():
    df = pd.read_csv("liderancas.csv", sep=";", encoding="utf-8")
    df.columns = df.columns.str.strip().str.title()
    for nome, dados in dados_complementares.items():
        df.loc[df["Nome Parlamentar"] == nome, "Foto"] = dados["foto"]
        df.loc[df["Nome Parlamentar"] == nome, "Perfil"] = dados["perfil"]
    return df

df = carregar_dados()

# === PREPROCESSAMENTO PARA BUSCA RÁPIDA ===
df['nome_clean'] = df['Nome Parlamentar'].apply(lambda x: unidecode(str(x).lower()))
df['partido_clean'] = df['Partido'].apply(lambda x: unidecode(str(x).lower()))
df['rep_clean'] = df['Representação'].apply(lambda x: unidecode(str(x).lower()))

# === CONTROLE DE CONTEXTO PARA CHAT ===
if "contexto" not in st.session_state:
    st.session_state.contexto = None

# === FILTROS ===
partidos = sorted(df['Partido'].dropna().unique())
ufs = sorted(df['Uf'].dropna().unique())
representacoes = sorted(df['Representação'].dropna().unique())

partido_sel = st.selectbox("Filtrar por Partido", options=["Todos"] + partidos)
uf_sel = st.selectbox("Filtrar por UF", options=["Todos"] + ufs)
rep_sel = st.selectbox("Filtrar por Representação", options=["Todas"] + representacoes)
nome_busca = st.text_input("🔎 Buscar por Nome, Representação ou Partido")

# === APLICA FILTROS ===
df_filtrado = df.copy()

if partido_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Partido"] == partido_sel]
if uf_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Uf"] == uf_sel]
if rep_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Representação"] == rep_sel]
if nome_busca:
    termo = unidecode(nome_busca.lower())
    df_filtrado = df_filtrado[
        df_filtrado['nome_clean'].str.contains(termo) |
        df_filtrado['rep_clean'].str.contains(termo) |
        df_filtrado['partido_clean'].str.contains(termo)
    ]

# === EXIBIÇÃO DOS RESULTADOS ===
st.markdown(f"### 👥 {len(df_filtrado)} líder(es) encontrado(s)")

if not df_filtrado.empty:
    for _, row in df_filtrado.iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            if 'Foto' in row and pd.notna(row['Foto']):
                st.image(row['Foto'], width=110)
        with col2:
            nome_link = f"[{row['Nome Parlamentar']}]({row['Perfil']})" if pd.notna(row.get("Perfil")) else row["Nome Parlamentar"]
            st.markdown(f"**{nome_link}**")
            st.markdown(f"Líder {row['Representação']}")
            st.markdown(f"📞 {row['Telefone']}")
            st.markdown(f"📧 {row['Correio Eletrônico']}")
            st.markdown(f"🏢 Gabinete: {row['Endereço Gabinete']}")
            st.markdown(f"🏛️ Liderança: {row['Endereço Liderança']}")
        st.markdown("---")
else:
    st.warning("Nenhum líder encontrado com os filtros aplicados.")

# === ÁREA DO CHAT ===
st.markdown("### 🤖 Chat sobre os Líderes - Pergunte diretamente quem é o líder, email, telefone")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

pergunta = st.chat_input("Pergunte sobre os contatos dos líderes")
if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    termo = unidecode(pergunta.lower())
    campos_alvo = {
        "email": "Correio Eletrônico",
        "e-mail": "Correio Eletrônico",
        "correio": "Correio Eletrônico",
        "telefone": "Telefone",
        "gabinete": "Endereço Gabinete",
        "lideranca": "Endereço Liderança",
        "liderança": "Endereço Liderança"
    }

    resposta = ""
    alvo_especifico = next((campo for campo in campos_alvo if campo in termo), None)

    if alvo_especifico:
        if st.session_state.contexto:
            lider = st.session_state.contexto
            linha = df[df['Nome Parlamentar'] == lider]
            if not linha.empty:
                resposta = f"{alvo_especifico.title()} de {lider}: {linha.iloc[0][campos_alvo[alvo_especifico]]}"
        else:
            encontrados = df[df['nome_clean'].apply(lambda x: x in termo)]
            if not encontrados.empty:
                row = encontrados.iloc[0]
                resposta = f"{alvo_especifico.title()} de {row['Nome Parlamentar']}: {row[campos_alvo[alvo_especifico]]}"
                st.session_state.contexto = row['Nome Parlamentar']
            else:
                resposta = "❌ Por favor, mencione o nome do líder para obter essa informação."
    else:
        encontrados = df[df.apply(lambda row: any(t in termo for t in [row['partido_clean'], row['nome_clean'], row['rep_clean'], f"lider do {row['partido_clean']}"]), axis=1)]
        if encontrados.empty:
            resposta = "❌ Nenhum líder encontrado com esse termo."
        else:
            resposta = "\n\n".join([f"**{row['Nome Parlamentar']} ({row['Partido']}/{row['Uf']})** — {row['Representação']}\nGabinete: {row['Endereço Gabinete']}\nLiderança: {row['Endereço Liderança']}" for _, row in encontrados.iterrows()])
            if len(encontrados) == 1:
                st.session_state.contexto = encontrados.iloc[0]['Nome Parlamentar']

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
    st.rerun()
