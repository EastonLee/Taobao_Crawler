import scrapy
from scrapy.crawler import CrawlerProcess
from taobao_crawler.spiders.taobao_1 import TaobaoSpider_1
from taobao_crawler.spiders.taobao_2 import TaobaoSpider_2
from taobao_crawler import settings as s
from scrapy.settings import Settings
from taobao_crawler.settings import DEBUG

settings = Settings()
settings.setmodule(s)
process = CrawlerProcess(settings)

if DEBUG:
    spider = TaobaoSpider_1
else: spider = TaobaoSpider_2
process.crawl(spider)
process.start()
