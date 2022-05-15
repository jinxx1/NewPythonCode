# -*- coding: utf-8 -*-
import json
import pprint
import sys, re,os
import time, datetime
import requests
import lxml
import lxml.html
from lxml.html import HtmlComment
from lxml import etree
from lxml import html as htmlstr
from mkdir import mkdir
from redisBloomHash import bl, bh
from getmysqlInfo import jsonInfo
from crawltools import *
from reqSession import *
from uxue_orm import *
from requests.adapters import HTTPAdapter
import chardet, cchardet
from urllib import parse as urlpase
from bs4 import BeautifulSoup
import json
import platform




minfo = {
    "craw_id": "www.ccgp-beijing.gov.cn",
    "site": "www.ccgp-beijing.gov.cn",
    "siteCname": "北京市政府采购网",
    "HEA": '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Cookie: insert_cookie=43910111; Hm_lvt_eb7ca92154026f45fd611a43a2f63b52=1645432749,1645774885,1646375245,1646718804; Hm_lpvt_eb7ca92154026f45fd611a43a2f63b52=1646718804
Host: www.ccgp-beijing.gov.cn
If-Modified-Since: Sat, 08 Jan 2022 06:01:19 GMT
Referer: http://www.ccgp-beijing.gov.cn/
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36''',
    "transmitCookies": False,
    "cookies": None
}

urlList = [
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbgg/index.html', 'subclass': '招标公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbjggg/index.html', 'subclass': '中标公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjhtgg/index.html', 'subclass': '合同公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjgzgg/index.html', 'subclass': '更正公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjfbgg/index.html', 'subclass': '废标公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjdygg/index.html', 'subclass': '单一公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjqtgg/index.html', 'subclass': '其他公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbgg/index.html', 'subclass': '招标公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbjggg/index.html', 'subclass': '中标公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjhtgg/index.html', 'subclass': '合同公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjgzgg/index.html', 'subclass': '更正公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjfbgg/index.html', 'subclass': '废标公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjdygg/index.html', 'subclass': '单一公告'},
    {'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjqtgg/index.html', 'subclass': '其他公告'}
]



def hub_main(timeL):
    mysql_db_orm = mysql_orm()
    reqSession = req_session(minfo)

    for cateCode in urlList:
        pageS = 100
        breakMark = 0
        whileTrue = 0
        pi = 0

        while pi < 142:
            if pi == 0:
                geturl = cateCode['url']
            else:
                geturl = cateCode['url'].replace('index.html', 'index_{}.html'.format(pi))
            browhtml = reqSession.GetReHtml(url=geturl)
            soup = BeautifulSoup(browhtml, 'lxml')
            li_all = soup.find('ul', attrs={'class': "inner-ul"}).find_all('li')
            li_list = [x for x in li_all]
            if len(li_list) == 0:
                pi = 143
                continue

            allInfo = []
            mark = 0
            for li in li_all:
                ztbhubinfo = {}
                page_url = urlpase.urljoin(cateCode['url'], li.find('a').get('href'))
                if bl.exists(page_url) or bh.exists(page_url):
                    mark += 1
                    continue
                ztbhubinfo['page_url'] = urlpase.urljoin(cateCode['url'], li.find('a').get('href'))

                ztbhubinfo['subclass'] = cateCode['subclass']
                ztbhubinfo['create_time'] = datetime.datetime.now()
                ztbhubinfo['update_time'] = datetime.datetime.now()
                ztbhubinfo['craw_status'] = 1
                ztbhubinfo['site'] = minfo['site']
                ztbhubinfo['craw_id'] = minfo['craw_id']
                ztbhubinfo['issue_time'] = get_timestr(li.find('span', attrs={"class": "datetime"}).get_text())
                ztbhubinfo['title'] = li.find('a').get_text()

                province_name_dict = tureLocation(localName='北京市', title=ztbhubinfo['title'])
                ztbhubinfo['province_name'] = province_name_dict['province_name']
                if province_name_dict['city_name']:
                    ztbhubinfo['city_name'] = province_name_dict['city_name']
                    if len(province_name_dict['city_name']) <= 2:
                        ztbhubinfo['city_name'] = ''
                else:
                    ztbhubinfo['city_name'] = ''
                ztbhubinfo['str1'] = province_name_dict['str1']

                allInfo.append(ztbhubinfo)

            if allInfo:
                aaa = mysql_db_orm.ztbhubinfo_all_insert(allInfo)
                print(aaa)

            log1 = f"{cateCode['subclass']}"
            log = f"本页{len(li_list)}条，未录{len(li_list) - mark}篇，第{pi}页，{timeL}"
            print(log1)
            print(log)
            print('--------------------------------------------')

            if mark == len(li_list):
                breakMark += 1
                print("breakMark += 1", breakMark)
            else:
                breakMark = 0

            if breakMark == 5:
                pi = 143
                continue

            pi += 1
            time.sleep(sleepSec(3, 5))



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
            mysql_db_orm.update_ztbHubInfo({"craw_status": 1}, hubInfo.id)
            continue
        hhtml = reqSession.GetReHtml(hubInfo.page_url)
        soup_index = BeautifulSoup(hhtml, 'lxml')
        soupHtml = soup_index.find("div", attrs={"id": "mainText"})

        ztbrawInfo_dict = {}

        hunbInfo_dict = hubInfo.__dict__
        for keyName in hunbInfo_dict.keys():
            if hunbInfo_dict[keyName]:
                ztbrawInfo_dict[keyName] = hunbInfo_dict[keyName]

        ztbrawInfo_dict['content'] = soupHtml.prettify()

        attsouplist = soupHtml.find_all('a', href=re.compile('.*\..*'))
        if attsouplist:
            ztbrawInfo_dict["attchments"] = []
            for i in attsouplist:
                ddict = {}
                ddict['download_url'] = urlpase.urljoin(hubInfo.page_url,i.get('href'))
                ddict['download_filename'] = i.get_text()
                if not os.path.splitext(ddict['download_filename'])[-1]:
                    continue
                ztbrawInfo_dict["attchments"].append(ddict)
            if not ztbrawInfo_dict["attchments"]:
                del ztbrawInfo_dict["attchments"]




        rawid = mysql_db_orm.insertInfo(ztbrawInfo_dict,hubInfo.id)
        ztbrawInfo_dict['content'] = len(ztbrawInfo_dict['content'])
        pprint.pprint(ztbrawInfo_dict)
        if rawid:
            mysql_db_orm.update_ztbHubInfo(update_dict={"craw_status": 1},hubInfo_id=hubInfo.id)
        else:
            mysql_db_orm.update_ztbHubInfo(update_dict={"craw_status": 3, 'str2': f"录入失败，未知错误"[:254]},
                                       hubInfo_id=hubInfo.id)
        print('------------------------------------------------',rawid)
        time.sleep(sleepSec(3, 5))


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

