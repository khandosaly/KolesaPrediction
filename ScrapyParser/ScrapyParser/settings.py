
BOT_NAME = 'ScrapyParser'

SPIDER_MODULES = ['ScrapyParser.spiders']
NEWSPIDER_MODULE = 'ScrapyParser.spiders'

ROBOTSTXT_OBEY = True

FEED_FORMAT = "csv"
FEED_URI = "kolesa_cars.csv"
DOWNLOAD_TIMEOUT = 60
RETRY_TIMES = 2
