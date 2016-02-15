Taobao_Crawler
==========
# Disclaimer
该程序功能并不完善，尚有许多方面没有考虑。只可作为教育目的使用，作者不对程序不当之处引发的损失负责。

对程序有看法，请新建Issues，或者Pull requests。

# 部分文件说明

    ├── __init__.py
    ├── cookies.pkl 我的cookies序列化之后的pickle文件，请使用你自己的代替它
    ├── db
    │   ├── mysql.sql 创建MySQL数据库的SQL脚本
    │   └── scrapy_result.sql 该程序运行之后爬取的数据
    ├── js_files 如果采用方法一，请在本地架设HTTPS服务器，并server这两个JS文件，以便注入到淘宝的页面，以便使用XPATH选择器定位元素。
    ├── scrapy.cfg #配置文件。
    ├── start_scrape_taobao.py 执行该文件，即开始运行。
    └── taobao_crawler
        ├── JOB 用来存放爬虫任务。爬虫执行过程中，如果人为中断(ctrl c)，或者爬虫遇到反爬虫自动中断，重新启动后都会继续上次未完成的任务。
        │   └── Taobao2 一次任务执行完后，需要删除JOB目录下内容，才能重新开新任务。
        │       ├── requests.queue
        │       ├── requests.seen
        │       └── spider.state
        ├── __init__.py
        ├── items.py
        ├── pipelines.py
        ├── settings.py #配置文件
        ├── spiders
        │   ├── __init__.py
        │   ├── dmoz.py 模仿案例
        │   ├── taobao_1.py 方法一(停止开发)
        │   ├── taobao_2.py 方法二(推荐)
        └── useragents.txt 随机User-Agent列表

# Developing steps(incomplete，help yourself according your missing part)

* Install scrapy，Selenium，etc.:

    easy_install scrapy，selenium，beautifulsoup4，scrapy-random-useragent
* Initialize MySQL db，[https server](http://brianflove.com/2014/12/01/https-everywhere/) serving to-inject javascript file into selenium driver
* Custom spiders，items.py，pipelines.py，settings.py
* Test spiders
* Avoid anti-spider

# 使用手册
## 配置
* settings.py
    DEBUG: 只对方法一生效。如果设置，将使用Selenium驱动Chrome浏览器进行爬取。如果设置False，则使用PhantomJS。

    if_load_cookies: 如果设置，将在请求中加入已保存的cookie(cookies.pkl)

    chromedriver_path，phantomjs_driver_path，inject_jsfile_path: 对应的驱动的本地地址，jsfile的url。在我的环境中，https://local.example.com/在本地搭建。

    random_useragent.RandomUserAgentMiddleware: 用来在发送的请求中随机添加User-Agent。

    CONCURRENT_REQUESTS_PER_IP, DOWNLOAD_DELAY: 调节每个IP的并发请求数和下载延迟, 如果遇到反爬虫, 请酌情调节这两个值.

    其他部分请参考[Scrapy文档](http://doc.scrapy.org/en/latest/)

## 启动
进入Taobao_Crawler目录，执行如下命令:

    python start_scrape_taobao.py
程序默认使用方法二爬取。

## 部分结果
时间两分多钟

    2016-02-14 23:54:57 [scrapy] INFO: Dumping Scrapy stats:
    {'downloader/request_bytes': 25600,
     'downloader/request_count': 67,
     'downloader/request_method_count/GET': 67,
     'downloader/response_bytes': 1276512,
     'downloader/response_count': 67,
     'downloader/response_status_count/200': 67,
     'finish_reason': 'finished',
     'finish_time': datetime.datetime(2016, 2, 14, 15, 54, 57, 231056),
     'item_scraped_count': 1179,
     'log_count/DEBUG': 2426,
     'log_count/INFO': 9,
     'log_count/WARNING': 3,
     'request_depth_max': 1,
     'response_received_count': 67,
     'scheduler/dequeued': 67,
     'scheduler/dequeued/disk': 67,
     'scheduler/enqueued': 67,
     'scheduler/enqueued/disk': 67,
     'start_time': datetime.datetime(2016, 2, 14, 15, 52, 16, 673640)}
    2016-02-14 23:54:57 [scrapy] INFO: Spider closed (finished)

# 附录
## 常用scrapy命令
    scrapy check/fetch url/crawl spider-name/parse url/runspider spider_file/view url/shell url/
