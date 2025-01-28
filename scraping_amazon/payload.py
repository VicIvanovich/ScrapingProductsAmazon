

def GetDomain(domain):
    jsonDom = {
            "amazon": {
                "price_xpath": "//span[contains(@class, 'a-price-whole')]/text()",
                "title_xpath": "//span[@id='productTitle']/text()",
                "fraction_xpath": "//span[contains(@class, 'a-price-fraction')]/text()",
                "discount_percentage":"//span[contains(@class, 'a-size-large') and contains(@class, 'savingsPercentage')]/text()",
                "asin_xpath": "/dp/"
            },
            "kabum": {
                "price_xpath": "//*[@id='blocoValores']//h4/text()",
                "title_xpath": "//h1[contains(@class, 'sc-58b2114e-6')]/text()",
                "discount_percentage": "//span[contains(@class, 'oldPrice')]/text()",
                "asin_xpath": "/produto/"
            },
            "magazineluiza": {
                "price_xpath": "//p[@data-testid='price-value']/text()",
                "title_xpath": "//h1[@data-testid='heading-product-title']/text()",
                "discount_percentage": "//p[contains(@data-testid, 'price-original')]/text()",
                "asin_xpath": "/p/"
            }

        }
    return jsonDom.get(domain)

