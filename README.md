# Scraping Amazon - Projeto Scrapy

## Descrição
Este projeto utiliza o framework Scrapy para realizar web scraping na Amazon, coletando informações de produtos. O projeto está configurado para respeitar práticas que reduzem bloqueios, como o uso de User-Agents dinâmicos e proxies rotativos.

## Requisitos

- Python 3.8+
- Google Chrome instalado no sistema
- Dependências listadas no `requirements.txt`

- ## Tecnologias Utilizadas
- **Selenium**: Para renderização de páginas dinâmicas.
- **Scrapy**: Para scraping eficiente e estruturado.
- **Requests & lxml**: Para raspagem leve e rápida de conteúdo HTML.
- **Azure Blob Storage**: Para armazenamento dos dados coletados.

## Dependências
- `Scrapy`
- `fake_useragent`
- `scrapy_user_agents`
- `rotating_proxies`
  
## Instalação e Execução
1. Clone o repositório:
   ```sh
   git clone https://github.com/VicIvanovich/scraping_amazon.git
   cd scraping_amazon
   ```
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
   
## Como Usar
### Executando Direto pela main
Para rodar o crawler principal:
```sh
python main.py
```

### Executando o Crawler Scrapy
Para rodar o crawler principal:
```sh
python -c "from scraping_amazon.spider import run_spider; run_spider()"
```

### Executando a Captura de Preços via Requests
Para rodar a captura via requests:
```sh
python -c "from scraping_amazon.reqsim import run_req; run_req(['URL_DO_PRODUTO'])"
```

### Executando a Captura de Preços via Selenium
Para rodar a captura via Selenium:
```sh
python -c "from scraping_amazon.another_spider import run_py; run_py(['URL_DO_PRODUTO'])"
```

## Configuração do Scrapy
### Definições Gerais
- **BOT_NAME:** `acesso_amazon`
- **SPIDER_MODULES:** `scraping_amazon.spiders`
- **NEWSPIDER_MODULE:** `scraping_amazon.spiders`
- **ROBOTSTXT_OBEY:** `False`
- **LOG_INFO:** `INFO`
- **CONCURRENT_REQUESTS:** `1`
- **DOWNLOAD_DELAY:** `5` segundos

### Headers Padrão
O projeto usa um User-Agent de um dispositivo iPhone para reduzir bloqueios:
```python
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
```

### Middlewares Ativados
O projeto conta com middlewares para alterar o User-Agent, rodar proxies rotativos e lidar com redirecionamentos:
```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'scraping_amazon.middlewares.RedirectMiddleware': 543
}
```

### AutoThrottle
O AutoThrottle está ativado para adaptar o ritmo de scraping conforme a resposta do servidor:
```python
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
```

### Outras Configurações
- **HTTPERROR_ALLOWED_CODES:** `[403]`
- **TWISTED_REACTOR:** `twisted.internet.asyncioreactor.AsyncioSelectorReactor`
- **FEED_EXPORT_ENCODING:** `utf-8`





## Estrutura do Projeto
```
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
```

## Autores
- Victor Ivanovich Bormotoff
- Pedro Henrique Teixeira

## Aviso Legal
Este projeto é apenas para fins educacionais. O uso indevido pode violar os Termos de Serviço dos sites envolvidos.

