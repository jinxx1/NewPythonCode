# -*- coding: utf-8 -*-
import scrapy
import re
import pprint
from gcproject.items import GcprojectItem
from gcproject.parseScrpy import get_timestr
import sqlalchemy
from urllib.parse import quote_plus
conStr_final = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER="gzcez",
                                                                                                 PASSWORD=quote_plus("1234@Qwer"),
                                                                                                 HOST="172.16.10.94",
                                                                                                 PORT=3306,
                                                                                                 DBNAME="shangqing")
conStr_temp = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER="xey",
                                                                                                PASSWORD=quote_plus("Xey123456!@#$%^"),
                                                                                                HOST="172.16.10.99",
                                                                                                PORT=3306,
                                                                                                DBNAME="shangqing")

mysqlcon_temp = sqlalchemy.create_engine(conStr_temp)
mysqlcon_final = sqlalchemy.create_engine(conStr_final)

temp_process_1_exc = "UPDATE ztbRawInfo_copy1 SET process_status=1 WHERE id={};"


def getmysqlInfo():
	exc = "select id,page_url,final_id from ztbRawInfo_copy1 where process_status=0;"
	a = mysqlcon_temp.execute(exc)
	llist = []
	for i in a:
		ddict = {}
		ddict['temp_id'] = i[0]
		ddict['page_url'] = i[1]
		ddict['final_id'] = i[2]
		llist.append(ddict)
	return llist

class DlztbArtcle1Spider(scrapy.Spider):
	name = 'dlztb_artcle1'

	allowed_domains = ['www.dlztb.com']
	site = '中国电力招标采购网'
	start_url = getmysqlInfo()

	def start_requests(self):
		meta = {}
		for i in self.start_url:
			# print(i)
			meta['page_url'] = i['page_url']
			meta['temp_id'] = i['temp_id']
			meta['final_id'] = i['final_id']

			if meta['final_id'] and meta['final_id'] > 0:
				yield scrapy.Request(url=meta['page_url'], callback=self.updateFinal, meta=meta)
			else:
				yield scrapy.Request(url=meta['page_url'], callback=self.parseA, meta=meta)

	def updateFinal(self, response):
		meta = response.meta
		item = {}
		Timet = response.xpath("//div[@class='m m3']/div[@class='m3l']/div[@class='info']|//div[@class='m_l f_l']/div[@class='left_box']/div[@class='info']").extract()
		Timet = ''.join(Timet)
		try:
			timerex = re.findall("\d{4}-\d{2}-\d{2}", Timet)[0]
		except:
			return None
		item['issue_time'] = get_timestr(timerex, "%Y-%m-%d %H:%M:%S")
		item['subclass'] = response.xpath("//div[@class='m']/div[@class='nav']/a[3]/text()|//div[@class='m_l f_l']/div[@class='left_box']/div[@class='pos']/a[3]").extract_first().replace('%', '%%')
		item['title'] = response.xpath("//h1[@id='title']/text()").extract_first().replace('%', '%%').replace('"', '')
		item['page_url'] = meta['page_url']


		exc2finalexc = '''UPDATE ztbRawInfo SET issue_time="{issue_time}",subclass="{subclass}",title="{title}" WHERE id={id};'''
		a = mysqlcon_final.execute(exc2finalexc.format(issue_time=item['issue_time'],
		                                           subclass=item['subclass'],
		                                           title=item['title'],
		                                           id=meta['final_id']))

		b = mysqlcon_temp.execute(temp_process_1_exc.format(str(meta['temp_id'])))



	def parseA(self, response):
		meta = response.meta
		item = GcprojectItem()
		Timet = response.xpath("//div[@class='m m3']/div[@class='m3l']/div[@class='info']|//div[@class='m_l f_l']/div[@class='left_box']/div[@class='info']").extract()
		Timet = ''.join(Timet)
		try:
			timerex = re.findall("\d{4}-\d{2}-\d{2}", Timet)[0]
		except:
			return None
		item['issue_time'] = get_timestr(timerex, "%Y-%m-%d %H:%M:%S")
		item['subclass'] = response.xpath(
			"//div[@class='m']/div[@class='nav']/a[3]/text()|//div[@class='m_l f_l']/div[@class='left_box']/div[@class='pos']/a[3]").extract_first().replace(
			'%', '%%')
		item['title'] = response.xpath("//h1[@id='title']/text()").extract_first().replace('%', '%%').replace('"', '')
		cutgif = "http://www.zgdlzb.org.cn/member/editor/fckeditor/editor/css/images/fck_anchor.gif"
		item['content'] = response.xpath("//div[@id='article']").extract_first().replace(cutgif, '').replace('%', '%%')
		item['page_url'] = response.url
		item['site'] = self.allowed_domains[0]
		if not item['content']:
			return None
		a = mysqlcon_temp.execute(temp_process_1_exc.format(str(meta['temp_id'])))
		print(a)
		yield item
