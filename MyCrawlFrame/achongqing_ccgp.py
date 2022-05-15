# -*- coding: utf-8 -*-
import json
import pprint
import sys, re
import time, datetime
import requests
import lxml
import lxml.html
from lxml.html import HtmlComment
from lxml import etree
from lxml import html as htmlstr
from mkdir import mkdir
from redisBloomHash import *
from getmysqlInfo import jsonInfo
from crawltools import *
from reqSession import *
from uxue_orm import *
from requests.adapters import HTTPAdapter
import chardet, cchardet
from urllib import parse as urlpase
from bs4 import BeautifulSoup
import json

minfo = {
	"craw_id": "www.ccgp-chongqing.gov.cn",
	"site": "www.ccgp-chongqing.gov.cn",
	"siteCname": "重庆市政府采购",
	"HEA": '''Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Cookie: Hm_lvt_a41ec8f07afa1805aa0eaeec292c8be0=1645083853; Hm_lpvt_a41ec8f07afa1805aa0eaeec292c8be0=1645083876
Host: www.ccgp-chongqing.gov.cn
Referer: https://www.ccgp-chongqing.gov.cn/notices/list?purches=%E9%87%87%E8%B4%AD%E5%85%AC%E5%91%8A
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36
X-Requested-With: XMLHttpRequest''',
	"cookies": None,

	"transmitCookies": False,
	"hub_xpath": {
		"page_url": "//table[@id='moredingannctable']//td/a/@href",
		"title": "//*[@href='{}']/text()",
		"issus_time": "",
		"location": "//meta[@name='SiteName']/@content",
	},
	"hub_method": "GET",
	"hub_jsonmainKey": "",
	"hub_postdate": {},
	"hub_dictKeys": {},
	"article_method": "GET",
	"article_postdate": {},
	"article_dictKeys": {},
	"article_jsonmainKey": "",
	"article_xpath": {
		"content": "//table[@id='2020_VERSION']//span[@class='txt7']",
		"location": "",
		"issus_time": "//meta[@name='PubDate']/@content",
		"title": "//meta[@name='ArticleTitle']/@content",
	},
	"article_attchment_hrefkeysword": "BidDingAnncFiles",
}


def hub_main(timeL):
	mysql_db_orm = mysql_orm()
	reqSession = req_session(minfo)
	pageS = 50
	breakMark = 0
	pi = 1
	baseUrl = "https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/new?__platDomain__=www.ccgp-chongqing.gov.cn&endDate={todaytime}&pi={pi}&ps={pageS}&startDate={todaytime}"
	getUrl = baseUrl.format(todaytime=timeL, pi=pi, pageS=pageS)
	artcleBaseUrl = "https://www.ccgp-chongqing.gov.cn/notices/detail/{}"
	whileTrue = True
	while whileTrue:
		hhtml = reqSession.GetReHtml(getUrl)
		jsonT = json.loads(hhtml)
		try:
			if len(jsonT['notices']) == 0:
				whileTrue = False
				continue
		except:
			whileTrue = False
			continue
		llist = []
		mark = 0
		for info in jsonT['notices']:
			article_Url = artcleBaseUrl.format(info['id'])
			if bl.exists(article_Url) or bh.exists(article_Url):
				mark += 1
				continue
			ztbhubinfo = ZtbHubInfo()
			ztbhubinfo.craw_status = 0
			ztbhubinfo.create_time = datetime.datetime.now()
			ztbhubinfo.update_time = datetime.datetime.now()
			ztbhubinfo.site = minfo['site']
			ztbhubinfo.craw_id = minfo['craw_id']
			ztbhubinfo.page_url = info['id']
			ztbhubinfo.title = info['title']
			ztbhubinfo.issue_time = info['issueTime']
			ztbhubinfo.subclass = ''
			ztbhubinfo.project_amount = round(info['projectBudget'], 2)
			ztbhubinfo.ztb_project_tenderer = info['buyerName'][:20]
			try:
				ztbhubinfo.ztb_project_agent = info['agentName'][:20]
			except:
				pass
			ztbhubinfo.business_type = info['projectDirectoryName']
			province_name_dict = tureLocation(localName='重庆市', title=info['districtName'])
			ztbhubinfo.province_name = province_name_dict['province_name']
			if province_name_dict['city_name']:
				ztbhubinfo.city_name = province_name_dict['city_name']
				if len(province_name_dict['city_name']) <= 2:
					ztbhubinfo.city_name = ''
			else:
				ztbhubinfo.city_name = ''
			ztbhubinfo.str1 = province_name_dict['str1'] + "/{}".format(info['districtName'])[:20]
			llist.append(ztbhubinfo.__dict__)

		if llist:
			mysql_db_orm.ztbhubinfo_all_insert(llist)

		if mark == len(jsonT['notices']):
			breakMark += 1
			print("breakMark += 1", breakMark)
		else:
			breakMark = 0

		if breakMark == 5:
			whileTrue = False
			continue

		if jsonT['total'] % pageS == 0:
			allPage = jsonT['total'] // pageS
		else:
			allPage = jsonT['total'] // pageS + 1
		if pi >= allPage:
			whileTrue = False
			continue
		else:
			pi += 1
		time.sleep(sleepSec(3, 9))


def article_main():
	mysql_db_orm = mysql_orm()
	reqSession = req_session(minfo)

	get_hubList = mysql_db_orm.session.query(ZtbHubInfo).filter(ZtbHubInfo.craw_status == 0,
	                                                            ZtbHubInfo.site == "www.ccgp-chongqing.gov.cn").order_by(
		ZtbHubInfo.issue_time.desc()).limit(300).all()
	print(len(get_hubList))
	if len(get_hubList) == 0:
		return None
	for hubInfo in get_hubList:

		artcleBaseUrl = "https://www.ccgp-chongqing.gov.cn/notices/detail/{}"
		postUrlbase = "https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/{}"
		page_url = artcleBaseUrl.format(hubInfo.page_url)
		if bl.exists(page_url):
			continue

		post_url = postUrlbase.format(hubInfo.page_url)
		hhtml = reqSession.GetReHtml(post_url)
		jsonT = json.loads(hhtml)
		if jsonT['msg'] != '成功':
			print(jsonT)
			continue
		json_notice = jsonT['notice']
		if not json_notice['html']:
			continue
		ztbrawInfo_dict = {}

		hunbInfo_dict = hubInfo.__dict__
		for keyName in hunbInfo_dict.keys():
			if hunbInfo_dict[keyName]:
				ztbrawInfo_dict[keyName] = hunbInfo_dict[keyName]
		ztbrawInfo_dict['content'] = json_notice['html']
		ztbrawInfo_dict['page_url'] = page_url
		try:
			ztbrawInfo_dict['purchase_type'] = json_notice['projectPurchaseWayName']
		except:
			pass

		ztbrawInfo_dict['attachments'] = []
		if 'attachments' in json_notice.keys() and len(json_notice['attachments']) > 2:
			attchmentsList = json.loads(json_notice['attachments'])

			for attch in attchmentsList:
				ddict = {}
				ddict['download_url'] = "https://www.ccgp-chongqing.gov.cn/" + attch['value']
				ddict['download_filename'] = attch['name']
				ztbrawInfo_dict['attachments'].append(ddict)

		rawinfo_id = mysql_db_orm.ztbRawInfo_add_single(hubInfo=hubInfo, articleInfo=ztbrawInfo_dict)
		if not rawinfo_id:
			# print('rawinfo_id',rawinfo_id)
			continue
		print(rawinfo_id)
		mysql_db_orm.ztbRawInfoContent_add_single(content=ztbrawInfo_dict['content'], rawid=rawinfo_id)
		if ztbrawInfo_dict['attachments']:
			mysql_db_orm.ztbInfoAttaChment_add_single(info=ztbrawInfo_dict['attachments'], rawid=rawinfo_id)

		mysql_db_orm.ztb_Attached_add_single(info=ztbrawInfo_dict, rawid=rawinfo_id)
		time.sleep(sleepSec(3, 9))

def main():
	print('chongqing')


if __name__ == '__main__':
	try:
		input_1 = sys.argv[1]
	except:
		raise '必须输入hub或article'
	try:
		input_2 = sys.argv[2]
	except:
		input_2 = ''

	if input_1 == 'hub':
		if input_2:
			timeList = getBetweenDayList(input_2)
			for timel in timeList:
				hub_main(timeL=timel)
				time.sleep(sleepSec(3, 9))
		else:
			hub_main(timeL=datetime.date.today())

	if input_1 == 'article':
		article_main()
