Projeto de Scraping da Amazon

Descrição

Este projeto realiza consultas de preços em vários sites de e-commerce, incluindo Amazon, Mercado Livre e Kabum. Ele utiliza Selenium e Scrapy para extrair informações sobre produtos, como título, preço, percentual de desconto e ASIN.

Requisitos

Python 3.8+

Google Chrome instalado no sistema

Dependências listadas no requirements.txt

Instalação

Clone este repositório:

git clone https://github.com/seu-usuario/scraping-amazon.git
cd scraping-amazon

Crie um ambiente virtual e ative-o:

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

Instale as dependências:

pip install -r requirements.txt

Como Usar

Executando o Crawler Scrapy

Para rodar o crawler principal:

python -c "from scraping_amazon.spider import run_spider; run_spider()"

Executando a Captura de Preços via Requests

Para rodar a captura via requests:

python -c "from scraping_amazon.reqsim import run_req; run_req(['URL_DO_PRODUTO'])"

Executando a Captura de Preços via Selenium

Para rodar a captura via Selenium:

python -c "from scraping_amazon.another_spider import run_py; run_py(['URL_DO_PRODUTO'])"

Tecnologias Utilizadas

Selenium: Para renderização de páginas dinâmicas.

Scrapy: Para scraping eficiente e estruturado.

Requests & lxml: Para raspagem leve e rápida de conteúdo HTML.

Azure Blob Storage: Para armazenamento dos dados coletados.

Estrutura do Projeto

/
|-- scraping_amazon/
|   |-- spider  # Scrapy Spider
|   |   |-- amazon_spider.py  # Scrapy Spider
|   |-- reqsim.py  # Scraping via requests
|   |-- another_spider.py  # Scraping via Selenium
|   |-- payload.py  # Configurações e XPaths
|   |-- utils.py  # Funções auxiliares
|   |-- pipelines.py  # Função ETL
|   |-- items.py  # Função ETL
|   |-- blob_utils.py  # Função CRUD na cloud
|   |-- setting.py  # Função de configuração do Spider
|   |-- middlewares.py  # Função middlewares
|-- requirements.txt
|-- README.md

Autores

Victor Ivanovich Bormotoff

Pedro Henrique Teixeira

Aviso Legal

Este projeto é apenas para fins educacionais. O uso indevido pode violar os Termos de Serviço dos sites envolvidos.