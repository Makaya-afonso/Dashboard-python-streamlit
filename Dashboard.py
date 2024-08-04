import streamlit as st
import pandas as pd
import plotly.express as px

# INDICADORES
# Com uma Visão Mensal
# Faturamento por Unidade
# Tipo de Produto mais vendido, contribuição por filial
# Desempenho das formas de pagamento
# Como estão as avaliações das filiais?

# tamanho cheia
st.set_page_config(layout="wide")

# Ler Arquivo CSV
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")

# Converter a coluna data no formato de Data
df["Date"] = pd.to_datetime(df["Date"])
# Ordenar o DataFrame pela coluna "Date" de forma decrescente
df = df.sort_values(by="Date", ascending=True)

# Adicionar uma nova coluna "Month" com apenas ano e mês
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Posicionar os meses no Sidebar em um selectbox
mes_filtro = st.sidebar.selectbox("Escolha o Mês", df["Month"].unique())

# DataFrame filtrado
df_filtrado = df[df["Month"] == mes_filtro]

# Estrutura da tela
frame1, frame2 = st.columns(2)
frame3, frame4, frame5 = st.columns(3)

# Criar gráfico de barra com Plotly
fig_date = px.bar(df_filtrado, x='Date', y='Total', color="City", title='Total de Vendas por Dia')
fig_date.update_layout(
    xaxis_title='Data',
    yaxis_title='Total'
)
frame1.plotly_chart(fig_date, use_container_width=True)

# Criar gráfico de barra com Plotly
fig_product = px.bar(df_filtrado, x='Date', y='Product line', color="City", title='Total de Vendas por Tipo de Produto', orientation="h")
fig_product.update_layout(
    xaxis_title='Data',
    yaxis_title='Total'
)
frame2.plotly_chart(fig_product, use_container_width=True)

# Avalição de agrupamento
city_total = df_filtrado.groupby("City")[["Total"]].sum().reset_index()
# Criar gráfico de barra com Plotly
fig_city = px.bar(city_total, x='City', y='Total', title='Faturamento por filiais')
fig_city.update_layout(
    xaxis_title='Data',
    yaxis_title='Total'
)
frame3.plotly_chart(fig_city, use_container_width=True)

# Criar gráfico de barra com Plotly
fig_kind = px.pie(df_filtrado, values="Total", names="Payment", title='Faturamento por Tipo de Pagamento')
frame4.plotly_chart(fig_kind, use_container_width=True)

# Avalição de agrupamento
city_mean = df_filtrado.groupby("City")[["Rating"]].mean().reset_index()
# Criar gráfico de barra com Plotly
fig_rating = px.bar(city_mean, x='City', y='Rating', title='Avaliação')
fig_rating.update_layout(
    xaxis_title='City',
    yaxis_title='Rating'
)
frame5.plotly_chart(fig_rating, use_container_width=True)