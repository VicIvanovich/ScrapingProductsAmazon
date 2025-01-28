from scraping_amazon.spiders.amazon_spider import AmazonSpider
from scrapy.crawler import CrawlerProcess

def run_spider():
    process = CrawlerProcess()
    process.crawl(AmazonSpider)
    process.start()

if __name__ == '__main__':
    print("Inicializando o spider da Amazon!")
    run_spider()
