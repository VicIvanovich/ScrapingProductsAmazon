import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from scrapy.http import HtmlResponse
import scrapy
from selenium.webdriver.chrome.options import Options
from scraping_amazon.blob_utils import upload_file_to_blob
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse
from ..payload import GetDomain
import re
from math import ceil
# Desenvolvido por Victor Ivanovich Bormotoff e Pedro Henrique Teixeira

# Projeto para realização de consultas de preço no site da amazon

# Disclaimer: É necessário que tenha instalado o Google Chrome no sistema para conseguir rodar o Selenium!


def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    
    currency = "BRL" if '.br' in domain.lower() else "USD"
    domain = domain.split('.')[0]
    

    return domain,currency


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com","amazon.com.br", "mercadolivre.com", "kabum.com.br"]
    start_urls = [

        # Inserir URLs para realizar a consulta!!

        "https://www.kabum.com.br/produto/385191/console-nintendo-switch-joy-con-neon-mario-kart-8-deluxe-3-meses-de-assinatura-nintendo-switch-online-azul-e-vermelho-hbdskabl2?awc=17729_1737135620_6fbeefe3ace3c0c9e0fda1b4f4fb4062&sn=1&utm_source=AWIN&utm_medium=AFILIADOS&utm_campaign=fevereiro24&utm_content=i8mHpW6AWECTVWXKusSESg:0001010111111111001110&utm_term=402367"

    ]

    def __init__(self, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def parse(self, response):

        self.driver.get(response.url)

        time.sleep(3)

        rendered_html = self.driver.page_source

        response = HtmlResponse(url=response.url, body=rendered_html, encoding='utf-8')

        domain,currency = get_domain(response.url)

        jsonDom = GetDomain(domain)

        #print(jsonDom)


        asin = response.url.split(jsonDom["asin_xpath"])[1].split("?")[0].split("/")[0]

        title = response.xpath(jsonDom["title_xpath"]).get()
        if title:
            title = title.strip()

        price_whole = response.xpath(jsonDom["price_xpath"]).get().strip() \
            if response.xpath(jsonDom["price_xpath"]).get() \
            else "Preço não encontrado"

        if jsonDom.get("fraction_xpath"):
            price_fraction = response.xpath(jsonDom.get("fraction_xpath")).get()
            full_price = f"{price_whole}.{price_fraction.strip()}"
        else:
            value = re.sub(r'[^\d,]', '', price_whole)
            full_price = f"{value}"

        discount_percentage = response.xpath(jsonDom.get("discount_percentage")).get()
        if discount_percentage:
            if "%" in discount_percentage:
                discount_percentage = discount_percentage.strip()
            else:
                discount_re = re.sub(r'[^\d,]', '', discount_percentage).replace(",", ".")
                price_re = re.sub(r'[^\d,]', '', price_whole).replace(",", ".")
                discount_percentage = f"-{ceil(((float(discount_re) / float(price_re)) - 1) * 100)}%"

        data = {
            # "Domain": domain if domain else "Não identificado o domínio",
            "ASIN": asin,
            "Title": title if title else "Título não encontrado",
            "Price to pay": full_price.replace(",", ".") if full_price else "Preço não encontrado",
            "Discount Percentage": discount_percentage if discount_percentage else "Sem desconto",
            "Domain": domain.upper(),
            "Currency": currency,
        }


        output_file = "output.json"

        if os.path.exists(output_file):
            with open(output_file, "r+", encoding="utf-8") as f:
                file_contents = f.read().strip()

                if not file_contents:
                    self.log("Arquivo JSON vazio. Inicializando como uma lista vazia")
                    file_data = []
                else:
                    try:
                        file_data = json.loads(file_contents)
                    except json.JSONDecodeError as e:
                        self.log(f"Erro ao decodificar JSON: {e}. Corrigindo arquivo...")
                        file_data = []
                        f.truncate(0)
                if not any(item['ASIN'] == data['ASIN'] for item in file_data):
                    file_data.append(data)

                    f.seek(0)
                    json.dump(file_data, f, ensure_ascii=False, indent=4)
                else:
                    self.log(f"Produto duplicado encontrado (ASIN {data['ASIN']}): {data['Title']}")
                    return None
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump([data], f, ensure_ascii=False, indent=4)
                self.log(f"Gerando arquivo JSON!")

        self.log(f"Data saved: {data}")

        upload_file_to_blob(output_file)

        yield data


def run_spider():
    process = CrawlerProcess()
    process.crawl(AmazonSpider)
    process.start()