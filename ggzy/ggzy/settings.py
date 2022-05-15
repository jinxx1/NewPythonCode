

from getmysqlInfo import jsonInfo
BOT_NAME = 'ggzy'

SPIDER_MODULES = ['ggzy.spiders']
NEWSPIDER_MODULE = 'ggzy.spiders'


CLOSESPIDER_TIMEOUT = 0
CLOSESPIDER_ITEMCOUNT = 0
CLOSESPIDER_PAGECOUNT = 0
CLOSESPIDER_ERRORCOUNT = 10


# LOG_FILE = 'ciclog.log'
# LOG_LEVEL = 'ERROR'
LOG_LEVEL = 'DEBUG'
MYSQLINFO = jsonInfo['uxuepai_sql']

import json
# with open('mysql.json', 'r') as ff:
# 	MYSQLINFO = json.load(ff)
# MYSQLINFO = {
#     "HOST": "183.6.136.67",
#     "DBNAME": "uxsq",
#     "USER": "jinxiao_67",
#     "PASSWORD": "Qwer1234AQ",
#     "PORT":3306
# }
MYSQL_HOST = MYSQLINFO['HOST']
MYSQL_DATABASE = MYSQLINFO['DBNAME']
MYSQL_PORT = MYSQLINFO['PORT']
MYSQL_USER = MYSQLINFO['USER']
MYSQL_PASSWORD = MYSQLINFO['PASSWORD']


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_TIMEOUT = 120
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)

COOKIES_ENABLED = True
# COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'ggzy.middlewares.GgzySpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'ggzy.middlewares.GgzyDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
	'ggzy.pipelines.MysqlPipLine': 200,
	'ggzy.pipelines.GgzyPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
