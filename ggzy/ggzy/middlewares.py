# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.exceptions import CloseSpider
from collections import defaultdict
from scrapy.exceptions import NotConfigured

class Close_spider(object):
	def __init__(self, crawler):
		self.crawler = crawler
		self.close_on = {
			'timeout': crawler.settings.getfloat('CLOSESPIDER_TIMEOUT'),
			'itemcount': crawler.settings.getint('CLOSESPIDER_ITEMCOUNT'),
			'pagecount': crawler.settings.getint('CLOSESPIDER_PAGECOUNT'),
			'errorcount': crawler.settings.getint('CLOSESPIDER_ERRORCOUNT'),
		}

		if not any(self.close_on.values()):
			raise NotConfigured

		self.counter = defaultdict(int)
		if self.close_on.get('errorcount'):
			crawler.signals.connect(self.error_count, signal=signals.spider_error)
		if self.close_on.get('pagecount'):
			crawler.signals.connect(self.page_count, signal=signals.response_received)
		if self.close_on.get('timeout'):
			crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
		if self.close_on.get('itemcount'):
			crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
		crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

		self.Error403 = 0

	def process_spider_input(self, response, spider):

		if self.Error403 == 10:
			self.Error403 = 0
			raise CloseSpider('{}错误，退出！'.format(response.status))
		if response.status > 402:
			self.Error403 += 1
		return None

	def process_spider_output(self, response, result, spider):
		for res in result:
			yield res

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler)

	def error_count(self, failure, response, spider):
		self.counter['errorcount'] += 1
		if self.counter['errorcount'] == self.close_on['errorcount']:
			self.crawler.engine.close_spider(spider, 'closespider_errorcount')

	def page_count(self, response, request, spider):
		self.counter['pagecount'] += 1
		if self.counter['pagecount'] == self.close_on['pagecount']:
			self.crawler.engine.close_spider(spider, 'closespider_pagecount')

	def spider_opened(self, spider):
		from twisted.internet import reactor
		self.task = reactor.callLater(self.close_on['timeout'],
		                              self.crawler.engine.close_spider, spider,
		                              reason='closespider_timeout')

	def item_scraped(self, item, spider):
		self.counter['itemcount'] += 1
		if self.counter['itemcount'] == self.close_on['itemcount']:
			self.crawler.engine.close_spider(spider, 'closespider_itemcount')

	def spider_closed(self, spider):
		task = getattr(self, 'task', False)
		if task and task.active():
			task.cancel()


class GgzySpiderMiddleware:
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the spider middleware does not modify the
	# passed objects.

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_spider_input(self, response, spider):
		# Called for each response that goes through the spider
		# middleware and into the spider.

		# Should return None or raise an exception.
		return None

	def process_spider_output(self, response, result, spider):
		# Called with the results returned from the Spider, after
		# it has processed the response.

		# Must return an iterable of Request, or item objects.
		for i in result:
			yield i

	def process_spider_exception(self, response, exception, spider):
		# Called when a spider or process_spider_input() method
		# (from other spider middleware) raises an exception.

		# Should return either None or an iterable of Request or item objects.
		pass

	def process_start_requests(self, start_requests, spider):
		# Called with the start requests of the spider, and works
		# similarly to the process_spider_output() method, except
		# that it doesn’t have a response associated.

		# Must return only requests (not items).
		for r in start_requests:
			yield r

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)


class GgzyDownloaderMiddleware:
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the downloader middleware does not modify the
	# passed objects.

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_request(self, request, spider):
		# Called for each request that goes through the downloader
		# middleware.

		# Must either:
		# - return None: continue processing this request
		# - or return a Response object
		# - or return a Request object
		# - or raise IgnoreRequest: process_exception() methods of
		#   installed downloader middleware will be called
		return None

	def process_response(self, request, response, spider):
		# Called with the response returned from the downloader.

		# Must either;
		# - return a Response object
		# - return a Request object
		# - or raise IgnoreRequest
		return response

	def process_exception(self, request, exception, spider):
		# Called when a download handler or a process_request()
		# (from other downloader middleware) raises an exception.

		# Must either:
		# - return None: continue processing this exception
		# - return a Response object: stops process_exception() chain
		# - return a Request object: stops process_exception() chain
		pass

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)
