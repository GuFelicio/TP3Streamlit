import streamlit as st
import pandas as pd
import numpy as np
from matplotlib.pyplot import figure, ylabel, scatter, xlabel, title, pause

# 01. Explicação do Objetivo e Motivação
st.title("Dashboard de Dados de Turismo do Data.Rio")
st.write("""
Este dashboard foi desenvolvido para explorar dados de turismo do portal Data.Rio, permitindo aos usuários realizar upload de arquivos CSV, filtrar e selecionar dados específicos, visualizar informações através de gráficos e tabelas interativas, e personalizar a interface. A motivação é facilitar a análise e compreensão dos dados, ajudando a identificar tendências e padrões relevantes.
""")

# 02. Realizar Upload de Arquivo CSV
st.sidebar.header("Upload do Arquivo CSV")
arquivo_csv = st.sidebar.file_uploader("Carregue um arquivo CSV", type=["csv"])

if arquivo_csv is not None:
    df = pd.read_csv(arquivo_csv)
    st.sidebar.success("Arquivo carregado com sucesso!")

    # 03. Filtro de Dados e Seleção
    st.sidebar.header("Filtros e Seleção de Dados")
    colunas_selecionadas = st.sidebar.multiselect("Selecione as colunas que deseja visualizar", df.columns.tolist(),
                                                  default=df.columns.tolist())
    df_filtrado = df[colunas_selecionadas]

    if st.sidebar.checkbox("Mostrar Dados Filtrados"):
        st.write(df_filtrado)

    # 04. Desenvolver Serviço de Download de Arquivos
    csv_filtrado = df_filtrado.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(label="Baixar dados filtrados em CSV", data=csv_filtrado,
                               file_name='dados_filtrados.csv', mime='text/csv')

    # 05. Utilizar Barra de Progresso e Spinners
    with st.spinner('Processando o arquivo...'):
        progresso = st.progress(0)
        for i in range(100):
            progresso.progress(i + 1)
            pause(0.01)

    # 06. Utilizar Color Picker
    st.sidebar.header("Personalização de Cores")
    cor_fundo = st.sidebar.color_picker("Escolha a cor de fundo", "#ffffff")
    cor_fonte = st.sidebar.color_picker("Escolha a cor da fonte", "#000000")
    st.markdown(f"<style>body {{ background-color: {cor_fundo}; color: {cor_fonte}; }}</style>", unsafe_allow_html=True)


    # 07. Utilizar Funcionalidade de Cache
    @st.cache_data
    def carregar_dados():
        return df


    dados_cache = carregar_dados()

    # 08. Persistir Dados Usando Session State
    if 'filtros' not in st.session_state:
        st.session_state.filtros = colunas_selecionadas

    # 09. Criar Visualizações de Dados - Tabelas
    st.header("Visualização de Dados - Tabela Interativa")
    st.dataframe(df_filtrado)

    # 10. Criar Visualizações de Dados - Gráficos Simples
    st.header("Visualização de Dados - Gráficos Simples")
    opcao_grafico = st.selectbox("Escolha o tipo de gráfico", ["Barras", "Linhas", "Pizza"])

    if opcao_grafico == "Barras":
        st.bar_chart(df_filtrado)
    elif opcao_grafico == "Linhas":
        st.line_chart(df_filtrado)
    elif opcao_grafico == "Pizza":
        col_pizza = st.selectbox("Selecione a coluna para o gráfico de pizza", df_filtrado.columns)
        st.write(df_filtrado[col_pizza].value_counts().plot.pie(autopct="%1.1f%%"))
        st.pyplot()

    # 11. Criar Visualizações de Dados - Gráficos Avançados
    st.header("Visualização de Dados - Gráficos Avançados")
    if st.checkbox("Mostrar Gráfico Avançado"):
        col_x = st.selectbox("Selecione a coluna para o eixo X", df_filtrado.columns)
        col_y = st.selectbox("Selecione a coluna para o eixo Y", df_filtrado.columns)
        figure(figsize=(10, 6))
        scatter(df_filtrado[col_x], df_filtrado[col_y])
        xlabel(col_x)
        ylabel(col_y)
        title("Gráfico de Dispersão")
        st.pyplot()

    # 12. Exibir Métricas Básicas
    st.header("Métricas Básicas dos Dados")
    st.write(f"Total de Registros: {len(df_filtrado)}")
    st.write(f"Média de Valores: {df_filtrado.mean()}")
    st.write(f"Soma de Valores: {df_filtrado.sum()}")

else:
    st.warning("Por favor, faça o upload de um arquivo CSV para começar.")
