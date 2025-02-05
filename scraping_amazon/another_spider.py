#import undetected_chromedriver as uc
import time
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from scraping_amazon.payload import GetXpath
import re
from math import ceil
from scraping_amazon.utils import get_domain,save_data


options = Options()
options.add_argument("--headless")  # Remova se quiser ver o navegador aberto
options.add_argument("--disable-blink-features=AutomationControlled")  # Evita detecção
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

output_file = "output.json"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def fetch_page_source(url):
    try:
        driver.get(url)
        time.sleep(5)

        html_content = driver.page_source

        response = HtmlResponse(url=url, body=html_content, encoding='utf-8')

        domain,currency = get_domain(response.url)
        
        jsonDom = GetXpath(domain)
        # Exemplo: obter o título da página
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
                discount_percentage = discount_percentage.replace("OFF","").replace("Baixou","").strip()
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

        save_data(data,output_file)
        print(f"Data saved: {data}")

        #upload_file_to_blob(output_file)

    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return None

def run_py(urls):
    for url in urls:
        page_content = fetch_page_source(url)
        if page_content:
            print("Página carregada com sucesso!")

    driver.quit()
