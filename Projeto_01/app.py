"""
Autor: Matheus Silva
Data: Maio 2022
Este projeto constrói uma aplicação
streamlit para visualização de dados
dos preços da gasolina no Brasil.
"""
import logging
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# configurando o logging
logging.basicConfig(
    filename="./results.log",
    level=logging.INFO,
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s")

def read_data(file_path):
    """Read data from csv.
    Args:
        file_path (str): file path to read.
    Return:
        df_file (DataFrame): returns the file read as a dataframe.
    """
    try:
        if "ca-" in file_path:
            df_file = pd.read_csv(file_path, sep = ";", encoding="ISO-8859-1")
        else:
            df_file = pd.read_csv(file_path)
        return df_file
    except FileNotFoundError: # pylint: disable=bare-except
        logging.error("Error read_csv. We were not able to find %s", file_path)
        return pd.Dataframe()

st.title("Analisando o preço da gasolina brasileira (2004 - 2021)")

st.subheader("A Streamlit web app by Matheus Silva and Yolanda Dantas")

st.markdown("Este projeto da disciplina de Mlops da UFRN visa analisar a variável do\
            preço da gasolina brasileira, como base se utilizou os dados disponibilizados\
            pelo governo federal na [série histórica de preços de combustíveis](\
            https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis)\
            que vai de 2004 até 2021. Cada ano possui dois arquivos, para cada semestre. \
            Exemplo do arquivo csv do segundo semestre de 2021:")

st.caption("ca_2021_02.head()")

ca_2021_02 = read_data("data/serie_historica_combustiveis/ca-2021-02.csv")

st.dataframe(ca_2021_02.head())

st.markdown("Após o download dos arquivos csv foi feito um tratamento de dados\
            coletando a média do preço da gasolina anual entre 2004 e 2021.")

gas_precos = read_data("data/gasolina_precos-2004-2021.csv")

st.dataframe(gas_precos)

st.markdown("Dataframe em gráfico de linha:")

gas_precos["Tempo"] = pd.to_datetime(gas_precos["Tempo"])

line_chart1 = px.line(gas_precos, x="Tempo", y="Preco_Media",
                      title = "Valor de venda da gasolina (2004 - 2021)",
                      labels={"Preco_Media": "Litro da gasolina (R$) - Média"})
st.plotly_chart(line_chart1, use_container_width=True)

st.markdown("Vendo a variação da inflação (editar texto)")

inflacao_gasolina = read_data("data/inflacao-semestral-gasolina-2004-2021.csv")
inflacao_gasolina["Tempo"] = pd.to_datetime(inflacao_gasolina["Tempo"])
# Create figure with secondary y-axis
line_chart3 = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
line_chart3.add_trace(
    go.Scatter(x=inflacao_gasolina["Tempo"],
               y=inflacao_gasolina["ipca_media_semestral"],
               name="IPCA Média Semestral"),
    secondary_y=False,
)
line_chart3.add_trace(
    go.Scatter(x=inflacao_gasolina["Tempo"],
               y=inflacao_gasolina["ipca_acumulado"],
               name="IPCA Acumulado"),
    secondary_y=False,
)
line_chart3.add_trace(
    go.Scatter(x=gas_precos["Tempo"],
               y=gas_precos["Preco_Media"],
               name="Preço da gasolina"),
    secondary_y=True, #second y-axis
)
# Add figure title
line_chart3.update_layout(
    title_text="Valor de venda e inflação da gasolina (2004 - 2021)",
    xaxis_title="Tempo"
)
# Set y-axes titles
line_chart3.update_yaxes(title_text="Inflação porcentagem", secondary_y=False)
line_chart3.update_yaxes(title_text="Litro da gasolina (R$) - Média", secondary_y=True)
st.plotly_chart(line_chart3)

st.markdown("Com o preço da gasolina foi possível fazer a atualização dos preços\
            pela variação do [Índice de Preços ao Consumidor Amplo (IPCA)](\
            https://www.ibge.gov.br/explica/inflacao.php) de abril de 2022.")

precos_atualizados = read_data("data/gasolina_precos_atualizada-2004-2021.csv")
precos_atualizados = precos_atualizados.rename(columns = {"Preco_Media": "Preço sem ajuste",
                                               "Preco_Atualizado": "Preço ajustado"})

line_chart3 = px.line(precos_atualizados, x="Tempo", y=["Preço sem ajuste",
                                                        "Preço ajustado"])
line_chart3.update_layout(
    title = "Valor de venda da gasolina (2004 - 2021)",
    yaxis_title = "Litro da Gasolina (R$) - Média",
    legend_title = "",
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.40
    )
)
st.plotly_chart(line_chart3, use_container_width=True)

regioes_2021 = read_data("data/precos_regioes_2021.csv")

bar_chart1 = px.bar(regioes_2021, x="Regiao_Sigla", y="Preco_Media", text_auto=".3s",
                    title = "Valor de venda da gasolina por regiões em 2021",
                    labels={"Regiao_Sigla": "Regiões",
                            "Preco_Media": "Litro da Gasolina (R$) - Média"})
st.plotly_chart(bar_chart1, use_container_width=True)

estados_2021 = read_data("data/precos_estados_2021.csv")

bar_chart2 = px.bar(estados_2021, x="Estado_Sigla", y="Preco_Media", text_auto=".3s",
                    title = "Valor de venda da gasolina por estados em 2021",
                    labels={"Estado_Sigla": "Estados",
                            "Preco_Media": "Litro da Gasolina (R$) - Média"})
st.plotly_chart(bar_chart2, use_container_width=True)
