
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard de Combustíveis", layout="wide")

st.title("⛽ Dashboard de Preços de Combustíveis")
st.caption("Fonte: Dataset de preços médios, mínimos e máximos por tipo de combustível.")

# ======================
# CARREGAR DADOS
# ======================
@st.cache_data
def load_data():
    return pd.read_csv("combustivel_dataset.csv")

df = load_data()

# Criar coluna de data (ano-mês)
df["data"] = pd.to_datetime(df["ano"].astype(str) + "-" + df["mes"].astype(str) + "-01")

# ======================
# FILTROS
# ======================
st.sidebar.header("⚙️ Filtros")

anos = st.sidebar.multiselect("Selecione o(s) ano(s):", sorted(df["ano"].unique()), default=sorted(df["ano"].unique()))
df_filtered = df[df["ano"].isin(anos)]

# ======================
# VISÃO GERAL
# ======================
st.subheader("🔎 Visão Geral do Dataset")
c1, c2, c3 = st.columns(3)
c1.metric("Período", f"{df['ano'].min()} - {df['ano'].max()}")
c2.metric("Nº Registros", f"{df.shape[0]}")
c3.metric("Combustíveis analisados", "Gasolina, Etanol, Diesel, GLP, GNV")

with st.expander("👀 Amostra dos Dados"):
    st.dataframe(df_filtered.head(20), use_container_width=True)

# ======================
# SÉRIE TEMPORAL
# ======================
st.subheader("📈 Evolução dos Preços Médios")

combustiveis = {
    "Gasolina Comum": "gasolina_comum_preco_revenda_avg",
    "Gasolina Aditivada": "gasolina_aditivada_preco_revenda_avg",
    "Etanol Hidratado": "etanol_hidratado_preco_revenda_avg",
    "Óleo Diesel": "oleo_diesel_preco_revenda_avg",
    "Óleo Diesel S10": "oleo_diesel_s10_preco_revenda_avg",
    "GLP (Gás de Cozinha)": "gas_cozinha_glp_preco_revenda_avg",
    "GNV": "gas_natural_veicular_gnv_preco_revenda_avg"
}

selected_comb = st.multiselect("Selecione os combustíveis:", options=list(combustiveis.keys()), default=["Gasolina Comum", "Etanol Hidratado"])

if selected_comb:
    fig, ax = plt.subplots(figsize=(10,5))
    for comb in selected_comb:
        col = combustiveis[comb]
        ax.plot(df_filtered["data"], df_filtered[col], label=comb)
    ax.set_title("Evolução dos Preços Médios")
    ax.set_ylabel("Preço (R$)")
    ax.legend()
    st.pyplot(fig)

# ======================
# COMPARAÇÃO ENTRE COMBUSTÍVEIS
# ======================
st.subheader("⚖️ Comparação de Combustíveis")

meses_opcoes = sorted(df_filtered["mes"].unique())
ano_selecionado = st.selectbox("Selecione o ano para comparação:", sorted(df_filtered["ano"].unique()))
mes_selecionado = st.selectbox("Selecione o mês para comparação:", meses_opcoes)

df_mes = df_filtered[(df_filtered["ano"] == ano_selecionado) & (df_filtered["mes"] == mes_selecionado)]

cols_avg = [v for v in combustiveis.values()]
df_plot = df_mes[cols_avg].mean().reset_index()
df_plot.columns = ["Combustível", "Preço Médio"]
df_plot["Combustível"] = df_plot["Combustível"].map({v: k for k, v in combustiveis.items()})

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(data=df_plot, x="Combustível", y="Preço Médio", ax=ax)
ax.set_title(f"Comparação de Preços Médios ({mes_selecionado:02d}/{ano_selecionado})")
ax.set_ylabel("Preço (R$)")
ax.tick_params(axis='x', rotation=30)
st.pyplot(fig)

# ======================
# ESTATÍSTICAS DESCRITIVAS
# ======================
st.subheader("📐 Estatísticas Descritivas")
st.dataframe(df_filtered[[v for v in combustiveis.values()]].describe().transpose(), use_container_width=True)

# ======================
# CORRELAÇÃO
# ======================
st.subheader("🧠 Correlação entre Preços Médios")

corr = df_filtered[[v for v in combustiveis.values()]].corr()
fig, ax = plt.subplots(figsize=(7,6))
sns.heatmap(corr, annot=True, cmap="viridis", fmt=".2f")
ax.set_title("Matriz de Correlação entre Combustíveis")
st.pyplot(fig)
