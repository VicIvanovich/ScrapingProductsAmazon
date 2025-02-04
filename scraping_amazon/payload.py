

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
                "price_xpath": "//*[@id='__next']//section[7]//div[6]//p/text()",
                "title_xpath": "//*[@id='__next']//section[5]//h1/text()",
                "discount_percentage": "//*[@id='product']//section//div[5]//p[1]/text()",
                "asin_xpath": "/p/"
            }

        }
    return jsonDom.get(domain)

