'''
Autor: Matheus Silva
Data: Maio 2022
Este projeto recebe os arquivos csv da database
do governo federal sobre a série histórica do preço
dos combustíveis e edita esses arquivos, agrupando
as informações do valor de venda da gasolina por 
estado ou região.
'''

# importando bibliotecas
import logging
import pandas as pd

# configurando o logging
logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

# lendo csv
def read_data(file_path):
    """Read data from csv.
    Args:
        file_path (str): file path to read.
    Return:
        df_file (DataFrame): returns the file read as a dataframe.
    """
    try:
        df = pd.read_csv(file_path, encoding='unicode_escape', sep = ';')
        return df
    except: # pylint: disable=bare-except
        logging.error("Error read_csv. We were not able to find %s", file_path)
        
# escrevendo csv
def write_data(df, file_path):
    """Write data to csv.
    Args:
        df(dataframe): dataframe to csv.
        file_path (str): file path to write.
    """
    try:
        df.to_csv(file_path, index=False)
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
    precos_combustiveis = read_data(pasta_dados + nome_csv)
    precos_combustiveis = precos_combustiveis.rename(columns={precos_combustiveis.columns[0]: "Regiao - Sigla"})
    
    precos_combustiveis['Valor de Venda'] = precos_combustiveis['Valor de Venda'].str.replace(',','.').astype(float)
    preco_gasolina = precos_combustiveis[precos_combustiveis['Produto'].str.contains('GASOLINA')]
    
    preco_gasolina_estados = preco_gasolina.groupby('Estado - Sigla')[['Valor de Venda']].mean()\
                            .rename(columns = {'Valor de Venda':'Valor de Venda - Media'}).reset_index()
    
    nova_linha = {'Estado - Sigla': 'Total', 'Valor de Venda - Media': preco_gasolina['Valor de Venda'].mean()}
    preco_gasolina_estados = preco_gasolina_estados.append(nova_linha, ignore_index = True)
    
    nome_arquivo = 'preco_gasolina_estados_' + nome_csv[3:]
    
    write_data(preco_gasolina_estados, pasta_destino + nome_arquivo)
    
    return 'Escrevendo ' + nome_arquivo + ' na pasta ' + pasta_destino
    
def sh_regiao(nome_csv, pasta_dados, pasta_destino):
    """Csv file of fuel prices grouped by regions.
    Args:
        nome_csv (str): file to read.
        pasta_dados (str): folder path with the data.
        pasta_destino (str): destination folder path.
    Return:
        string: success message.
    """
    precos_combustiveis = read_data(pasta_dados + nome_csv)
    precos_combustiveis = precos_combustiveis.rename(columns={precos_combustiveis.columns[0]: "Regiao - Sigla"})
    
    precos_combustiveis['Valor de Venda'] = precos_combustiveis['Valor de Venda'].str.replace(',','.').astype(float)
    precos_combustiveis = precos_combustiveis[precos_combustiveis['Produto'].str.contains('GASOLINA')]
    
    preco_gasolina_regioes = precos_combustiveis.groupby('Regiao - Sigla')[['Valor de Venda']].mean()\
                            .rename(columns = {'Valor de Venda':'Valor de Venda - Media'}).reset_index()
    
    nova_linha = {'Regiao - Sigla': 'Total', 'Valor de Venda - Media': precos_combustiveis['Valor de Venda'].mean()}
    preco_gasolina_regioes = preco_gasolina_regioes.append(nova_linha, ignore_index = True)
    
    nome_arquivo = 'preco_gasolina_regioes_' + nome_csv[3:]
    
    write_data(preco_gasolina_regioes, pasta_destino + nome_arquivo)
    
    return 'Escrevendo ' + nome_arquivo + ' na pasta ' + pasta_destino
    
