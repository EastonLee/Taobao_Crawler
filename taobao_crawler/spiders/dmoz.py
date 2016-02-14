#coding=utf-8
from scrapy.selector import Selector
from scrapy.http import HtmlResponse, Request
from ..items import *
from rw_cookies import *
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
#from selenium.
from scrapy.spiders import BaseSpider, Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from ..settings import *
import traceback, sys, logging, ijson
from time import sleep
from StringIO import StringIO

logger = logging.getLogger('easton')

class DmozSpider_old(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://s.taobao.com/search?q=空调",
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url https://s.taobao.com/search?q=%E7%A9%BA%E8%B0%83
        @returns items 1 16
        @returns requests 0 0
        @scrapes name
        """
        sel = Selector(response)
        sites = sel.xpath('//ul[@class="directory-url"]/li')
        items = []

        for site in sites:
            item = Website()
            item['name'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            items.append(item)

        return items

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ul[@class="directory-url"]/li')

        for site in sites:
            il = WebsiteLoader(response=response, selector=site)
            il.add_xpath('name', 'a/text()')
            il.add_xpath('url', 'a/@href')
            il.add_xpath('description', 'text()', re='-\s([^\n]*?)\\n')
            yield il.load_item()

