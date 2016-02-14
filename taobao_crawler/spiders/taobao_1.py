#encoding=utf-8
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
from dmoz import logger
from ..settings import DEBUG

class JSMiddleware(object):
    _driver = [0]

    def __init__(self):
        super(JSMiddleware, self).__init__()
        if DEBUG:
            self._driver[0] = webdriver.Chrome(chromedriver_path, service_args=['--load-images=no'])
        else:
            self._driver[0] = webdriver.PhantomJS(phantomjs_driver_path, service_args=['--load-images=no'])

    @classmethod
    def get_driver(self):
        return self._driver[0]

    def process_request(self, request, spider):
        # TODO: easton: currently use PhantomJS to render all
        #if request.meta.get('js'): # you probably want a conditional trigger
            # easton: only chrome needs open the page before real one, and must in the same domain
            if DEBUG:
                self.get_driver().get('https://www.taobao.com/about/')
            load_cookies(self.get_driver())
            self.get_driver().get(request.url)
            # easton: phantomjs stored other domain's cookie, serious.
            #store_cookies(self.driver())
            if 'anti_Spider' in self.get_driver().current_url:
                logger.error('anti_Spider got you, gonna retry')
                sleep(1)
                reason = 'anti_Spider'
                return self._retry(request, reason, spider)
            body = self.get_driver().page_source
            return HtmlResponse(self.get_driver().current_url, body=body, encoding='utf-8', request=request)

    # easton: copy from RetryMiddleware
    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= 2: #self.max_retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority #+ self.priority_adjust
            return retryreq
        else:
            logger.warning("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})

if DEBUG == True:
    instantiated = JSMiddleware()

# if encounter anti spider, retry
# http://stackoverflow.com/questions/15602857/how-do-i-conditionally-retry-and-rescrape-the-current-page-in-scrapy
# http://stackoverflow.com/questions/20805932/scrapy-retry-or-redirect-middleware
class RetryMiddlewareSubclass(RetryMiddleware):
    pass
#    def process_response(self, request, response, spider):
#        if response.status in self.retry_http_codes:
#            reason = response_status_message(response.status)
#            return self._retry(request, reason, spider) or response
#        return response

class TaobaoSpider_1(Spider):
    """
    by emulating human browsing behaviour
    """
    name = "Taobao1"
    allowed_domains = ["taobao.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'taobao_crawler.pipelines.Taobao_Brands_Store_Pipeline': 1,
        }
    }
    start_urls = [
        "https://s.taobao.com/search?q=空调",
    ]

    def parse(self, response):
        items = []
        sel = Selector(response)
        brands_xpath = "//div[@id='J_NavCommonRowItems_0']/a"
        brands_links = sel.xpath(brands_xpath)
        assert len(brands_links) > 0, 'cant find brands on this page: {}'.format(response.url)

        count = 1
        for brand in brands_links:
            # easton: avoid taobao's anti spider
            sleep(5)
            JSMiddleware.get_driver().get(self.start_urls[0])

            item = Brand()
            item['name'] = brand.xpath('@title').extract()[0]
            try:
                # chrome and PhantomJS can't click invisible link, but js can make it
                #JSMiddleware.driver().find_element_by_xpath(brands_xpath + '[' + str(count) + ']').click()
                script = "var s=window.document.createElement('script');\
                    s.src='{}';\
                    window.document.head.appendChild(s); \
                    var s=window.document.createElement('script');\
                    s.src='{}';\
                    window.document.head.appendChild(s);".format(inject_jsfile_path1, inject_jsfile_path2)
                JSMiddleware.get_driver().execute_script(script)
                sleep(1) # wait browser loads js libs
                # chrome supports `$x(//div[@id="J_NavCommonRowItems_0"]/a)[0].click()
                script = '$(document).xpath("' + brands_xpath + '")[' + str(count-1) + '].click()'
                JSMiddleware.get_driver().execute_script(script)
            except WebDriverException:
                # if can't click
                logger.error(traceback.format_exc())
                logger.error(' '.join(['click failed.', 'count:', str(count), item['name'], JSMiddleware.get_driver.current_url, '\n']))
            else:
                item['url'] = JSMiddleware.get_driver().current_url
                items.append(item)
                yield item
            finally:
                 # if jump to login page, or pop the login window
                if 'anti_Spider' in JSMiddleware.get_driver().current_url or \
                        JSMiddleware.get_driver().current_url.startswith(self.start_urls[0].decode('utf-8')):
                    logger.critical('cant go ahead crawling, please manually pass the verification')
                    sys.exit(0)

        for i in items:
            yield Request(i['url'], callback = self.parse_separate_brand)

        #self.driver().close()
        #return items

    def parse_separate_brand(self):
        pass