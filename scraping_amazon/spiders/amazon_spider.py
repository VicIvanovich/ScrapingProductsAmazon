from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from scrapy.http import HtmlResponse
import scrapy
from selenium.webdriver.chrome.options import Options
from scraping_amazon.blob_utils import upload_file_to_blob
from scrapy.crawler import CrawlerProcess
from scraping_amazon.payload import GetXpath,selectUrls
import re
from math import ceil
from scrapy.utils.project import get_project_settings
from scraping_amazon.another_spider import run_py
from scraping_amazon.reqsim import run_req
from scraping_amazon.utils import get_domain,save_data
# Desenvolvido por Victor Ivanovich Bormotoff e Pedro Henrique Teixeira

# Projeto para realização de consultas de preço no site da amazon

# Disclaimer: É necessário que tenha instalado o Google Chrome no sistema para conseguir rodar o Selenium!
output_file = "output.json"

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com","amazon.com.br", "mercadolivre.com", "kabum.com.br","www.mercadolivre.com.br"]
    start_urls = selectUrls("AmazonSpider")

    def __init__(self, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def parse(self, response):
        
        self.driver.get(response.url)

        time.sleep(5)
            
        rendered_html = self.driver.page_source

        response = HtmlResponse(url=response.url, body=rendered_html, encoding='utf-8')

        domain,currency = get_domain(response.url)
        
        jsonDom = GetXpath(domain)

        asin = response.url.split(jsonDom["asin_xpath"])[1].split("?")[0].split("/")[0]

        title = response.xpath(jsonDom["title_xpath"]).get()
        if title:
            title = title.strip()

        price_whole = response.xpath(jsonDom["price_xpath"]).get().strip() \
            if response.xpath(jsonDom["price_xpath"]).get() \
            else "Preço não encontrado"

        value = re.sub(r'[^\d,]', '', price_whole)

        if jsonDom.get("fraction_xpath"):
            price_fraction = response.xpath(jsonDom.get("fraction_xpath")).get()
            full_price = f"{value}.{price_fraction.strip()}"
        else:
            full_price = f"{value}"

        discount_percentage = response.xpath(jsonDom.get("discount_percentage")).get()

        if discount_percentage:
            if "%" in discount_percentage:
                discount_percentage = discount_percentage.replace("OFF","").strip()
            else:
                discount_re = re.sub(r'[^\d,]', '', discount_percentage).replace(",", ".")
                price_re = re.sub(r'[^\d,]', '', price_whole)
                discount_percentage = f"-{ceil(((float(discount_re) / float(price_re)) - 1) * 100)}%"

        data = {

            "ASIN": asin,
            "Title": title if title else "Título não encontrado",
            "Price to pay": full_price.replace(",", ".") if full_price else "Preço não encontrado",
            "Discount Percentage": discount_percentage if discount_percentage else "Sem desconto",
            "Domain": domain.upper() if domain else "Não identificado o domínio",
            "Currency": currency,
        }

        

        save_data(data,output_file)
        self.log(f"Data saved: {data}")

        #upload_file_to_blob(output_file)

        yield data
        
def run_spider():
    settings = get_project_settings().copy()  # Converte Settings para dict
    process = CrawlerProcess(settings)
    process.crawl(AmazonSpider)
    process.start()
    run_py(selectUrls("AnotherSpider"))
    run_req(selectUrls("reqsim"))
    upload_file_to_blob(output_file)
