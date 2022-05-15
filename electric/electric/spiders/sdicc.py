import scrapy
import pprint
import re
from electric.scrapyParse import *
from bs4 import BeautifulSoup
from electric.items import ElectricItem


class SdiccSpider(scrapy.Spider):
	name = 'sdicc'
	allowed_domains = ['www.sdicc.com.cn']
	start_urls = [
		{'catName': '招标预审公告', 'url': 'https://www.sdicc.com.cn/cgxx/ggList',
		 'arturl': 'https://www.sdicc.com.cn/cgxx/ggDetail?gcGuid={n1}&ggGuid={n0}',
		 'alpage': 11},
		# {'catName': '非招标采购公告', 'url': 'https://www.sdicc.com.cn/cgxx/ggList?caiGouType=1',
		#  'arturl': 'https://www.sdicc.com.cn/cgxx/ggDetail?gcGuid={n1}&ggGuid={n0}',
		#  'alpage': 53},
		# {'catName': '变更公告', 'url': 'https://www.sdicc.com.cn/cgxx/ggList?ggXingZhi=2',
		#  'arturl': 'https://www.sdicc.com.cn/cgxx/bgggDetail?ggGuid={n0}&shiXiangGuid={n1}',
		#  'alpage': 19},
		# {'catName': '候选人公示', 'url': 'https://www.sdicc.com.cn/cgxx/zbhxrList',
		#  'arturl': 'https://www.sdicc.com.cn/cgxx/zbhxrDetail?bdGuid={n0}&guid={n1}',
		#  'alpage': 3},
		# {'catName': '结果公告', 'url': 'https://www.sdicc.com.cn/cgxx/zbjgList',
		#  'arturl': 'https://www.sdicc.com.cn/cgxx/zbjgDetail?bdGuid={n0}&guid={n1}',
		#  'alpage': 35}
	]

	def __init__(self, goon=None, *args, **kwargs):
		super(SdiccSpider, self).__init__(*args, **kwargs)
		self.goon = goon

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		for i in self.start_urls:
			meta['subclass'] = i['catName']
			meta['listUrl'] = i['url']
			meta['actUrl'] = i['arturl']
			meta['alpage'] = i['alpage']
			nextPage = {'currentPage': str(meta['Num'])}
			yield scrapy.FormRequest(url=meta['listUrl'],
			                         dont_filter=True,
			                         formdata=nextPage,
			                         callback=self.parse,
			                         meta=meta)

	def parse(self, response):
		meta = response.meta
		lists = response.xpath("//tbody/tr/@onclick").extract()
		if not lists:
			return None
		llistUrl1 = []
		for i in lists:
			n = re.findall("\'(.*?)\'", i)
			acturl = meta['actUrl'].format(n0=n[0], n1=n[1])
			llistUrl1.append(acturl)
		llistUrl = urlIsExist(llistUrl1)
		print(meta['subclass'], meta['Num'], self.goon, len(lists))
		print('未录入数量', len(llistUrl))
		print('-------------------------------------------------------------------------------')
		for i in llistUrl:
			meta['urlcontent'] = i
			yield scrapy.Request(url=meta['urlcontent'],
			                     callback=self.parseA,
			                     meta=meta,
			                     dont_filter=True)
		print('************************************************************')

		if not llistUrl and self.goon == 'no':
			return None
		else:
			meta['Num'] += 1
			if meta['Num'] == meta['alpage'] + 1:
				return None
			nextPage = {'currentPage': str(meta['Num'])}
			yield scrapy.FormRequest(url=meta['listUrl'],
			                         dont_filter=False,
			                         formdata=nextPage,
			                         callback=self.parse,
			                         meta=meta)

	def parseA(self, response):
		item = ElectricItem()
		meta = response.meta
		content = response.xpath("/html/body/div[@class='dg-index-content']//span[@class='dg-flex-item']").extract()
		if not content:
			print('no content')
			print(response.url)
			print('----------------------------')
			return None
		HTMLcontent = ''.join(content)
		title = response.xpath(
			"//div[@class='dg-index-content']//h3[@class = 'dg-notice-title']/text()").extract_first()

		Time = response.xpath(
			"/html/body/div[@class='dg-index-content']//span[@class='dg-notice-state-item']/text()").extract_first()
		Timel = re.findall("\(发布时间：(.*?)\)", Time)

		if not Timel:
			Timel = re.findall("\d{2,4}-\d{1,2}-\d{1,2}", HTMLcontent)
			if not Timel:
				return None

		Timelstr = get_timestr(Timel[0], '%Y-%m-%d %H:%M:%S')

		soup = BeautifulSoup(HTMLcontent, 'lxml')
		hrefall = soup.find_all(href=re.compile('download'))
		if hrefall:
			from urllib.parse import unquote
			import requests
			attchment = []
			for nn in hrefall:
				ddict = {}
				ddict['download_url'] = nn.get('href')
				brow = requests.get(ddict['download_url'])
				filename = re.findall("filename=(.*)", brow.headers['Content-Disposition'])[0]
				ddict['name'] = unquote(filename, 'utf-8')
				attchment.append(ddict)
			item['attachmentListJson'] = json.dumps(attchment, ensure_ascii=False)

		item['issueTime'] = Timelstr
		item['url'] = meta['urlcontent']
		item['site'] = self.allowed_domains[0]
		item['subclass'] = meta['subclass']
		item['title'] = title
		item['content'] = HTMLcontent
		# pprint.pprint(item)

		yield item
