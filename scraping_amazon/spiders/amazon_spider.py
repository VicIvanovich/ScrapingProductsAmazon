
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options

# Desenvolvido por Victor Ivanovich Bormotoff

# Projeto para realização de consultas de preço no site da amazon

# Disclaimer: É necessário que tenha instalado o Google Chrome no sistema para conseguir rodar o Selenium!

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = [

        # Inserir URLs para realizar a consulta!!

        "https://a.co/d/8VWd5R1"

    ]

    def __init__(self, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)

        options = Options()
        options.add_argument("--headless")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def parse(self, response):

        self.driver.get(response.url)

        time.sleep(3)

        rendered_html = self.driver.page_source

        self.driver.quit()

        response = HtmlResponse(url=response.url, body=rendered_html, encoding='utf-8')

        asin = response.url.split("/dp/")[1].split("?")[0].split("/")[0]

        title = response.xpath('//span[@id="productTitle"]/text()').get()
        if title:
            title = title.strip()

        price_whole = response.xpath('//span[contains(@class, "a-price-whole")]/text()').get().strip() \
            if response.xpath('//span[contains(@class, "a-price-whole")]/text()').get() \
            else "Preço não encontrado"

        price_fraction = response.xpath('//span[contains(@class, "a-price-fraction")]/text()').get().strip() \
            if response.xpath('//span[contains(@class, "a-price-fraction")]/text()').get() \
            else "00"

        full_price = f"${price_whole}.{price_fraction}"

        discount_percentage = response.xpath('//span[contains(@class, "a-size-large") and contains(@class, "savingsPercentage")]/text()').get()
        if discount_percentage:
            discount_percentage = discount_percentage.strip()

        data = {
            "ASIN": asin,
            "Title": title if title else "Título não encontrado",
            "Price to pay (USD)": full_price if full_price else "Preço não encontrado",
            "Discount Percentage": discount_percentage if discount_percentage else "Sem desconto"
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
                    return
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump([data], f, ensure_ascii=False, indent=4)
                self.log(f"Gerando arquivo JSON!")

        self.log(f"Data saved: {data}")

        yield data


process = CrawlerProcess()
process.crawl(AmazonSpider)
process.start()