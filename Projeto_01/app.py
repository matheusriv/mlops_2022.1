'''
Autor: Matheus Silva
Data: Maio 2022
Este projeto constrói uma aplicação
streamlit para visualização de dados
dos preços da gasolina no Brasil.
'''
import logging
import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.express as px

# configurando o logging
logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

def read_data(file_path):
    """Read data from csv.
    Args:
        file_path (str): file path to read.
    Return:
        df_file (DataFrame): returns the file read as a dataframe.
    """
    try:
        if 'ca-' in file_path:
            df_file = pd.read_csv(file_path, sep = ';', encoding='ISO-8859-1')
        else:
            df_file = pd.read_csv(file_path)
        return df_file
    except FileNotFoundError: # pylint: disable=bare-except
        logging.error("Error read_csv. We were not able to find %s", file_path)
        return pd.Dataframe()

st.title('Analisando o preço da gasolina brasileira (2004 - 2021)')

st.subheader('A Streamlit web app by Matheus Silva and Yolanda Dantas')

st.markdown('Este projeto da disciplina de Mlops da UFRN visa analisar a variável do\
            preço da gasolina brasileira, como base se utilizou os dados disponibilizados\
            pelo governo federal na [série histórica de preços de combustíveis](\
            https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis)\
            que vai de 2004 até 2021. Cada ano possui dois arquivos, para cada semestre. \
            Exemplo do arquivo csv do segundo semestre de 2021:')

st.caption('ca_2021_02.head()')

ca_2021_02 = read_data('data/serie_historica_combustiveis/ca-2021-02.csv')
st.dataframe(ca_2021_02.head())

st.markdown('Após o download dos arquivos csv foi feito um tratamento de dados\
            coletando a média do preço da gasolina anual entre 2004 e 2021.')

gas_precos = read_data('data/gasolina_precos-2004-2021.csv')

st.dataframe(gas_precos)

st.markdown('Dataframe em gráfico de linha:')

gas_precos['Tempo'] = pd.to_datetime(gas_precos['Tempo'])

line_chart1 = px.line(gas_precos, x='Tempo', y='Preco_Media')
line_chart1.update_layout(
    title = "Valor de venda da gasolina (2004 - 2021)",
    yaxis_title = "Litro da gasolina (R$) - Média",
    font = dict(family = "Open Sans, monospace", size = 12)
)

st.plotly_chart(line_chart1, use_container_width=True)

st.markdown('Com esses valores foi possível fazer a atualização dos preços\
            pela variação do [Índice de Preços ao Consumidor Amplo (IPCA)](\
            https://www.ibge.gov.br/explica/inflacao.php) de abril de 2022.')

precos_atualizados = read_data('data/gasolina_precos_atualizada-2004-2021.csv')
precos_atualizados = precos_atualizados.rename(columns = {'Preco_Media': 'Preço',
                                               'Preco_Atualizado': 'Preço atualizado'})

line_chart2 = px.line(precos_atualizados, x='Tempo', y=['Preço',
                                                        'Preço atualizado'])
line_chart2.update_layout(
    title = "Valor de venda da gasolina (2004 - 2021)",
    yaxis_title = "Litro da Gasolina (R$) - Média",
    legend_title = "",
    font = dict(family="Open Sans, monospace", size=12)
)

st.plotly_chart(line_chart2, use_container_width=True)

regioes_2021 = read_data('data/precos_regioes_2021.csv')

bar_chart1 = px.bar(regioes_2021, x='Preco_Media', y='Regiao_Sigla', text_auto='.3s')
bar_chart1.update_layout(
    title = "Valor de venda da gasolina por regiões em 2021",
    xaxis_title = "Litro da Gasolina (R$) - Média",
    yaxis_title = "Regiões",
    font = dict(family="Open Sans, monospace", size=12)
)

st.plotly_chart(bar_chart1, use_container_width=True)

estados_2021 = read_data('data/precos_estados_2021.csv')

bar_chart2 = px.bar(estados_2021, x='Estado_Sigla', y='Preco_Media', text_auto='.3s')
bar_chart2.update_layout(
    title = "Valor de venda da gasolina por estados em 2021",
    xaxis_title = "Estados",
    yaxis_title = "Litro da Gasolina (R$) - Média",
    font = dict(family="Open Sans, monospace", size=12)
)

st.plotly_chart(bar_chart2, use_container_width=True)
