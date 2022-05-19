"""
Autor: Matheus Silva e Yolanda Dantas
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
from matplotlib import style
import matplotlib.pyplot as plt
#pylint: disable = unused-variable

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

def plot_valor_gasolina():
    """Plota um gráfico line chart de título "Valor de
    venda da gasolina (2004 - 2021) usando plotly.express".
    """
    line_chart1 = px.line(gas_precos, x="Tempo", y="Preco_Media",
                      title = "Valor de venda da gasolina (2004 - 2021)",
                      labels={"Preco_Media": "Litro da gasolina (R$) - Média"})
    st.plotly_chart(line_chart1, use_container_width=True)

def plot_inflacao_gasolina():
    """Plota um gráfico line chart de título "Valor de
    venda e inflação da gasolina (2004 - 2021) usando plotly.express".
    """
    # Create figure with secondary y-axis
    line_chart2 = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    line_chart2.add_trace(
        go.Scatter(x=inflacao_gasolina["Tempo"],
                   y=inflacao_gasolina["ipca_media_semestral"],
                   name="IPCA Média Semestral"),
        secondary_y=False,
    )
    line_chart2.add_trace(
        go.Scatter(x=inflacao_gasolina["Tempo"],
                   y=inflacao_gasolina["ipca_acumulado"],
                   name="IPCA Acumulado"),
        secondary_y=False,
    )
    line_chart2.add_trace(
        go.Scatter(x=gas_precos["Tempo"],
                   y=gas_precos["Preco_Media"],
                   name="Preço da gasolina"),
        secondary_y=True, #second y-axis
    )
    # Add figure title
    line_chart2.update_layout(
        title_text="Valor de venda e inflação da gasolina (2004 - 2021)",
        xaxis_title="Tempo"
    )
    # Set y-axes titles
    line_chart2.update_yaxes(title_text="Inflação porcentagem", secondary_y=False)
    line_chart2.update_yaxes(title_text="Litro da gasolina (R$) - Média", secondary_y=True)
    st.plotly_chart(line_chart2)

def plot_gasolina_ajustada():
    """Plota um gráfico line chart com dados do
    preço da gasolina e valores da inflação usando plotly.express.
    """
    line_chart3 = px.line(precos_atualizados, x="Tempo", y=["Preço sem ajuste",
                                                        "Preço ajustado"])
    line_chart3.update_layout(
        title = "Valor de venda da gasolina (2004 - 2021)",
        yaxis_title = "Litro da Gasolina (R$) - Média",
        legend_title = "",
        legend = dict(yanchor="top",
                      y=0.99,
                      xanchor="left",
                      x=0.40)
    )
    st.plotly_chart(line_chart3, use_container_width=True)

def plot_inflacao_presidentes():
    """Plota um gráfico line chart da inflação acumulada
    com mandatos presidenciais usando matplotlib.
    """
    lula = inflacao_gasolina[(inflacao_gasolina["Tempo"] >= "2003-01-01") &
                         (inflacao_gasolina["Tempo"] <= "2010-12-01")]
    dilma = inflacao_gasolina[(inflacao_gasolina["Tempo"] >= "2010-12-01") &
                              (inflacao_gasolina["Tempo"] <= "2016-06-01")]
    temer = inflacao_gasolina[(inflacao_gasolina["Tempo"] >= "2016-06-01") &
                              (inflacao_gasolina["Tempo"] <= "2018-12-01")]
    bolsonaro = inflacao_gasolina[(inflacao_gasolina["Tempo"] >= "2018-12-01") &
                                  (inflacao_gasolina["Tempo"] <= "2021-12-01")]

    # Setting figure size
    plt.figure(figsize=(8,6))

    # Plotting the inflaction variation by Presidents
    plt.plot(lula["Tempo"], lula["ipca_acumulado"],
             label="Lula", color="#49be25")
    plt.plot(dilma["Tempo"], dilma["ipca_acumulado"],
             label="Dilma", color="#be4d25")
    plt.plot(temer["Tempo"], temer["ipca_acumulado"],
             label="Temer", color="#9925be")
    plt.plot(bolsonaro["Tempo"], bolsonaro["ipca_acumulado"],
             label="Bolsonaro", color="#2596be")

    # habilitando as legendas
    plt.legend()
    # definindo titulo e sub-titulo
    plt.text(731516.0, 60, ""*22+"""Variação da inflação acumulada (2006-2021)""",
             fontsize=14, weight="bold")
    plt.text(731000.0, 55,
             "Governos Lula(2004-2010), Dilma(2011-2016.1), Temer(2016.2-2018)\
              e Bolsonaro(2019-2021)",
             fontsize=10)
    #definindo footer
    plt.text(731000.0, -21, "Autoria: Yolanda" + " "*110 + "Fonte: IBGE",
             color="#f0f0f0",
             backgroundcolor="#4d4d4d",
             size=11)

    plt.savefig("imagens/inflacao_gasolina.png", format="png")

    st.image("imagens/inflacao_gasolina.png")

def plot_gasolina_ajustada_presidentes():
    """Plota um gráfico line chart dos preços da gasolina
    ajustados pela inflação por mandatos presidenciais usando matplotlib.
    """
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, ncols=1, figsize=(6,8))
    axes = [ax1, ax2, ax3, ax4]

    for ax in axes:
        ax.plot(precos_atualizados["Tempo"], precos_atualizados["Preco_Atualizado"],
                color="#af0b1e", alpha=0.1)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.axhline(5, xmin=0.0, xmax=1, color="#625d56", linewidth=(0.5),
                   alpha=0.2, linestyle="dashdot")
        ax.axhline(6, xmin=0.0, xmax=1, color="#625d56", linewidth=(0.5),
                   alpha=0.2, linestyle="dashdot")
        ax.grid(False)
        ax.tick_params(bottom=0, left=0)
        for location in ["left", "right", "top", "bottom"]:
            ax.spines[location].set_visible(False)

    lula_2 = precos_atualizados[(precos_atualizados["Tempo"] >= "2003-01-01") &
                                (precos_atualizados["Tempo"] <= "2010-12-01")]
    dilma_2 = precos_atualizados[(precos_atualizados["Tempo"] >= "2010-12-01") &
                                 (precos_atualizados["Tempo"] <= "2016-06-01")]
    temer_2 = precos_atualizados[(precos_atualizados["Tempo"] >= "2016-06-01") &
                                 (precos_atualizados["Tempo"] <= "2018-12-01")]
    bolsonaro_2 = precos_atualizados[(inflacao_gasolina["Tempo"] >= "2018-12-01") &
                                     (precos_atualizados["Tempo"] <= "2021-12-01")]

    #Lula"s chart elements
    ax1.plot(lula_2["Tempo"], lula_2["Preco_Atualizado"], label="Lula", color="#49be25")
    ax1.text(0.15, 0.95, "R$6,41", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, fontsize=12, color="#49be25")
    ax1.text(0.37, 0.14, "R$5,23", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, fontsize=12, color="#49be25")
    ax1.text(-0.05, 0.15, "R$5", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, fontsize=12, color="#625d56", alpha=0.2)
    ax1.text(-0.05, 0.65, "R$6", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, fontsize=12, color="#625d56", alpha=0.2)
    ax1.text(0.55, 0.4, "Governo Lula", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, fontsize=12, color="#49be25")
    ax1.text(0.05, 0, "2004", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, fontsize=12, color="#625d56", alpha=0.2)
    ax1.text(0.97, 0, "2021", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, fontsize=12, color="#625d56", alpha=0.2)

    #Dilmas"s chart elements
    ax2.plot(dilma_2["Tempo"], dilma_2["Preco_Atualizado"],label="Dilma", color="#be4d25")
    ax2.text(0.58, -0.1, "R$4,77", horizontalalignment="center", verticalalignment="center",
             transform=ax2.transAxes, fontsize=12, color="#be4d25")
    ax2.text(0.40, 0.14, "R$5,30", horizontalalignment="center", verticalalignment="center",
             transform=ax2.transAxes, fontsize=12, color="#be4d25")
    ax2.text(0.55, 0.4, "Governo Dilma", horizontalalignment="center", verticalalignment="center",
             transform=ax2.transAxes, fontsize=12, color="#be4d25")

    #Temer"s chart elements
    ax3.plot(temer_2["Tempo"], temer_2["Preco_Atualizado"], label="Temer", color="#9925be")
    ax3.text(0.71, 0.0, "R$4,90", horizontalalignment="center", verticalalignment="center",
             transform=ax3.transAxes, fontsize=12, color="#9925be")
    ax3.text(0.79, 0.62, "R$5,74", horizontalalignment="center", verticalalignment="center",
             transform=ax3.transAxes, fontsize=12, color="#9925be")
    ax3.text(0.55, 0.4, "Governo Temer", horizontalalignment="center", verticalalignment="center",
             transform=ax3.transAxes, fontsize=12, color="#9925be")

    #Bolsonaro"s chart elements
    ax4.plot(bolsonaro_2["Tempo"], bolsonaro_2["Preco_Atualizado"],
             label="Bolsonaro", color="#2596be")
    ax4.text(0.94, 1.02, "R$6,59", horizontalalignment="center", verticalalignment="center",
             transform=ax4.transAxes, fontsize=12, color="#2596be")
    ax4.text(0.9, 0.04, "R$4,98", horizontalalignment="center", verticalalignment="center",
             transform=ax4.transAxes, fontsize=12, color="#2596be")
    ax4.text(0.55, 0.4, "Governo Bolsonaro", horizontalalignment="center",
             verticalalignment="center", transform=ax4.transAxes, fontsize=12, color="#2596be")

    # Title and subtitle
    ax4.text(0.48, 1.4, "Preço da gasolina ajustado pela inflação do período",
             horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, size=14, weight="bold")
    ax4.text(0.48, 1.2, "Máximo e mínimo em cada governo entre 2004 e 2021",
             horizontalalignment="center", verticalalignment="center", transform=ax1.transAxes)

    # Credits
    ax4.text(0.48, -0.2, "Autores: Matheus Silva e Yolanda Dantas" + " "*20 + "Fonte: IBGE, ANP",
             horizontalalignment="center", verticalalignment="center",
             transform=ax4.transAxes, color = "#f0f0f0", backgroundcolor = "#4d4d4d", size=12)

    plt.savefig("imagens/gasolina_ajustada_presidentes.png", format="png")

    st.image("imagens/gasolina_ajustada_presidentes.png")

def plot_meta_inflacao():
    """Plota um gráfico line chart da inflação acumulada
    e preços da gasolina usando matplotlib.
    """
    fig, ax1 = plt.subplots(figsize=(10,6))

    ax1.plot(inflacao_gasolina["Tempo"], inflacao_gasolina["ipca_acumulado"], color="#db4b26")
    ax1.yaxis.set_ticklabels([])
    ax1.grid(False)

    #Inflation data (sellected area between 0 and 4.5%)
    ax1.axhline(2.25, xmin=0.0, xmax=1, color="#db4b26", alpha=0.1, linewidth=(30))
    ax1.text(0.27, 0.32, "Meta de inflação", horizontalalignment="center",
             verticalalignment="center", transform=ax1.transAxes, fontsize=12, weight="bold",
             color="#db4b26", alpha=0.4)
    ax1.text(-0.03, 0.22, "0%", horizontalalignment="center",verticalalignment="center",
             transform=ax1.transAxes, fontsize=14, color="#db4b26", alpha=0.4)
    ax1.text(-0.03, 0.3, "4,5%", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, fontsize=14, color="#db4b26", alpha=0.4)
    ax1.text(0.08, 0.48, "14,64%", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, color="#db4b26", fontsize=12, weight="bold")
    ax1.text(0.65, 0.565, "20,10%", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, color="#db4b26", fontsize=12, weight="bold")
    ax1.text(0.847, 0.11, "-11,88%", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, color="#db4b26", fontsize=12, weight="bold", rotation=-79)
    ax1.text(0.968, 0.88, "47,49%", horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, color="#db4b26", fontsize=12, weight="bold", rotation=83)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.plot(inflacao_gasolina["Tempo"], gas_precos["Preco_Media"], color="#0a5891")
    ax2.grid(False)
    ax2.yaxis.set_ticklabels([])
    ax2.tick_params(axis="x", colors="#625d56")

    #Gasoline data
    ax2.text(0.03, 0.1, "R$2,03", horizontalalignment="center", verticalalignment="center",
            transform=ax2.transAxes, color="#0a5891", fontsize=12, weight="bold")
    ax2.text(0.8, 0.61, "R$4,58", horizontalalignment="center", verticalalignment="center",
            transform=ax2.transAxes, color="#0a5891", fontsize=12, weight="bold")
    ax2.text(0.925, 0.88, "R$6,34", horizontalalignment="center", verticalalignment="center",
            transform=ax2.transAxes, color="#0a5891", fontsize=12, weight="bold", rotation=74)

    # Title and subtitle
    ax2.text(0.49, 1.1, "Gasolina inflaciona e tem aumento abrupto de preços no último ano",
             horizontalalignment="center", verticalalignment="center",
             transform=ax1.transAxes, size=17, weight="bold")
    ax2.text(0.49, 1.05, "Preço médio da gasolina e inflação acumulada por ano entre 2004 e 2021",
             horizontalalignment="center", verticalalignment="center", transform=ax1.transAxes)

    # Credits
    ax2.text(0.48, -0.1, "Autores: Matheus Silva e Yolanda Dantas" +
             " "*90 + "Fonte: IBGE, ANP", horizontalalignment="center",
             verticalalignment="center", transform=ax1.transAxes,
             color = "#f0f0f0", backgroundcolor = "#4d4d4d", size=12)

    fig.tight_layout()

    plt.savefig("imagens/meta_inflacao_precos.png", format="png")

    st.image("imagens/meta_inflacao_precos.png")

def plot_regioes_estados_2021():
    """Plota gráficos de barras com valores da gasolina
    por região e estado usando plotly.express.
    """
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

# Setting graph style
style.use("fivethirtyeight")

st.title("Analisando o preço da gasolina brasileira (2004 - 2021)")

st.subheader("A Streamlit web app by Matheus Silva and Yolanda Dantas")

st.markdown("Este projeto, apresentado na disciplina de Mlops da UFRN, visa analisar o \
            comportamento do preço da gasolina brasileira em relação à inflação. Como base, \
            utilizados dados disponibilizados pelo governo federal (ANP) na \
            [série histórica de preços de combustíveis](\
            https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis)\
            que vai de 2004 até 2021. Cada ano possui dois arquivos, para cada semestre. \
            Exemplo do arquivo csv do segundo semestre de 2021:")

st.caption("ca_2021_02.head()")

ca_2021_02 = read_data("data/serie_historica_combustiveis/ca-2021-02.csv")

# Mostrando head do arquivo ca_2021_02
st.dataframe(ca_2021_02.head())

st.markdown("Após o download dos arquivos csv foi feito um tratamento de dados\
            coletando a média do preço da gasolina anual entre 2004 e 2021.")

gas_precos = read_data("data/gasolina_precos-2004-2021.csv")

# Mostrando o arquivo gasolina_precos-2004-2021
st.dataframe(gas_precos)

st.markdown("Dataframe em gráfico de linha:")

# Grafico: Valor de venda da gasolina (2004 - 2021)
plot_valor_gasolina()

st.markdown("Já os dados da [série histórica da inflação (IPCA) para gasolina](\
            https://sidra.ibge.gov.br/Busca?q=ipca) foram obtidos através do IBGE, \
            que calcula os índides de inflação mensalmente\
            (tabelas 655, 657, 2938, 1419 e 7060). \
            Abaixo podemos visualizar parte do arquivo csv gerado após a junção das \
            tabelas e optenção de médias semestrais no excel:")

inflacao_gasolina = read_data("data/inflacao-semestral-gasolina-2004-2021.csv")

# Mostrando o arquivo inflacao-semestral-gasolina-2004-2021
st.dataframe(inflacao_gasolina)

# Grafico: Valor de venda e inflação da gasolina (2004 - 2021)
plot_inflacao_gasolina()

st.markdown("É possível ver os dados da inflação acumulada com destaques dos presidentes\
            brasileiros:")

inflacao_gasolina["Tempo"] = pd.to_datetime(inflacao_gasolina["Tempo"])

# Grafico: Inflação acumulada e mandatos presidenciais
plot_inflacao_presidentes()

# Grafico: Inflação e preços da gasolina
plot_meta_inflacao()

st.markdown("Com o preço da gasolina foi possível fazer a atualização dos preços\
            pela variação do [Índice de Preços ao Consumidor Amplo (IPCA)](\
            https://www.ibge.gov.br/explica/inflacao.php) de abril de 2022.")

precos_atualizados = read_data("data/gasolina_precos_atualizada-2004-2021.csv")
precos_atualizados = precos_atualizados.rename(columns = {"Preco_Media": "Preço sem ajuste",
                                               "Preco_Atualizado": "Preço ajustado"})

# Grafico: Preços da gasolina ajustados pela inflação
plot_gasolina_ajustada()

precos_atualizados = precos_atualizados.rename(columns = {"Preço sem ajuste": "Preco_Media",
                                               "Preço ajustado": "Preco_Atualizado"})
precos_atualizados["Tempo"] = pd.to_datetime(precos_atualizados["Tempo"])

# Grafico: Preços da gasolina ajustados pela inflação e mandatos presidenciais
plot_gasolina_ajustada_presidentes()

st.markdown("Por último, vamos visualizar os dados de preço de 2021 por regiões e estados:")

# Graficos valor de venda da gasolina por estados e regiões 2021
plot_regioes_estados_2021()
