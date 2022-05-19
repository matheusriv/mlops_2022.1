# Visualização dos preços da gasolina brasileira entre 2004 e 2021

### Autores: Matheus Silva e Yolanda Dantas

Projeto da disciplina de MLOps da UFRN que tem como objetivo principal colocar em prática o conteúdo referente a Semana 04 da matéria, focado nos princípios de visualização de dados, escrita limpa, documentação, refatoração e análise da qualidade do código através de ferramentas.

<p align="center">
<img src="imagens/gasolina_ajustada_presidentes.png" alt="Gráfico dos preços da gasolina ajustados pela inflação por mandatos presidenciais (2004 - 2021)" style="height: 700px;"/>
</p>

## Requisitos

Verifique se você atende a todos os requisitos a seguir:
* Ter uma máquina com ` Windows | Linux | Mac `.
* Ter o [`Python 3.9`](https://www.python.org/downloads/) instalado na sua máquina.

## Começando

Para começar a usar este projeto, basta clonar o repositório:

Opção HTTP:
```
git clone https://github.com/matheusriv/mlops_2022.1.git
```

Opção SSH:
```
git clone git@github.com:matheusriv/mlops_2022.1.git
```

## 💻 Etapas do Projeto

A semana 04 (https://github.com/ivanovitchm/mlops) do nosso curso teve como objetivo continuar a apresentação sobre outras habilidades relacionadas com o código limpo, nomeadamente: captura e manipulação de erros, testes, registros (logging).

O trabalho como meta explorar tais habilidades juntamente com aquelas já apresentadas na semana 03 (escrita limpa, documentação, refatoração e análise da qualidade do código através de ferramentas).

A primeira parte do trabalho foi adquirir o jupyter notebook (arquivo.ipynb) referente ao Projeto Guiado [Guided Project: Storytelling Data Visualization on Exchange Rates](https://github.com/dataquestio/solutions/blob/master/Mission529Solutions.ipynb). Após isso foi pedido para fazer uma comparação com outras variáveis/séries temporais diferentes daquelas jámencionadas no Dataquest.io e Real/Dolar/Euro/Presidentes.

A variável escolhida foi os preços dos combustíveis brasileiros, em particular a gasolina, analisando os dados de 2004 até 2021 [disponibilizados pelo governo federal](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis).

Com os arquivos csv da série histórica foi feito uma análise prévia e depois um tratamento dos dados, coletando os preços da gasolina por estados e regiões. Esta análise foi feita no notebook sh_estados_regioes.

No notebook gasolina_precos_analise foi utilizado os arquivos gerados de preços por estados e regiões e se calcula o preço médio por ano da gasolina.

Por último foi criado um dashboard com a solução no Streamlit.io para a visualização dos dados e gráficos.

Todos os arquivos .py gerados foram avaliados pela aderência das boas práticas do código limpo executando em terminal o comando [Pylint](https://pylint.pycqa.org/en/latest/), ferramenta de análise para a linguagem de programação Python que analisa código-fonte, bug e qualidade de códigos, seguindo o estilo recomendado pelo PEP 8.

Você pode verificar se todas as técnicas de práticas recomendadas de codificação foram aplicadas executando:
```
pylint app.py
```

Para explorar o dashboard do streamlit é só colocar na linha de comando:
```
streamlit run app.py
```

O comando vai abrir uma nova aba no navegador com o dashboard.

## 💻 Vídeo

Link do vídeo explicando o projeto: https://www.loom.com/share/c0dd02ed76e44d1b94b4eccfd72f8b02
