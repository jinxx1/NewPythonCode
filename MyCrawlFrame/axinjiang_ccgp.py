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
	"craw_id": "www.ccgp-xinjiang.gov.cn",
	"site": "www.ccgp-xinjiang.gov.cn",
	"siteCname": "新疆政府采购网",
	"HEA": '''Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: close
Content-Length: 162
Content-Type: application/json
Host: www.ccgp-xinjiang.gov.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36
X-Requested-With: XMLHttpRequest''',
	"transmitCookies": False,
	"cookies": None,
	"posturl": "http://www.ccgp-xinjiang.gov.cn/front/search/category",
}

sub_and_codeList = [{'subclass': '采购意向', 'code': 'ZcyAnnouncement11'},
                    {'subclass': '采购项目公告', 'code': 'ZcyAnnouncement2'},
                    {'subclass': '采购公示', 'code': 'ZcyAnnouncement1'},
                    {'subclass': '采购结果公告', 'code': 'ZcyAnnouncement4'},
                    {'subclass': '澄清变更公告', 'code': 'ZcyAnnouncement3'},
                    {'subclass': '采购合同公告', 'code': 'ZcyAnnouncement5'},
                    {'subclass': '履约验收', 'code': 'ZcyAnnouncement6'},
                    # {'subclass': '电子卖场公告', 'code': 'ZcyAnnouncement8'},
                    {'subclass': '非政府采购公告', 'code': 'ZcyAnnouncement9'},
                    {'subclass': '废标公告', 'code': 'ZcyAnnouncement10'}]
location_codeList = [["659900"], ["650", "652", "653", "654", "659099"]]

def hub_main(timeL):
	mysql_db_orm = mysql_orm()
	reqSession = req_session(minfo)
	pageS = 50

	for cateCode in sub_and_codeList:
		for lo in location_codeList:
			breakMark = 0
			whileTrue = True
			pi = 1
			while whileTrue:

				postdate = {"pageNo": pi,
				            "pageSize": pageS,
				            "categoryCode": cateCode['code'],
				            "districtCode": lo,
				            "publishDateBegin": str(timeL), 'publishDateEnd': str(timeL)}
				import pprint
				pprint.pprint(postdate)


				originBrow = reqSession.PostResult(posturl=minfo['posturl'], postdate=json.dumps(postdate), jsonT=1)
				jsonT = originBrow['hits']
				mark = 0
				hubinfoList = []
				if len(jsonT['hits']) == 0:
					whileTrue = False
					continue
				for info in jsonT['hits']:
					ZtbHubInfo_obj = ZtbHubInfo()
					ZtbHubInfo_obj.page_url = 'http://www.ccgp-xinjiang.gov.cn' + info['_source']['url']
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

					province_name_dict = tureLocation(localName='新疆', title=ZtbHubInfo_obj.title)
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
				print(postdate)
				print('--------------------------------------------')

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
				time.sleep(sleepSec(2, 5))


def article_main():
	mysql_db_orm = mysql_orm()
	reqSession = req_session(minfo)

	get_hubList = mysql_db_orm.session.query(ZtbHubInfo).filter(ZtbHubInfo.craw_status == 0,
	                                                            ZtbHubInfo.site == minfo['site']).order_by(
		ZtbHubInfo.issue_time.desc()).limit(300).all()
	if not get_hubList:
		return None
	for hubInfo in get_hubList:
		# if bl.exists(hubInfo.page_url):
		# 	continue
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
				ddict['download_url'] = i.get("href").replace('http://', '//').replace('//', 'http://')
				ddict['download_filename'] = i.get_text()
				ztbrawInfo_dict['attachments'].append(ddict)

		rawinfo_id = mysql_db_orm.ztbRawInfo_add_single(hubInfo=hubInfo, articleInfo=ztbrawInfo_dict)
		if not rawinfo_id or rawinfo_id == 1:
			continue

		insertContent = mysql_db_orm.ztbRawInfoContent_add_single(content=ztbrawInfo_dict['content'], rawid=rawinfo_id)
		if not insertContent:
			mysql_db_orm.session.query(ZtbRawInfo).filter(ZtbRawInfo.id == rawinfo_id).update({"craw_status": 2})
			mysql_db_orm.session.commit()
		if ztbrawInfo_dict['attachments']:
			mysql_db_orm.ztbInfoAttaChment_add_single(info=ztbrawInfo_dict['attachments'], rawid=rawinfo_id)

		mysql_db_orm.ztb_Attached_add_single(info=ztbrawInfo_dict, rawid=rawinfo_id)
		print('-----------------------------------')
		time.sleep(sleepSec(2, 5))


def main():
	print('xinjiang')


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
