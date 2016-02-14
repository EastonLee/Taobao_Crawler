#coding=utf-8
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.http import HtmlResponse, Request
from ..items import *
from rw_cookies import *
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
#from selenium.
from scrapy.spiders import BaseSpider, Spider
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from ..settings import *
import traceback, sys, logging, ijson
from time import sleep
from StringIO import StringIO
from scrapy.utils.response import open_in_browser, response_status_message
from dmoz import logger
from scrapy.exceptions import CloseSpider

class TaobaoSpider_2(Spider):
    """
    by parse javascript code on taobao page
    """
    name = "Taobao2"
    allowed_domains = ["taobao.com"]


    custom_settings = {
        'ITEM_PIPELINES': {
            'taobao_crawler.pipelines.Taobao_Brands_Store_Pipeline': 1,
            'taobao_crawler.pipelines.Taobao_BrandsModel_Store_Pipeline': 1,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
            'random_useragent.RandomUserAgentMiddleware': 400
        },
        'JOBDIR':  os.path.join(os.path.dirname(__file__), '..', 'JOB', 'Taobao2'),
    }

    # this var name will not used by default (start_urls)
    easton_start_urls = [
        "https://s.taobao.com/search?q=空调",
    ]

    def __init__(self):
        super(TaobaoSpider_2, self).__init__()
        self.scrape_count = 0
        self.total_scrape = 1
        self.anti_spider_breakpoit_msg = 'detected anti spider, please take a break for 10 min. restart to resume'

    def start_requests(self):
        if if_load_cookies:
            return [scrapy.FormRequest(self.easton_start_urls[0], cookies=load_cookies())]
        else:
            return [scrapy.FormRequest(self.easton_start_urls[0], meta={'cookiejar': 9999},)]

    def parse(self, response):
        #self.logger.info(response.request.headers['User-Agent'])
        js_obj = self.parse_js_obj_g_page_config(response)

        items = []
        sel = Selector(response)
        brands_xpath = "//div[@id='J_NavCommonRowItems_0']/a"
        brands_links = sel.xpath(brands_xpath)

        # js_obj['mods']['nav']['data']['common'] is different category, like brands, form, due size, power, and so on
        # js_obj['mods']['nav']['data']['common'][0]['sub'] is all brands
        self.total_scrape = len(js_obj['mods']['nav']['data']['common'][0]['sub']) + 1

        for i in range(self.total_scrape - 1):
            item = Brand()
            item['name'] = js_obj['mods']['nav']['data']['common'][0]['sub'][i]['text']
            url = js_obj['mods']['nav']['data']['common'][0]['sub'][i]['traceData']['click']
            url = url.replace(':', '=').replace(';', '&')
            url = ''.join([self.easton_start_urls[0], '&', url.encode('utf-8')])
            item['url'] = url
            items.append(item)
            self.scrape_count += 1
            yield item

        for i in items:
            if if_load_cookies:
                yield Request(i['url'], cookies=load_cookies(), callback = self.parse_separate_brand)
            else:
                yield Request(i['url'], meta={'cookiejar': i}, callback = self.parse_separate_brand)

    def parse_separate_brand(self, response):
        js_obj = self.parse_js_obj_g_page_config(response)

        brand = js_obj['mods']['nav']['data']['breadcrumbs']['propSelected'][0]['sub'][0]['text']
        items = []
        # js_obj['mods']['grid']['spus'] is all models list
        for i in range(len(js_obj['mods']['grid']['data']['spus'])):
            model = js_obj['mods']['grid']['data']['spus'][i]
            item = Model()
            item['brand'] = brand.encode('utf-8')
            item['model'] = model['title'].encode('utf-8')
            item['price'] = model['price'].encode('utf-8')
            item['no_of_seller'] = model['seller']['num'].encode('utf-8')
            item['power'] = model['importantKey'].encode('utf-8')
            items.append(item)
            yield item

    def parse_js_obj_g_page_config(self, response):
        """
        :param response:
        :type response: str
        :return dicted js obj  g_page_config:
        :rtype :dict
        """
        if self.detect_anti_spider_from_response(response):
            logger.critical(self.anti_spider_breakpoit_msg)
            sys.exit()
        # this name is from taobao page: https://s.taobao.com/search?q=空调
        g_page_config = ''
        for line in response.body.split('\n'):
            if 'g_page_config' in line:
                g_page_config = line.split('{', 1)[1].rsplit('}', 1)[0]
                break

        js_obj_gen = ijson.items(StringIO(''.join(('{', g_page_config, '}'))), '')
        js_obj_from_gen = [i for i in js_obj_gen]
        js_obj = js_obj_from_gen[0]

        if self.detect_anti_spider_from_js_obj(js_obj, response):
            logger.critical(self.anti_spider_breakpoit_msg)
            sys.exit()
        return js_obj

    def detect_anti_spider_from_js_obj(self, js_obj, response):
        if 'pageName' not in js_obj or js_obj['pageName'] != u'spulist' :
            msg = '\nthis page is not search result! the url is {}\n'\
                  'please consider a retry, or use random USER_AGENT in settings.py, '\
                  'or load a different cookie, or set separate cookie for each spider' \
                  'or try a proxy\n' \
                  '{} done scrapes / {} due scrapes'.format(response.url, self.scrape_count, self.total_scrape)
            self.logger.critical(msg)
            self.logger.critical('let me check this in browser...')
            open_in_browser(response)
            return True
        return False

    def detect_anti_spider_from_response(self, response):
        if 'anti_Spider' in response.url:
            return True
        return False
