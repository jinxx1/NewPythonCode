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
from redisBloomHash import bl
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
	"craw_id": "www.ccgp.gov.cn",
	"site": "www.ccgp.gov.cn",
	"siteCname": "中国政府采购网",
	"HEA": '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Cookie: Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1642767651,1645007077,1645112929; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1645112938; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1642764246,1645112943; JSESSIONID=cDkIX5w3ej74okvNBjwN4S-M3f5EsHKtodanVolD6HPBO7wKMFC3!-1094063090; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1645112959
Host: search.ccgp.gov.cn
Referer: http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=2&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=&dbselect=bidx&kw=&start_time=2022%3A02%3A17&end_time=2022%3A02%3A17&timeType=0&displayZone=&zoneId=&pppStatus=0&agentName=
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36''',
	"transmitCookies": False,
	"cookies": None
}


def hub_main(timeL):

	mysql_db_orm = mysql_orm()
	reqSession = req_session(minfo)
	pageS = 20
	pi = 1
	baseUrl = "http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={pi}&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=&dbselect=bidx&kw=&start_time={todaytime}&end_time={todaytime}&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName="

	breakMark = 0
	whileTrue = True
	while whileTrue:
		timeaL = str(timeL).replace('-','%3A')

		getUrl = baseUrl.format(todaytime=timeaL, pi=pi)
		hhtml = reqSession.GetReHtml(getUrl)
		soup = BeautifulSoup(hhtml, 'lxml')
		info = soup.find('ul', class_="vT-srch-result-list-bid").find_all('li')

		if len(info) == 0:
			whileTrue = False
			continue

		allInfo = []
		mark = 0
		for li in info:
			ztbhubinfo = ZtbHubInfo()
			ztbhubinfo.craw_status = 0
			ztbhubinfo.create_time = datetime.datetime.now()
			ztbhubinfo.update_time = datetime.datetime.now()
			ztbhubinfo.site = minfo['site']
			ztbhubinfo.craw_id = minfo['craw_id']
			try:
				ztbhubinfo.page_url = li.find('a').get('href')
				if bl.exists(ztbhubinfo.page_url) or bh.exists(ztbhubinfo.page_url):
					mark += 1
					continue
			except Exception as ff:
				continue

			try:
				ztbhubinfo.title = li.find('a').get_text().strip()
			except:
				ztbhubinfo.title = ''

			ztbhubinfo.province_name = ''
			location = li.find('a', attrs={'href': "javascript:void(0)"}).get_text()
			if location:
				province_name_dict = tureLocation(localName=location, title=ztbhubinfo.title)
				ztbhubinfo.province_name = province_name_dict['province_name']
				if province_name_dict['city_name']:
					ztbhubinfo.city_name = province_name_dict['city_name']
					if len(province_name_dict['city_name']) <= 2:
						ztbhubinfo.city_name = ''
				else:
					ztbhubinfo.city_name = ''
				ztbhubinfo.str1 = province_name_dict['str1']

			span = li.find('span').get_text().replace('\r', '').strip()
			reg_time = re.compile("\d{1,4}\.\d{1,2}\.\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}")
			if reg_time.search(span):
				ztbhubinfo.issue_time = get_timestr(reg_time.search(span).group())
			try:
				ztbhubinfo.ztb_project_tenderer = re.findall("采购人：(.*)", span)[0][:20]
			except:
				ztbhubinfo.ztb_project_tenderer = ''

			try:
				ztbhubinfo.ztb_project_agent = re.findall("代理机构：(.*)", span)[0][:20]
			except:
				ztbhubinfo.ztb_project_agent = ''
			strongList = li.find_all('strong')
			if len(strongList) == 2:
				ztbhubinfo.purchase_type = strongList[0].get_text().strip()
				ztbhubinfo.business_type = strongList[1].get_text().strip()
			elif len(strongList) == 1:
				ztbhubinfo.purchase_type = strongList[0].get_text().strip()
			else:
				pass
			ztbhubinfo.subclass = ''
			allInfo.append(ztbhubinfo.__dict__)

		if allInfo:
			mysql_db_orm.ztbhubinfo_all_insert(allInfo)
		reg_allpage = int(re.findall("Pager\(\{.*?size: (\d{1,4}),", soup.prettify(), re.M | re.S)[0])

		if len(info) < pageS or pi == reg_allpage:
			whileTrue = False
			continue

		if mark == len(info):
			breakMark += 1
			print("breakMark += 1", breakMark)
		else:
			breakMark = 0

		if breakMark == 15:
			whileTrue = False
			continue

		log = f"本页{len(info)}条，未录{len(info) - mark}篇，共{reg_allpage}页，第{pi}页，{timeL}"
		print(log)
		pi += 1
		time.sleep(sleepSec(3, 9))

def article_main():
	mysql_db_orm = mysql_orm()
	reqSession = req_session(minfo)

	get_hubList = mysql_db_orm.session.query(ZtbHubInfo).filter(ZtbHubInfo.craw_status == 0,
	                                                            ZtbHubInfo.site == minfo['site']).order_by(
		ZtbHubInfo.issue_time.desc()).limit(300).all()
	print(len(get_hubList))
	if not get_hubList:
		return None
	for hubInfo in get_hubList:
		# if bl.exists(hubInfo.page_url):
		# 	continue
		hhtml = reqSession.GetReHtml(hubInfo.page_url)
		soup = BeautifulSoup(hhtml, 'lxml')

		ztbrawInfo_dict = {}
		ztbrawInfo_dict['title'] = soup.find('meta', attrs={"name": "ArticleTitle"}).get('content')
		ztbrawInfo_dict['issue_time'] = get_timestr(soup.find('meta', attrs={"name": "PubDate"}).get('content'))

		hunbInfo_dict = hubInfo.__dict__
		for keyName in hunbInfo_dict.keys():
			if keyName in ['title', 'issue_time']:
				continue
			if hunbInfo_dict[keyName]:
				ztbrawInfo_dict[keyName] = hunbInfo_dict[keyName]

		content = soup.find('div', class_="vF_detail_content").prettify()
		content_summary = soup.find('div', class_="table").prettify()

		ztbrawInfo_dict['content'] = content_summary + content

		regex = re.compile(".*download.*|.*api/file.*|.*uploadfile.*")
		attchments = soup.find_all(href=regex)
		ztbrawInfo_dict['attachments'] = []
		if attchments:
			for i in attchments:
				ddict = {}

				ddict['download_url'] = urlpase.urljoin(base='http://www.ccgp.gov.cn/',url=i.get("href"))
				if not ddict['download_url']:
					continue
				ddict['download_filename'] = i.get_text()
				ztbrawInfo_dict['attachments'].append(ddict)

		rawinfo_id = mysql_db_orm.ztbRawInfo_add_single(hubInfo=hubInfo, articleInfo=ztbrawInfo_dict)
		if not rawinfo_id:
			continue
		insertContent = mysql_db_orm.ztbRawInfoContent_add_single(content=ztbrawInfo_dict['content'], rawid=rawinfo_id)
		if not insertContent:
			mysql_db_orm.session.query(ZtbRawInfo).filter(ZtbRawInfo.id == rawinfo_id).update({"craw_status": 2})
			mysql_db_orm.session.commit()
		if ztbrawInfo_dict['attachments']:
			mysql_db_orm.ztbInfoAttaChment_add_single(info=ztbrawInfo_dict['attachments'], rawid=rawinfo_id)

		mysql_db_orm.ztb_Attached_add_single(info=ztbrawInfo_dict, rawid=rawinfo_id)
		time.sleep(sleepSec(3, 9))

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
