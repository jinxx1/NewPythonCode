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
	"craw_id": "www.ccgp-liaoning.gov.cn",
	"site": "www.ccgp-liaoning.gov.cn",
	"siteCname": "辽宁政府采购网",
	"HEA": '''Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Content-Length: 154
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: UqZBpD3n3iXPAw1X9E/skHKTXvkP4MMYVsrD6tfF81w@=v1Vn7rsn2go00; JSESSIONID=49E6F2DCC2A560578E437A60631BCBB9
Host: www.ccgp-liaoning.gov.cn
Origin: http://www.ccgp-liaoning.gov.cn
Referer: http://www.ccgp-liaoning.gov.cn/portalindex.do?method=goPubInfoList&infoType=1001
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36
X-Requested-With: XMLHttpRequest''',
	"transmitCookies": False,
	"cookies": None
}


def hub_main(timeL):
	mysql_db_orm = mysql_orm()
	reqSession = req_session(minfo)

	baseUrl = "http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoList&t_k=null"
	urlList = [
	{'subclass': '采购公告', 'code': 1001},
	           {'subclass': '单一来源公示', 'code': 1008},
	           {'subclass': '结果公告', 'code': 1002},
	           {'subclass': '其他公示', 'code': 1007},
	           {'subclass': '更正公告', 'code': 1003}
	           ]
	for cateCode in urlList:
		pageS = 100
		breakMark = 0
		whileTrue = True
		pi = 1

		while whileTrue:
			postdate = {"current": str(pi), "rowCount": str(pageS), "releaseDateStart": timeL, "releaseDateEnd": timeL,
			            "infoTypeCode": str(cateCode['code'])}
			jsonT = reqSession.PostResult(posturl=baseUrl, postdate=postdate, jsonT=1)
			allInfo = []
			print(len(jsonT['rows']),timeL)
			if len(jsonT['rows']) == 0:
				whileTrue = False
				continue
			mark = 0
			for jsoninfo in jsonT['rows']:
				ztbhubinfo = ZtbHubInfo()
				ztbhubinfo.page_url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoViewOpen&infoId=' + \
				                      jsoninfo['id']
				if bl.exists(ztbhubinfo.page_url) or bh.exists(ztbhubinfo.page_url):
					mark += 1
					continue
				ztbhubinfo.craw_status = 0
				ztbhubinfo.create_time = datetime.datetime.now()
				ztbhubinfo.update_time = datetime.datetime.now()
				ztbhubinfo.site = minfo['site']
				ztbhubinfo.craw_id = minfo['craw_id']
				ztbhubinfo.issue_time = get_timestr(jsoninfo['releaseDate'])
				ztbhubinfo.title = jsoninfo['title']

				province_name_dict = tureLocation(localName='辽宁省', title=ztbhubinfo.title)
				ztbhubinfo.province_name = province_name_dict['province_name']
				if province_name_dict['city_name']:
					ztbhubinfo.city_name = province_name_dict['city_name']
					if len(province_name_dict['city_name']) <= 2:
						ztbhubinfo.city_name = ''
				else:
					ztbhubinfo.city_name = ''
				try:
					ztbhubinfo.str1 = jsoninfo['district']
				except:
					ztbhubinfo.str1 = province_name_dict['str1']

				try:
					ztbhubinfo.purchase_type = jsoninfo['infoTypeName']
				except:
					pass
				ztbhubinfo.subclass = ''
				allInfo.append(ztbhubinfo.__dict__)

			if allInfo:
				mysql_db_orm.ztbhubinfo_all_insert(allInfo)

			log1 = f"{cateCode['subclass']}"
			log = f"本页{len(jsonT['rows'])}条，未录{len(jsonT['rows']) - mark}篇，共{jsonT['total']}篇，第{pi}页，{timeL}"
			print(log1)
			print(log)
			print(postdate)
			print('--------------------------------------------')

			if mark == len(jsonT['rows']):
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
			time.sleep(sleepSec(3, 5))


def article_main():
	mysql_db_orm = mysql_orm()
	reqSession = req_session(minfo)

	get_hubList = mysql_db_orm.session.query(ZtbHubInfo).filter(ZtbHubInfo.craw_status == 0,
	                                                            ZtbHubInfo.site == minfo['site']).order_by(
		ZtbHubInfo.issue_time.desc()).limit(300).all()
	# hubpageurl = "http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoViewOpen&infoId=-14872a0b17ee3fe9910-60c9"
	# get_hubList = mysql_db_orm.session.query(ZtbHubInfo).filter(ZtbHubInfo.page_url == hubpageurl).all()
	print(len(get_hubList))


	if not get_hubList:
		return None
	for hubInfo in get_hubList:
		if bl.exists(hubInfo.page_url):
			mysql_db_orm.update_ztbHubInfo({"craw_status":1},hubInfo.id)
			continue
		hhtml = reqSession.GetReHtml(hubInfo.page_url)
		soup_index = BeautifulSoup(hhtml, 'lxml')
		soupHtml = soup_index.find("div",attrs={"id":"template"}).get_text()
		soup = BeautifulSoup(soupHtml,'lxml')
		ztbrawInfo_dict = {}

		hunbInfo_dict = hubInfo.__dict__
		for keyName in hunbInfo_dict.keys():
			if hunbInfo_dict[keyName]:
				ztbrawInfo_dict[keyName] = hunbInfo_dict[keyName]

		regex = re.compile("thisform|nform")
		try:
			ztbrawInfo_dict['content'] = soup.find('form', attrs={"name": regex}).find('table').prettify()
		except Exception as fform:
			mysql_db_orm.update_ztbHubInfo(update_dict={"craw_status":2,"str2":fform[:254]})
			continue


		rawinfo_id = mysql_db_orm.ztbRawInfo_add_single(hubInfo=hubInfo, articleInfo=ztbrawInfo_dict)
		if not rawinfo_id:
			continue
		insertContent = mysql_db_orm.ztbRawInfoContent_add_single(content=ztbrawInfo_dict['content'], rawid=rawinfo_id)
		if not insertContent:
			mysql_db_orm.session.query(ZtbRawInfo).filter(ZtbRawInfo.id == rawinfo_id).update({"craw_status": 2})
			mysql_db_orm.session.commit()

		mysql_db_orm.ztb_Attached_add_single(info=ztbrawInfo_dict, rawid=rawinfo_id)
		time.sleep(sleepSec(3, 9))



def main():
	print('liaoning')

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
