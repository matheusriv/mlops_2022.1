"""
Autor: Matheus Silva
Data: Maio 2022
Este projeto recebe uma url do site do governo
federal sobre a série histórica do preço dos
combustíveis e baixa esses arquivos na pasta
de destino explicitada.
"""
#pylint: disable = invalid-name
import shutil
import requests

def download_file(web_address, path):
    """Download a file.
    Args:
        web_address (str): file url.
        path (str): file destination folder.
    Return:
        local_filename (str): file name.
    """
    local_filename = web_address.split("/")[-1]
    with requests.get(web_address, stream=True) as r:
        with open(path + local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename

url = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/"
lista = ["ca-2004-01.csv", "ca-2004-02.csv", "ca-2005-01.csv", "ca-2005-02.csv",
         "ca-2006-01.csv", "ca-2006-02.csv", "ca-2007-01.csv", "ca-2007-02.csv",
         "ca-2008-01.csv", "ca-2008-02.csv", "ca-2009-01.csv", "ca-2009-02.csv",
         "ca-2010-01.csv", "ca-2010-02.csv", "ca-2011-01.csv", "ca-2011-02.csv",
         "ca-2012-01.csv", "ca-2012-02.csv", "ca-2013-01.csv", "ca-2013-02.csv",
         "ca-2014-01.csv", "ca-2014-02.csv", "ca-2015-01.csv", "ca-2015-02.csv",
         "ca-2016-01.csv", "ca-2016-02.csv", "ca-2017-01.csv", "ca-2017-02.csv",
         "ca-2018-01.csv", "ca-2018-02.csv", "ca-2019-01.csv", "ca-2019-02.csv",
         "ca-2020-01.csv", "ca-2020-02.csv", "ca-2021-01.csv", "ca-2021-02.csv"]

pasta_destino = "data/serie_historica_combustiveis/"

for arquivo in lista:
    nome_arquivo = download_file(url + arquivo, pasta_destino)
    print(nome_arquivo + " baixado na pasta " + pasta_destino)
