"""
Autor: Matheus Silva
Data: Maio 2022
Este projeto recebe os arquivos csv da database
do governo federal sobre a série histórica do preço
dos combustíveis e edita esses arquivos, agrupando
as informações do valor de venda da gasolina por
estado ou região.
"""
# pylint: disable = no-member

# importando bibliotecas
import logging
import pandas as pd

# configurando o logging
logging.basicConfig(
    filename="./results.log",
    level=logging.INFO,
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s")

# lendo csv
def read_data(file_path):
    """Read data from csv.
    Args:
        file_path (str): file path to read.
    Return:
        df_file (DataFrame): returns the file read as a dataframe.
    """
    try:
        df_file = pd.read_csv(file_path, sep = ";", encoding="ISO-8859-1")
        return df_file
    except: # pylint: disable=bare-except
        logging.error("Error read_csv. We were not able to find %s", file_path)
        return pd.Dataframe()

# escrevendo csv
def write_data(df_file, file_path):
    """Write data to csv.
    Args:
        df(dataframe): dataframe to csv.
        file_path (str): file path to write.
    """
    try:
        df_file.to_csv(file_path, index=False)
    except: # pylint: disable=bare-except
        logging.error("Error to_csv. We were not able to find %s", file_path)

def sh_estado(nome_csv, pasta_dados, pasta_destino):
    """Csv file of fuel prices grouped by states.
    Args:
        nome_csv (str): file to read.
        pasta_dados (str): folder path with the data.
        pasta_destino (str): destination folder path.
    Return:
        string: success message.
    """
    df_combustiveis = read_data(pasta_dados + nome_csv)

    df_combustiveis = df_combustiveis.rename(columns={df_combustiveis.columns[0]: "Regiao - Sigla"})

    df_combustiveis["Valor de Venda"] = df_combustiveis["Valor de Venda"]\
                                        .str.replace(",",".").astype(float)
    df_combustiveis = df_combustiveis[df_combustiveis["Produto"] == "GASOLINA"]

    df_estados = df_combustiveis.groupby("Estado - Sigla")[["Valor de Venda"]].mean().round(2)\
                 .reset_index()
    df_estados = df_estados.rename(columns = {"Estado - Sigla": "Estado_Sigla",
                                              "Valor de Venda": "Preco_Media"})

    nova_linha = {"Estado_Sigla": "Total", "Preco_Media":
                  round(df_combustiveis["Valor de Venda"].mean(), 2)}
    df_estados = df_estados.append(nova_linha, ignore_index = True)

    nome_arquivo = "preco_gasolina_estados_" + nome_csv[3:]

    write_data(df_estados, pasta_destino + nome_arquivo)

    return "Escrevendo " + nome_arquivo + " na pasta " + pasta_destino

def sh_regiao(nome_csv, pasta_dados, pasta_destino):
    """Csv file of fuel prices grouped by regions.
    Args:
        nome_csv (str): file to read.
        pasta_dados (str): folder path with the data.
        pasta_destino (str): destination folder path.
    Return:
        string: success message.
    """
    df_combustiveis = read_data(pasta_dados + nome_csv)

    df_combustiveis = df_combustiveis.rename(columns={df_combustiveis.columns[0]: "Regiao - Sigla"})

    df_combustiveis["Valor de Venda"] = df_combustiveis["Valor de Venda"]\
                                        .str.replace(",",".").astype(float)
    df_combustiveis = df_combustiveis[df_combustiveis["Produto"] == "GASOLINA"]

    df_regioes = df_combustiveis.groupby("Regiao - Sigla")[["Valor de Venda"]].mean().round(2)\
                 .reset_index()
    df_regioes = df_regioes.rename(columns = {"Regiao - Sigla": "Regiao_Sigla",
                                              "Valor de Venda": "Preco_Media"})

    nova_linha = {"Regiao_Sigla": "Total", "Preco_Media":
                  round(df_combustiveis["Valor de Venda"].mean(), 2)}
    df_regioes = df_regioes.append(nova_linha, ignore_index = True)

    nome_arquivo = "preco_gasolina_regioes_" + nome_csv[3:]

    write_data(df_regioes, pasta_destino + nome_arquivo)

    return "Escrevendo " + nome_arquivo + " na pasta " + pasta_destino
