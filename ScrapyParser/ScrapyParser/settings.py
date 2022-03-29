
BOT_NAME = 'ScrapyParser'

SPIDER_MODULES = ['ScrapyParser.spiders']
NEWSPIDER_MODULE = 'ScrapyParser.spiders'

ROBOTSTXT_OBEY = True

FEED_FORMAT = "csv"
FEED_URI = "kolesa_cars.csv"
DOWNLOAD_TIMEOUT = 60
RETRY_TIMES = 2

PROXY_LIST = 'proxylist.txt'
PROXY_MODE = 0
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy_crawlera.CrawleraMiddleware': 600,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400
}