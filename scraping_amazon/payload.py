

def selectUrls(Bot):
    dctList = {
        "AmazonSpider": [
                        "https://www.mercadolivre.com.br/samsung-galaxy-a55-5g-dual-sim-256-gb-azul-celeste-8-gb-ram/p/MLB34731719#polycard_client=recommendations_home_navigation-recommendations&reco_backend=machinalis-homes-univb-equivalent-offer&wid=MLB3837910201&reco_client=home_navigation-recommendations&reco_item_pos=9&reco_backend_type=function&reco_id=16181c70-5e0e-44cb-b224-c0b924fa54a4&sid=recos&c_id=/home/navigation-recommendations/element&c_uid=9d633a92-6229-4f4a-8d3d-5a6dc4ba9856",
                         #"https://www.mercadolivre.com.br/samsung-galaxy-a55-5g-dual-sim-256-gb-azul-celeste-8-gb-ram/p/MLB34731719#polycard_client=recommendations_home_navigation-recommendations&reco_backend=machinalis-homes-univb-equivalent-offer&wid=MLB3837910201&reco_client=home_navigation-recommendations&reco_item_pos=9&reco_backend_type=function&reco_id=16181c70-5e0e-44cb-b224-c0b924fa54a4&sid=recos&c_id=/home/navigation-recommendations/element&c_uid=9d633a92-6229-4f4a-8d3d-5a6dc4ba9856",
                         #"https://www.kabum.com.br/produto/475647/placa-de-video-rx-7600-gaming-oc-8g-amd-radeon-gigabyte-8gb-gddr6-128bits-rgb-gv-r76gaming-oc-8gd"
                         ],
        "AnotherSpider": [
                          #"https://www.pontofrio.com.br/apple-iphone-15-128gb-preto/p/55065306",
                          #"https://www.casasbahia.com.br/mangueira-especial-tramontina-flex-com-engate-rosqueado-e-esguicho-15-metros/p/175513?utm_source=Google&utm_medium=BuscaOrganica&utm_campaign=DescontoEspecial",
                          #"https://www.mercadolivre.com.br/samsung-galaxy-a55-5g-dual-sim-256-gb-azul-celeste-8-gb-ram/p/MLB34731719#polycard_client=recommendations_home_navigation-recommendations&reco_backend=machinalis-homes-univb-equivalent-offer&wid=MLB3837910201&reco_client=home_navigation-recommendations&reco_item_pos=9&reco_backend_type=function&reco_id=16181c70-5e0e-44cb-b224-c0b924fa54a4&sid=recos&c_id=/home/navigation-recommendations/element&c_uid=9d633a92-6229-4f4a-8d3d-5a6dc4ba9856"
                        ],
        "reqsim":       [
            
                          "https://www.mercadolivre.com.br/celular-samsung-galaxy-a35-5g-cmera-tripla-ate-50mp-tela-66-128gb-rosa/p/MLB34729763#polycard_client=recommendations_home_navigation-recommendations&reco_backend=machinalis-homes-univb-equivalent-offer&wid=MLB3663500281&reco_client=home_navigation-recommendations&reco_item_pos=1&reco_backend_type=function&reco_id=6f681f85-cd4a-4765-9c1f-beb897583b7c&sid=recos&c_id=/home/navigation-recommendations/element&c_uid=63851c63-5382-49b4-9435-67e5ac98ab10"
                        ]

    }
    return dctList.get(Bot)

def GetXpath(domain):
    jsonDom = {
            "amazon": {
                "price_xpath": "//div[contains(@class, 'a-section a-spacing-none a-padding-none')]//span[contains(@class, 'a-price-whole')]/text()",
                "title_xpath": "//span[@id='productTitle']/text()",
                "fraction_xpath": "//div[contains(@class, 'a-section a-spacing-none a-padding-none')]//span[contains(@class, 'a-price-fraction')]/text()",
                "discount_percentage":"//span[contains(@class, 'a-size-large') and contains(@class, 'savingsPercentage')]/text()",
                "asin_xpath": "/dp/"
            },
            "kabum": {
                "price_xpath": "//*[@id='blocoValores']//h4/text()",
                "title_xpath": "/html/head/title/text()",#"title_xpath": "//h1[contains(@class, 'sc-58b2114e-6')]/text()",
                "discount_percentage": "//span[contains(@class, 'oldPrice')]/text()",
                "asin_xpath": "/produto/"
            },
            "pontofrio": {
                "price_xpath": "//*[@id='product-price']/span[2]/text()",
                "title_xpath": "/html/head/title/text()",
                "discount_percentage": "//*[@id='__next']/div/div[5]/div[2]/div/span/span[2]/text()",
                "asin_xpath": "/p/"
            },
            
            "magazineluiza": {
                "price_xpath": "//p[@data-testid='price-value']/text()",
                "title_xpath": "/html/head/title/text()",#"title_xpath": "//*[@id='__next']//section[5]//h1/text()",
                "discount_percentage": "//p[@data-testid='price-original']/text()",
                "asin_xpath": "/p/"
            },
            "casasbahia": {
                "price_xpath": "//*[@id='product-price']/span[2]/text()",
                "title_xpath": "/html/head/title/text()",#"title_xpath": "//*[@id='__next']/div/div[2]/div[1]/div/h1/text()",
                "discount_percentage": "//*[@id='product']//section//div[5]//p[1]/text()",
                "asin_xpath": "/p/"
            },
            "mercadolivre": {
                "price_xpath": "//div[contains(@class, 'ui-pdp-price__second-line')]//span[contains(@class, 'andes-money-amount__fraction')]/text()",
                "fraction_xpath": "//div[contains(@class, 'ui-pdp-price__second-line')]//span[contains(@class, 'andes-money-amount__cents')]/text()",
                "title_xpath": "/html/head/title/text()",#"title_xpath": "//h1[@class='ui-pdp-title']/text()",
                "discount_percentage": "//div[contains(@class, 'ui-pdp-container__col col-2 mr-24 mt-8')]//span[contains(@class, 'andes-money-amount__discount')]/text()",
                "asin_xpath": "/p/"
            }

        }
    return jsonDom.get(domain)

