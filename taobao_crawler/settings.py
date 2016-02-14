# Scrapy settings for taobao_crawler project
from random import randint
import os

SPIDER_MODULES = ['taobao_crawler.spiders']
NEWSPIDER_MODULE = 'taobao_crawler.spiders'
DEFAULT_ITEM_CLASS = 'taobao_crawler.items.Website'

# easton: i have scrapy-random-useragent now
#user_agent_list = [
#    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
#    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0'
#]
#i = 2
#USER_AGENT = user_agent_list[randint(0, len(user_agent_list) - 1)] if not i else i

# easton: don't use general pipeline for all spider.
# define specific pipeline for spider in their spider class
'''
ITEM_PIPELINES = {
    'taobao_crawler.pipelines.RequiredFieldsPipeline': 1,
    'taobao_crawler.pipelines.FilterWordsPipeline': 1,
    'taobao_crawler.pipelines.MySQLStorePipeline': 1,
}
'''


MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'scrapy'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'mysql'

# easton: visible chrome is used for debug, invisible PhantomJS is used for production enviroment
DEBUG = False
# if you load your own cookies
if_load_cookies = False

chromedriver_path = '/Users/easton/SCRIPTS/chromedriver'
phantomjs_driver_path = '/Users/easton/SCRIPTS/phantomjs-2.1.1'
# local.example.com lies on my computer.
inject_jsfile_path1 = 'https://cdn.staticfile.org/jquery/3.0.0-alpha1/jquery.min.js'
inject_jsfile_path1 = 'https://local.example.com/jquery.min.js'
inject_jsfile_path2 = 'https://cdn.jsdelivr.net/jquery.xpath/0.2.5/jquery.xpath.js'
inject_jsfile_path2 = 'https://local.example.com/jquery.xpath.js'


# =======================================================


# easton: avoid being block by anti spider
CONCURRENT_REQUESTS_PER_IP = 2
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
# easton: as for Phantom as the downloader middlewares
# https://groups.google.com/forum/#!topic/scrapy-users/vRZEP1vyJg8
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'random_useragent.RandomUserAgentMiddleware': 400,
        'taobao_crawler.spiders.taobao_1.JSMiddleware': 99
}
USER_AGENT_LIST = os.path.join(os.path.dirname(__file__), 'useragents.txt')
# retry failed request at the end
RETRY_ENABLED = True
RETRY_TIMES = 3
sleep_time_between_retry = 180
# cookie can be used to tell spider http://doc.scrapy.org/en/latest/topics/practices.html#bans
COOKIES_ENABLED = False
#COOKIES_DEBUG = True