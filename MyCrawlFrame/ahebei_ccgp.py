# -*- coding: utf-8 -*-
import tables
import tblib.decorators
from reqSession import *
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
from requests_obj import *
from uxue_orm import *
from requests.adapters import HTTPAdapter
import chardet, cchardet
from urllib import parse as urlpase
from bs4 import BeautifulSoup

mysql_db_orm = mysql_orm()

minfo = {
	"craw_id": "www.ccgp-hebei.gov.cn",
	"site": "www.ccgp-hebei.gov.cn",
	"cookies":False,
	"siteCname": "中国河北政府采购网",
	"HEA": '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Cookie: yunsuo_session_verify=50e4c33d6abd97807f3e6d9b8fada8d8
Host: www.ccgp-hebei.gov.cn
If-Modified-Since: Wed, 22 Dec 2021 01:14:04 GMT
If-None-Match: "14e94-5d3b1d67751f9"
Referer: http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/index_746_1.html
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36''',

	"transmitCookies": False,
	"hub_url": [{'subclass': '招标公告',
	             'url': 'http://search.hebcz.cn:8080/was5/web/search?page={page}&channelid=240117&perpage=50&outlinepage=10&lanmu=zbgg&fstarttime={startime}&fendtime={endtime}'},
	            {'subclass': '中标公告',
	             'url': 'http://search.hebcz.cn:8080/was5/web/search?page={page}&channelid=240117&perpage=50&outlinepage=10&lanmu=zhbgg&fstarttime={startime}&fendtime={endtime}'},
	            {'subclass': '废标公告',
	             'url': 'http://search.hebcz.cn:8080/was5/web/search?page={page}&channelid=240117&perpage=50&outlinepage=10&lanmu=fbgg&fstarttime={startime}&fendtime={endtime}'},
	            {'subclass': '变更公告',
	             'url': 'http://search.hebcz.cn:8080/was5/web/search?page={page}&channelid=240117&perpage=50&outlinepage=10&lanmu=gzgg&fstarttime={startime}&fendtime={endtime}'},
	            {'subclass': '单一来源',
	             'url': 'http://search.hebcz.cn:8080/was5/web/search?page={page}&channelid=240117&perpage=50&outlinepage=10&lanmu=dyly&fstarttime={startime}&fendtime={endtime}'},
	            {'subclass': '合同公告',
	             'url': 'http://search.hebcz.cn:8080/was5/web/search?page={page}&channelid=206382&perpage=50&outlinepage=10&lanmu=htgg&fstarttime={startime}&fendtime={endtime}'},
	            {'subclass': '政府采购意向',
	             'url': 'http://search.hebcz.cn:8080/was5/web/search?page={page}&channelid=218195&perpage=50&outlinepage=10&lanmu=zfcgyx&fstarttime={startime}&fendtime={endtime}'},
	            {'subclass': '政府采购意向变更',
	             'url': 'http://search.hebcz.cn:8080/was5/web/search?page={page}&channelid=218195&perpage=50&outlinepage=10&lanmu=zfcgyxbg&fstarttime={startime}&fendtime={endtime}'},
	            ]
	,

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



def regetTime(llist):
	dlist = []
	for i in llist:
		try:
			reg = re.findall("t(\d{8})_", i['page_url'])[0]
			i['issus_time'] = get_timestr(reg)
		except:
			continue
		dlist.append(i)
	return dlist


def hub_main(inputType, timeL):

	timeInfo = timeL
	if inputType == 'hub':
		hub_url_dupcut = False
		if not timeL:
			timeInfo = datetime.datetime.today().strftime('%Y-%m-%d')
	else:
		hub_url_dupcut = True

	hubrow = request_hub_OBJ(minfo)
	mark = 0
	for urlInfo in minfo['hub_url']:
		for timeL in getBetweenDayList(timeInfo):
			for pageNum in range(1, 100):
				url = urlInfo['url'].format(page=pageNum, startime=timeL, endtime=timeL)
				if hub_url_dupcut:
					if bl.exists(url) or bh.exists(url):
						mark += 1
						continue

				hubListUrl, listinfo = hubrow.get_hubInfo_list(url=url, baseUrl=minfo['site'],
				                                               subclass=urlInfo['subclass'], location='河北省')
				if hubListUrl == 'no link':
					print('nolink', timeL, urlInfo['subclass'], pageNum)
					break
				if listinfo:
					if hub_url_dupcut:
						break
					elif mark == 3:
						mark = 0
						break
					else:
						print('continue', timeL, urlInfo['subclass'], pageNum)
						mark += 1
						continue
				hubListUrl = regetTime(hubListUrl)
				insertall = mysql_db_orm.ztbhubinfo_all_insert(hubListUrl)
				print('-----{},第{}页的  {}  未录入{}'.format(
					timeL,
					pageNum,
					urlInfo['subclass'],
					len(hubListUrl)))
				time.sleep(sleepSec(3, 9))


def articleInfo(url):
	reqsession = req_session(minfo)

	article_html = reqsession.GetReHtml(url=url)
	soup = BeautifulSoup(article_html, 'lxml')

	try:
		title = soup.find(name='meta', attrs={'name': 'ArticleTitle'}).get('content')
	except Exception as errortitle:
		print('error title', url)
		return None

	try:
		issusTime = soup.find(name='meta', attrs={'name': 'PubDate'}).get('content')
	except Exception as errortime:
		try:
			reg = re.findall("t(\d{8})_", url)[0]
			issusTime = get_timestr(reg)
		except:
			print('error time', url)
			return None

	try:
		content_table = soup.find(name='table', attrs={'width': '1022'})
	except Exception as errorcontent:
		print('error content', url)
		return None

	try:
		content_table_input = content_table.find(name='input')
		content_table_input.decompose()
	except:
		pass

	try:
		content_table_navi_bs = content_table.find(name='td', attrs={"id": "navi"})
		content_table_navi_bs.decompose()
	except:
		pass

	content_html = content_table.prettify()

	try:
		content_table_navi = re.compile("<!--导航栏 start-->(.*?)<!--导航栏 end-->", re.S | re.M)
		aa = content_table_navi.search(content_html).group()
		content_html = content_html.replace(aa, '')
	except:
		pass

	jsCut_closewindow = re.compile("(function closeWindow\(\).*?).function", re.S | re.M)
	jsCut_autoIframeHeight = re.compile("(function autoIframeHeight\(.*?).function", re.S | re.M)
	jsCut_functionNavi = re.compile("(\$\(function.\(\).*#navi.*首页.\);.*?);|(\$\(function\(\).*#navi.*首页.\);.*?);",
	                                re.S | re.M)

	jsCodeAll = soup.find(name='script', attrs={"type": "text/javascript", "src": None}).prettify()
	jsCodeAll = re.sub(jsCut_closewindow, 'function', jsCodeAll)
	jsCodeAll = re.sub(jsCut_autoIframeHeight, 'function', jsCodeAll)
	jsCodeAll = re.sub(content_table_navi, '', jsCodeAll)

	jsCodeAll = re.sub(jsCut_functionNavi, '$(function () {content_hebei();})', jsCodeAll)
	jsCodeAll = jsCodeAll.replace('content()', 'content_hebei()')
	fujian_original = []

	try:
		fujian_original = content_table.find(name='span', attrs={"id": "fujian_2020"}).get_text().replace('#filename#',
		                                                                                                  '').split(
			'@_@')
		if not fujian_original[0]:
			fujian_original = []
	except Exception as ffujian:
		pass
	if not fujian_original:
		fujian_original_list = soup.find_all(name='span', attrs={"id": "con"})
		if fujian_original_list:
			regWord = fujian_original_list[0]
			aaaaa = re.findall("#filename#.*?@_@", str(regWord))
			if aaaaa:
				fujian_original = aaaaa[0].replace('#filename#', '').split('@_@')

	attchment = []
	if 'ContractAnncFiles' in soup.prettify():
		fujian_path_ture = 'ContractAnncFiles'
	elif 'BidWinAnncFiles' in soup.prettify():
		fujian_path_ture = 'BidWinAnncFiles'
	elif 'BidInquiryAnncFiles' in soup.prettify():
		fujian_path_ture = 'BidInquiryAnncFiles'
	elif 'BidCorrectionAnncFiles' in soup.prettify():
		fujian_path_ture = 'BidCorrectionAnncFiles'
	else:
		fujian_path_ture = None

	if fujian_original:
		for fujianInfo in fujian_original:
			fujianList = fujianInfo.split('#_#')
			if len(fujianList) > 1:
				ddict = {}
				ddict['download_filename'] = f"{fujianList[0]}.{fujianList[1]}"
				ddict['download_url'] = f"http://www.ccgp-hebei.gov.cn/{fujian_path_ture}/{fujianList[2]}.{fujianList[1]}"
				# print(ddict)
				attchment.append(ddict)
	item = {}
	if attchment:
		item['attchment'] = attchment

	item['title'] = title
	item['issue_time'] = issusTime
	item['content'] = jsCodeAll + content_html
	item['content'] = item['content']
	item['page_url'] = url
	return item



def main():
	print('hebei')


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
			hub_main(inputType='hub', timeL=input_2)
		else:
			hub_main(inputType='hub', timeL='')

	if input_1 == 'manual':
		if not input_2:
			raise '如果使用manual模式，必须输入时间，比如2022-01-01'
		hub_main(inputType=input_1, timeL=input_2)
	if input_1 == 'article':
		get_hubList = mysql_db_orm.session.query(ZtbHubInfo).filter(ZtbHubInfo.craw_status == 0,ZtbHubInfo.site=="www.ccgp-hebei.gov.cn").order_by(
				ZtbHubInfo.issue_time.desc()).limit(300).all()
		if len(get_hubList) == 0:
			get_hubList = None
			exit()
		for hubInfo in get_hubList:
			if bl.exists(hubInfo.page_url):
				continue
			a = articleInfo(hubInfo.page_url)
			if not a:
				aa = mysql_db_orm.update_ztbHubInfo(update_dict={"craw_status":2}, hubInfo_id=hubInfo.id)
				continue
			else:
				aa = mysql_db_orm.update_ztbHubInfo(update_dict={"craw_status":1}, hubInfo_id=hubInfo.id)
			ztb_raw_info_ID = mysql_db_orm.ztbRawInfo_add_single(hubInfo=hubInfo, articleInfo=a)
			if not ztb_raw_info_ID:
				aa = mysql_db_orm.update_ztbHubInfo(update_dict={"craw_status":1}, hubInfo_id=hubInfo.id)
				continue
			mysql_db_orm.ztbRawInfoContent_add_single(content=a['content'], rawid=ztb_raw_info_ID)
			if 'attchment' in a.keys():
				mysql_db_orm.ztbInfoAttaChment_add_single(info=a['attchment'], rawid=ztb_raw_info_ID)
			print(ztb_raw_info_ID)
			hubInfo = None
			a = None
			ddict = None
			ztb_raw_info_ID = None
			time.sleep(sleepSec(3, 9))
		get_hubList = None
		print('the end')

