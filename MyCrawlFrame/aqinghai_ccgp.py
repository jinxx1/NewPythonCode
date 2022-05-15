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
import requests
from bs4 import BeautifulSoup
import json

minfo = {
	"craw_id": "www.ccgp-qinghai.gov.cn",
	"site": "www.ccgp-qinghai.gov.cn",
	"siteCname": "青海政府采购网",
	"HEA": '''Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Content-Length: 211
Content-Type: application/json
Cookie: _zcy_log_client_uuid=0eecdba0-91b3-11ec-a3db-cde1659c2509; acw_tc=76b20ff816453461003348703e3bb4f488d56ef77498a6ebaffcae1afb4c41
Host: www.ccgp-qinghai.gov.cn
Origin: http://www.ccgp-qinghai.gov.cn
Referer: http://www.ccgp-qinghai.gov.cn/ZcyAnnouncement/ZcyAnnouncement2/index.html?begin=1643644800000&end=1645372799999&districtCode=630100%2C630200%2C632200%2C632300%2C632500%2C632600%2C632700%2C632800
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36''',
	"transmitCookies": False,
	"cookies": None,
	"posturl": 'http://www.ccgp-qinghai.gov.cn/front/search/category',
}

sub_and_codeList = [
	{'subclass': '采购意向', 'code': 'ZcyAnnouncement11'},
                    {'subclass': '采购公示', 'code': 'ZcyAnnouncement1'},
                    {'subclass': '公开招标', 'code': 'ZcyAnnouncement2'},
                    {'subclass': '邀请招标公告', 'code': 'ZcyAnnouncement3009'},
                    {'subclass': '竞争性谈判公告', 'code': 'ZcyAnnouncement3002'},
                    {'subclass': '竞争性磋商公告', 'code': 'ZcyAnnouncement3011'},
                    {'subclass': '询价采购公告', 'code': 'ZcyAnnouncement3003'},
                    {'subclass': '中标公告', 'code': 'ZcyAnnouncement4'},
                    {'subclass': '变更公告', 'code': 'ZcyAnnouncement3'},
                    {'subclass': '废流标公告', 'code': 'ZcyAnnouncement9999'},
                    {'subclass': '资格预审公告', 'code': 'ZcyAnnouncement8888'},
                    {'subclass': '合同公告', 'code': 'ZcyAnnouncement5'},
                    {'subclass': '电子卖场公告', 'code': 'ZcyAnnouncement8'}
                    ]

location_codeList = [["639900"], ["630100", "630200", "632200", "632300", "632500", "632600", "632700", "632800"]]

def hub_main(timeL):
	mysql_db_orm = mysql_orm()
	reqSession = req_session(minfo)
	pageS = 15

	for cateCode in sub_and_codeList:
		for lo in location_codeList:
			breakMark = 0
			whileTrue = True
			pi = 1
			while whileTrue:
				time.sleep(sleepSec(3, 9))

				postdate = {"pageNo": pi,
				            "pageSize": pageS,
				            "categoryCode": cateCode['code'],
				            "districtCode": lo,
				            "publishDateBegin": str(timeL), 'publishDateEnd': str(timeL)}

				originBrow = reqSession.PostResult(posturl=minfo['posturl'], postdate=json.dumps(postdate), jsonT=1)
				jsonT = originBrow['hits']
				# pprint.pprint(originBrow)
				mark = 0
				hubinfoList = []
				if len(jsonT['hits']) == 0:
					whileTrue = False
					print('not hubinfoList',len(hubinfoList))
					continue
				for info in jsonT['hits']:
					ZtbHubInfo_obj = ZtbHubInfo()
					ZtbHubInfo_obj.page_url = 'http://www.ccgp-qinghai.gov.cn/' + info['_source']['url']
					if bl.exists(ZtbHubInfo_obj.page_url) or bh.exists(ZtbHubInfo_obj.page_url):
						mark += 1
						continue
					ZtbHubInfo_obj.site = minfo['site']

					try:
						ZtbHubInfo_obj.purchase_type = info['_source']['pathName']
					except:
						pass
					try:
						ZtbHubInfo_obj.ztb_ztbInfoType_tenderType = info['_source']['procurementMethod']
					except:
						pass
					try:
						ZtbHubInfo_obj.business_type = info['_source']['gpCatalogName']
					except:
						pass

					ZtbHubInfo_obj.title = info['_source']['title']
					ZtbHubInfo_obj.subclass = cateCode['subclass']
					ZtbHubInfo_obj.issue_time = timestampREtimestr(info['_source']['publishDate'])

					province_name_dict = tureLocation(localName='青海', title=ZtbHubInfo_obj.title)
					ZtbHubInfo_obj.province_name = province_name_dict['province_name']
					if province_name_dict['city_name']:
						ZtbHubInfo_obj.city_name = province_name_dict['city_name']
						if len(province_name_dict['city_name']) <= 2:
							ZtbHubInfo_obj.city_name = ''
					else:
						ZtbHubInfo_obj.city_name = ''
					ZtbHubInfo_obj.str1 = province_name_dict['str1']
					hubinfoList.append(ZtbHubInfo_obj.__dict__)
				if hubinfoList:
					mysql_db_orm.ztbhubinfo_all_insert(hubinfoList)

				log1 = f"{cateCode['subclass']}"
				log2 = lo
				log = f"本页{len(jsonT['hits'])}条，未录{len(jsonT['hits']) - mark}篇，共{jsonT['total']}篇，第{pi}页，{timeL}"
				print(log1)
				print(log2)
				print(log)
				# print(postdate)
				# print(json.dumps(postdate))
				# whileTrue = False
				print('--------------------------------------------')
				time.sleep(sleepSec(3, 9))


				if mark == len(jsonT['hits']):
					breakMark += 1
					print("breakMark += 1", breakMark)
				else:
					breakMark = 0

				if breakMark == 5:
					whileTrue = False
					continue

				if jsonT['total'] % pageS == 0:
					allPage = jsonT['total'] // 20
				else:
					allPage = jsonT['total'] // 20 + 1
				if pi >= allPage:
					whileTrue = False
					continue
				else:
					pi += 1



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
		if bl.exists(hubInfo.page_url):
			mysql_db_orm.update_ztbHubInfo(update_dict={"craw_status":1},hubInfo_id=hubInfo.id)
			continue
		hhtml = reqSession.GetReHtml(hubInfo.page_url)
		soup = BeautifulSoup(hhtml, 'lxml')

		ztbrawInfo_dict = {}
		hunbInfo_dict = hubInfo.__dict__
		for keyName in hunbInfo_dict.keys():
			if hunbInfo_dict[keyName]:
				ztbrawInfo_dict[keyName] = hunbInfo_dict[keyName]
		articleDetail_html = soup.find('input', attrs={"name":"articleDetail"}).get('value')
		json_html= json.loads(articleDetail_html)
		content_soup = BeautifulSoup(json_html['content'],'lxml')
		ztbrawInfo_dict['content'] = content_soup.prettify()
		regex = re.compile(".*aliyuncs.*")
		attchments = content_soup.find_all(href=regex)
		ztbrawInfo_dict['attachments'] = []
		if attchments:
			for i in attchments:
				ddict = {}
				if 'http' in i.get("href"):
					ddict['download_url'] = i.get("href")
				else:
					ddict['download_url'] = i.get("href").replace('//', 'http://')
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

def singleArticle(url):
	import pprint

	mysql_db_orm = mysql_orm()
	reqSession = req_session(minfo)

	hhtml = reqSession.GetReHtml(url)
	soup = BeautifulSoup(hhtml, 'lxml')

	ztbrawInfo_dict = {}

	articleDetail_html = soup.find('input', attrs={"name": "articleDetail"}).get('value')
	json_html = json.loads(articleDetail_html)
	content_soup = BeautifulSoup(json_html['content'], 'lxml')
	ztbrawInfo_dict['content'] = content_soup.prettify()
	regex = re.compile(".*aliyuncs.*")
	attchments = content_soup.find_all(href=regex)
	ztbrawInfo_dict['attachments'] = []
	if attchments:
		for i in attchments:
			ddict = {}
			if 'http' in i.get("href"):
				ddict['download_url'] = i.get("href")
			else:
				ddict['download_url'] = i.get("href").replace('//', 'http://')
			ddict['download_filename'] = i.get_text()
			ztbrawInfo_dict['attachments'].append(ddict)

	ztbrawInfo_dict['content'] = len(ztbrawInfo_dict['content'])
	pprint.pprint(ztbrawInfo_dict)


	return None

		# rawinfo_id = mysql_db_orm.ztbRawInfo_add_single(hubInfo=hubInfo, articleInfo=ztbrawInfo_dict)
		# if not rawinfo_id:
		# 	continue
		# insertContent = mysql_db_orm.ztbRawInfoContent_add_single(content=ztbrawInfo_dict['content'], rawid=rawinfo_id)
		# if not insertContent:
		# 	mysql_db_orm.session.query(ZtbRawInfo).filter(ZtbRawInfo.id == rawinfo_id).update({"craw_status": 2})
		# 	mysql_db_orm.session.commit()
		# if ztbrawInfo_dict['attachments']:
		# 	mysql_db_orm.ztbInfoAttaChment_add_single(info=ztbrawInfo_dict['attachments'], rawid=rawinfo_id)
		# mysql_db_orm.ztb_Attached_add_single(info=ztbrawInfo_dict, rawid=rawinfo_id)





def main():
	print('qinghai')


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
