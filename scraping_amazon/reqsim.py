import requests
from scraping_amazon.payload import GetXpath
from lxml import html
from math import ceil
import re
from scraping_amazon.utils import get_domain,save_data

# Definição dos cabeçalhos para a requisição
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "DNT": "1",

    }
output_file = "output.json"

def fetch_page_source(url, header=HEADERS):
    try:
        print(header)
        response = requests.get(url, headers=header, timeout=10)
        response.raise_for_status()  # Levanta erro para HTTP 4xx e 5xx

        domain, currency = get_domain(url)
        tree = html.fromstring(response.text)  # Converte HTML em objeto lxml

        jsonDom = GetXpath(domain)
        # Extraindo ASIN
        try:
            asin = response.url.split(jsonDom["asin_xpath"])[1].split("?")[0].split("/")[0]
        except (IndexError, KeyError):
            asin = "ASIN não encontrado"

        # Extraindo título
        title = tree.xpath(jsonDom["title_xpath"])
        title = title[0].strip() if title else "Título não encontrado"

        # Extraindo preço principal
        price_whole_element = tree.xpath(jsonDom["price_xpath"])
        price_whole = price_whole_element[0].strip() if price_whole_element else "Preço não encontrado"

        value = re.sub(r'[^\d,]', '', price_whole)
        # Extraindo fração do preço (se aplicável)
        if jsonDom.get("fraction_xpath"):
            price_fraction_element = tree.xpath(jsonDom["fraction_xpath"])
            price_fraction = price_fraction_element[0].strip() if price_fraction_element else "00"
            full_price = f"{value}.{price_fraction.strip()}"
        else:
            full_price = f"{value}"

        # Extraindo percentual de desconto
        discount_element = tree.xpath(jsonDom.get("discount_percentage"))
        if discount_element:
            discount_percentage = discount_element[0].strip()
            if "%" in discount_percentage:
                discount_percentage = discount_percentage.replace("OFF", "").strip()
            else:
                try:
                    discount_re = re.sub(r'[^\d,]', '', discount_percentage).replace(",", ".")
                    price_re = re.sub(r'[^\d,]', '', price_whole).replace(",", ".")
                    discount_percentage = f"-{ceil(((float(discount_re) / float(price_re)) - 1) * 100)}%"
                except ValueError:
                    discount_percentage = "Sem desconto"
        else:
            discount_percentage = "Sem desconto"

        # Criando dicionário com os dados extraídos
        data = {
            "ASIN": asin,
            "Title": title,
            "Price to pay": full_price.replace(",", ".") if full_price else "Preço não encontrado",
            "Discount Percentage": discount_percentage,
            "Domain": domain.upper(),
            "Currency": currency,
        }

        save_data(data,output_file)
        print(f"Data saved: {data}")

        return data

    except requests.RequestException as e:
        return {"Erro": f"Falha na requisição: {e}"}
    except Exception as e:
        return {"Erro": f"Erro inesperado: {e}"}
    
def run_req(urls):
    for url in urls:
        page_content = fetch_page_source(url,header=HEADERS)
        if page_content:
            print("Página carregada com sucesso!")
