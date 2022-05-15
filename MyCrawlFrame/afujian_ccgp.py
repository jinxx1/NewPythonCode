# -*- coding: utf-8 -*-
import json
import pprint
from urllib.parse import quote
import sys, re, os
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
from web_driver import webdriver_getCookie_fujian
from requests.adapters import HTTPAdapter
import chardet, cchardet
from urllib import parse as urlpase
from bs4 import BeautifulSoup
import platform

sys_code = platform.system()

if sys_code == 'Windows':
    codeimgPath = r"D:/PythonCode/MyCrawlFrame/orcpic/code_fujian.png"
    cookiesPath = r"D:/PythonCode/MyCrawlFrame/orcpic/cookies_fujian.json"
elif sys_code == 'Linux':
    codeimgPath = "/home/terry/i139/mcf/codeimgpath/code_fujian.png"
    cookiesPath = "/home/terry/i139/mcf/codeimgpath/cookies_fujian.json"
else:
    raise 'Opertion System is not Windows or Linux, Exiting Program'

minfo = {
    "craw_id": "www.ccgp-fujian.gov.cn",
    "site": "www.ccgp-fujian.gov.cn",
    "siteCname": "福建省政府采购网",
    "HEA": '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Host: www.ccgp-fujian.gov.cn
Referer: http://www.ccgp-fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/?csrfmiddlewaretoken=cXqbP3dIaB8gkGeZxj8vOncoFpULXyDz0Eux1pAexZT3Dgjc4QlaNMgrMXtlGcu2&zone_code=&zone_name=&croporgan_name=&project_no=&fromtime=2022-01-01&endtime=2022-04-06&gpmethod=%E7%AB%9E%E4%BA%89%E6%80%A7%E8%B0%88%E5%88%A4&agency_name=&title=&notice_type=b716da75fe8d4e4387f5a8c72ac2a937&open_type=
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36''',
    "transmitCookies": False,
    "cookies": None
}

urlList = [
    {'purchaseName': '采购公告', 'purchaseCode': '463fa57862ea4cc79232158f5ed02d03', 'subclassName': '公开招标'},
    {'purchaseName': '资格预审公告', 'purchaseCode': 'ac97d61fa3734f16a266822e697c8763', 'subclassName': '公开招标'},
    {'purchaseName': '更正公告', 'purchaseCode': '7dc00df822464bedbf9e59d02702b714', 'subclassName': '公开招标'},
    {'purchaseName': '结果公告', 'purchaseCode': 'b716da75fe8d4e4387f5a8c72ac2a937', 'subclassName': '公开招标'},
    {'purchaseName': '结果更正公告', 'purchaseCode': 'd812e46569204c7fbd24cbe9866d0651', 'subclassName': '公开招标'},
    {'purchaseName': '合同公告', 'purchaseCode': '1d5eac5cd0b14515aacaf2e9aee5f928', 'subclassName': '公开招标'},
    {'purchaseName': '网上超市合同', 'purchaseCode': 'ce932df3036340559c19acc4935c04b9', 'subclassName': '公开招标'},
    {'purchaseName': '单一来源公示', 'purchaseCode': '255e087cf55a42139a1f1b176b244ebb', 'subclassName': '公开招标'},
    {'purchaseName': '补充公告', 'purchaseCode': '30f19b25203f11e8b43a060400ef5315', 'subclassName': '公开招标'},
    {'purchaseName': '中标预公示', 'purchaseCode': '30f19b24203f11e8b43a060400ef5315', 'subclassName': '公开招标'},
    {'purchaseName': '采购意向公开', 'purchaseCode': '8fd455f244cc11eb88b50cda411d946b', 'subclassName': '公开招标'},
    {'purchaseName': '资格预审公告', 'purchaseCode': 'ac97d61fa3734f16a266822e697c8763', 'subclassName': '竞争性谈判'},
    {'purchaseName': '采购公告', 'purchaseCode': '463fa57862ea4cc79232158f5ed02d03', 'subclassName': '竞争性谈判'},
    {'purchaseName': '更正公告', 'purchaseCode': '7dc00df822464bedbf9e59d02702b714', 'subclassName': '竞争性谈判'},
    {'purchaseName': '结果公告', 'purchaseCode': 'b716da75fe8d4e4387f5a8c72ac2a937', 'subclassName': '竞争性谈判'},
    {'purchaseName': '结果更正公告', 'purchaseCode': 'd812e46569204c7fbd24cbe9866d0651', 'subclassName': '竞争性谈判'},
    {'purchaseName': '合同公告', 'purchaseCode': '1d5eac5cd0b14515aacaf2e9aee5f928', 'subclassName': '竞争性谈判'},
    {'purchaseName': '网上超市合同', 'purchaseCode': 'ce932df3036340559c19acc4935c04b9', 'subclassName': '竞争性谈判'},
    {'purchaseName': '单一来源公示', 'purchaseCode': '255e087cf55a42139a1f1b176b244ebb', 'subclassName': '竞争性谈判'},
    {'purchaseName': '补充公告', 'purchaseCode': '30f19b25203f11e8b43a060400ef5315', 'subclassName': '竞争性谈判'},
    {'purchaseName': '中标预公示', 'purchaseCode': '30f19b24203f11e8b43a060400ef5315', 'subclassName': '竞争性谈判'},
    {'purchaseName': '采购意向公开', 'purchaseCode': '8fd455f244cc11eb88b50cda411d946b', 'subclassName': '竞争性谈判'},
    {'purchaseName': '资格预审公告', 'purchaseCode': 'ac97d61fa3734f16a266822e697c8763', 'subclassName': '竞争性磋商'},
    {'purchaseName': '采购公告', 'purchaseCode': '463fa57862ea4cc79232158f5ed02d03', 'subclassName': '竞争性磋商'},
    {'purchaseName': '更正公告', 'purchaseCode': '7dc00df822464bedbf9e59d02702b714', 'subclassName': '竞争性磋商'},
    {'purchaseName': '结果公告', 'purchaseCode': 'b716da75fe8d4e4387f5a8c72ac2a937', 'subclassName': '竞争性磋商'},
    {'purchaseName': '结果更正公告', 'purchaseCode': 'd812e46569204c7fbd24cbe9866d0651', 'subclassName': '竞争性磋商'},
    {'purchaseName': '合同公告', 'purchaseCode': '1d5eac5cd0b14515aacaf2e9aee5f928', 'subclassName': '竞争性磋商'},
    {'purchaseName': '网上超市合同', 'purchaseCode': 'ce932df3036340559c19acc4935c04b9', 'subclassName': '竞争性磋商'},
    {'purchaseName': '单一来源公示', 'purchaseCode': '255e087cf55a42139a1f1b176b244ebb', 'subclassName': '竞争性磋商'},
    {'purchaseName': '补充公告', 'purchaseCode': '30f19b25203f11e8b43a060400ef5315', 'subclassName': '竞争性磋商'},
    {'purchaseName': '中标预公示', 'purchaseCode': '30f19b24203f11e8b43a060400ef5315', 'subclassName': '竞争性磋商'},
    {'purchaseName': '采购意向公开', 'purchaseCode': '8fd455f244cc11eb88b50cda411d946b', 'subclassName': '竞争性磋商'},
    {'purchaseName': '资格预审公告', 'purchaseCode': 'ac97d61fa3734f16a266822e697c8763', 'subclassName': '单一来源'},
    {'purchaseName': '采购公告', 'purchaseCode': '463fa57862ea4cc79232158f5ed02d03', 'subclassName': '单一来源'},
    {'purchaseName': '更正公告', 'purchaseCode': '7dc00df822464bedbf9e59d02702b714', 'subclassName': '单一来源'},
    {'purchaseName': '结果公告', 'purchaseCode': 'b716da75fe8d4e4387f5a8c72ac2a937', 'subclassName': '单一来源'},
    {'purchaseName': '结果更正公告', 'purchaseCode': 'd812e46569204c7fbd24cbe9866d0651', 'subclassName': '单一来源'},
    {'purchaseName': '合同公告', 'purchaseCode': '1d5eac5cd0b14515aacaf2e9aee5f928', 'subclassName': '单一来源'},
    {'purchaseName': '网上超市合同', 'purchaseCode': 'ce932df3036340559c19acc4935c04b9', 'subclassName': '单一来源'},
    {'purchaseName': '单一来源公示', 'purchaseCode': '255e087cf55a42139a1f1b176b244ebb', 'subclassName': '单一来源'},
    {'purchaseName': '补充公告', 'purchaseCode': '30f19b25203f11e8b43a060400ef5315', 'subclassName': '单一来源'},
    {'purchaseName': '中标预公示', 'purchaseCode': '30f19b24203f11e8b43a060400ef5315', 'subclassName': '单一来源'},
    {'purchaseName': '采购意向公开', 'purchaseCode': '8fd455f244cc11eb88b50cda411d946b', 'subclassName': '单一来源'},
    {'purchaseName': '资格预审公告', 'purchaseCode': 'ac97d61fa3734f16a266822e697c8763', 'subclassName': '邀请招标'},
    {'purchaseName': '采购公告', 'purchaseCode': '463fa57862ea4cc79232158f5ed02d03', 'subclassName': '邀请招标'},
    {'purchaseName': '更正公告', 'purchaseCode': '7dc00df822464bedbf9e59d02702b714', 'subclassName': '邀请招标'},
    {'purchaseName': '结果公告', 'purchaseCode': 'b716da75fe8d4e4387f5a8c72ac2a937', 'subclassName': '邀请招标'},
    {'purchaseName': '结果更正公告', 'purchaseCode': 'd812e46569204c7fbd24cbe9866d0651', 'subclassName': '邀请招标'},
    {'purchaseName': '合同公告', 'purchaseCode': '1d5eac5cd0b14515aacaf2e9aee5f928', 'subclassName': '邀请招标'},
    {'purchaseName': '网上超市合同', 'purchaseCode': 'ce932df3036340559c19acc4935c04b9', 'subclassName': '邀请招标'},
    {'purchaseName': '单一来源公示', 'purchaseCode': '255e087cf55a42139a1f1b176b244ebb', 'subclassName': '邀请招标'},
    {'purchaseName': '补充公告', 'purchaseCode': '30f19b25203f11e8b43a060400ef5315', 'subclassName': '邀请招标'},
    {'purchaseName': '中标预公示', 'purchaseCode': '30f19b24203f11e8b43a060400ef5315', 'subclassName': '邀请招标'},
    {'purchaseName': '采购意向公开', 'purchaseCode': '8fd455f244cc11eb88b50cda411d946b', 'subclassName': '邀请招标'},
    {'purchaseName': '资格预审公告', 'purchaseCode': 'ac97d61fa3734f16a266822e697c8763', 'subclassName': '询价采购'},
    {'purchaseName': '采购公告', 'purchaseCode': '463fa57862ea4cc79232158f5ed02d03', 'subclassName': '询价采购'},
    {'purchaseName': '更正公告', 'purchaseCode': '7dc00df822464bedbf9e59d02702b714', 'subclassName': '询价采购'},
    {'purchaseName': '结果公告', 'purchaseCode': 'b716da75fe8d4e4387f5a8c72ac2a937', 'subclassName': '询价采购'},
    {'purchaseName': '结果更正公告', 'purchaseCode': 'd812e46569204c7fbd24cbe9866d0651', 'subclassName': '询价采购'},
    {'purchaseName': '合同公告', 'purchaseCode': '1d5eac5cd0b14515aacaf2e9aee5f928', 'subclassName': '询价采购'},
    {'purchaseName': '网上超市合同', 'purchaseCode': 'ce932df3036340559c19acc4935c04b9', 'subclassName': '询价采购'},
    {'purchaseName': '单一来源公示', 'purchaseCode': '255e087cf55a42139a1f1b176b244ebb', 'subclassName': '询价采购'},
    {'purchaseName': '补充公告', 'purchaseCode': '30f19b25203f11e8b43a060400ef5315', 'subclassName': '询价采购'},
    {'purchaseName': '中标预公示', 'purchaseCode': '30f19b24203f11e8b43a060400ef5315', 'subclassName': '询价采购'},
    {'purchaseName': '采购意向公开', 'purchaseCode': '8fd455f244cc11eb88b50cda411d946b', 'subclassName': '询价采购'}
]

baseUrl = "http://www.ccgp-fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/?page={pageNum}&csrfmiddlewaretoken={token}&zone_code=&zone_name=&croporgan_name=&project_no=&fromtime={startime}&endtime={endtime}&gpmethod={subclass}&agency_name=&title=&notice_type={purchaseCode}&open_type=&verifycode={verifycode}"

code_chaojiying = 2004  # 四个数字


def get_cookies():
    testUrl = "http://www.ccgp-fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/?page=2&endtime=2022-04-06&gpmethod=%E7%AB%9E%E4%BA%89%E6%80%A7%E8%B0%88%E5%88%A4&notice_type=b716da75fe8d4e4387f5a8c72ac2a937&fromtime=2022-01-01"
    from_json_getCookies = openJson(path=cookiesPath)
    headers_formjson = creatHeader(minfo['HEA'])
    headers_formjson['Referer'] = from_json_getCookies['Referer']

    brow = requests.get(url=testUrl, timeout=(20, 20), headers=headers_formjson,
                        cookies=from_json_getCookies['cookies'])
    soup = BeautifulSoup(brow.text, 'lxml')
    links = soup.find_all('tr', attrs={'class': 'gradeX'})
    csrtoken = soup.find('input', attrs={"name": "csrfmiddlewaretoken"}).get("value")
    if len(links) == 10:

        return {"cookies": from_json_getCookies['cookies'],
                "csrfmiddlewaretoken": csrtoken,
                'pic_str': from_json_getCookies['pic_str'],
                'Referer': from_json_getCookies['Referer']
                }
    else:
        print('本地cookies，无效！！使用wd重新获取本地cookies')
        return wd_get_cookies()


def wd_get_cookies():
    getCookiesUrl = "http://www.ccgp-fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/"
    from_wd_getCookies = webdriver_getCookie_fujian(url=getCookiesUrl, path=codeimgPath, code=code_chaojiying)
    soup = BeautifulSoup(from_wd_getCookies['html'], 'lxml')
    csrtoken = soup.find('input', attrs={"name": "csrfmiddlewaretoken"}).get("value")
    del from_wd_getCookies['html']

    writeJson(path=cookiesPath, jsonT=from_wd_getCookies)

    return {"cookies": from_wd_getCookies['cookies'],
            "csrfmiddlewaretoken": csrtoken,
            'pic_str': from_wd_getCookies['pic_str'],
            'Referer': from_wd_getCookies['Referer']}


def hub_main(timeL):
    timeStartArray = time.strptime(timeL, '%Y-%m-%d')
    timeStartStamp = time.mktime(timeStartArray)
    endStamp = int(timeStartStamp) + 86400
    timeStartA = time.localtime(timeStartStamp)
    endStartA = time.localtime(endStamp)
    TIMESTART = time.strftime("%Y-%m-%d", timeStartA)
    TIMEEND = time.strftime("%Y-%m-%d", endStartA)

    mysql_db_orm = mysql_orm()
    requests_cookies = get_cookies()

    for i in urlList:

        pageNum = 1
        breakMark = 0
        whileTrue = True
        while whileTrue:

            getUrl = baseUrl.format(
                pageNum=pageNum,
                token=requests_cookies['csrfmiddlewaretoken'],
                startime=TIMESTART,
                endtime=TIMEEND,
                purchaseCode=i['purchaseCode'],
                verifycode=quote(requests_cookies['pic_str'], 'utf-8'),
                subclass=quote(i['subclassName'], 'utf-8'),
            )

            header_temp = creatHeader(minfo['HEA'])
            header_temp['Referer'] = requests_cookies['Referer']

            brow = requests.get(url=getUrl,
                                timeout=(20, 20),
                                headers=header_temp,
                                cookies=requests_cookies['cookies'])

            requests_cookies['Referer'] = getUrl

            soup = BeautifulSoup(brow.text, 'lxml')
            wrapTable_soup = soup.find('div', attrs={"class": "wrapTable"})
            if '暂无数据' in wrapTable_soup.prettify():
                print(i['purchaseName'], i['subclassName'], pageNum, TIMESTART, TIMEEND)
                print(getUrl)
                print('-------------------暂无数据--------------------------------------------')
                whileTrue = False
                continue
            if '请完成上方验证码操作' in wrapTable_soup.prettify():
                print(i['purchaseName'], i['subclassName'], pageNum, TIMESTART, TIMEEND)
                print(getUrl)
                print('------------------cookies ERROR---------------------------------------------')
                requests_cookies = wd_get_cookies()
                continue

            info_all = wrapTable_soup.find_all('tr', attrs={'class': 'gradeX'})
            mark = 0
            llist = []
            for info in info_all:
                ele = info.find_all('td')
                location = str(ele[0].get_text())
                tender = str(ele[2].get_text())
                url_temp = ele[3].find('a').get('href')
                title = ele[3].find('a').get_text()
                times = str(ele[4].get_text())

                article_Url = urlpase.urljoin(base='http://www.ccgp-fujian.gov.cn', url=url_temp)
                if bl.exists(article_Url) or bh.exists(article_Url):
                    mark += 1
                    continue
                ztbhubinfo = ZtbHubInfo()
                ztbhubinfo.craw_status = 0
                ztbhubinfo.create_time = datetime.datetime.now()
                ztbhubinfo.update_time = datetime.datetime.now()
                ztbhubinfo.site = minfo['site']
                ztbhubinfo.craw_id = minfo['craw_id']
                ztbhubinfo.page_url = article_Url
                ztbhubinfo.title = title
                ztbhubinfo.issue_time = get_timestr(times)
                ztbhubinfo.subclass = i['subclassName']
                ztbhubinfo.purchase_type = i['purchaseName']
                ztbhubinfo.ztb_project_tenderer = tender[:20]

                province_name_dict = tureLocation(localName='福建省', title=location + ztbhubinfo.title)
                ztbhubinfo.province_name = province_name_dict['province_name']
                if province_name_dict['city_name']:
                    ztbhubinfo.city_name = province_name_dict['city_name']
                    if len(province_name_dict['city_name']) <= 2:
                        ztbhubinfo.city_name = ''
                else:
                    ztbhubinfo.city_name = ''
                llist.append(ztbhubinfo.__dict__)
                pprint.pprint(ztbhubinfo.__dict__)
                print(ztbhubinfo.subclass, ztbhubinfo.purchase_type, pageNum, TIMESTART, TIMEEND)
                print('------------------------------------------')
                writeJson(path=cookiesPath, jsonT=requests_cookies)

            if llist:
                mysql_db_orm.ztbhubinfo_all_insert(llist)

            if mark == len(info_all):
                breakMark += 1
                print("breakMark += 1", breakMark)
            else:
                breakMark = 0

            if breakMark == 3:
                whileTrue = False
                continue

            get_pageCountEle = soup.find('button', attrs={"type": "button"}, text=re.compile("末页"))
            if get_pageCountEle:
                allPage = int(re.findall("page=(\d{1,10})", get_pageCountEle.get('onclick'))[0])
            else:
                allPage = 0

            if pageNum >= allPage:
                whileTrue = False
                continue
            else:
                pageNum += 1

            time.sleep(sleepSec(3, 5))


def article_main():
    mysql_db_orm = mysql_orm()

    get_hubList = mysql_db_orm.session.query(ZtbHubInfo).filter(ZtbHubInfo.craw_status == 0,
                                                                ZtbHubInfo.site == minfo['site']).order_by(
        ZtbHubInfo.issue_time.desc()).limit(300).all()
    print(len(get_hubList))

    pprint.pprint(get_hubList)
    if not get_hubList:
        return None

    for hubInfo in get_hubList:
        # if bl.exists(hubInfo.page_url):
        # 	continue
        header_temp = creatHeader(minfo['HEA'])
        brow = requests.get(url=hubInfo.page_url, headers=header_temp)
        soup = BeautifulSoup(brow.text, 'lxml')

        ztbrawInfo_dict = {}

        hunbInfo_dict = hubInfo.__dict__
        for keyName in hunbInfo_dict.keys():
            if hunbInfo_dict[keyName]:
                ztbrawInfo_dict[keyName] = hunbInfo_dict[keyName]


        content = soup.find('div', class_="notice-con")
        style_tag = content.find_all(name=re.compile('style|input'))
        for i in style_tag:
            i.decompose()

        null_tag = content.find_all(name=re.compile('div'),class_=re.compile('hide'))
        for i in null_tag:
            i.decompose()

        ztbrawInfo_dict['content'] = content.prettify()


        attchments = soup.find_all(href=re.compile("upload|conractnotice"))
        ztbrawInfo_dict['attachments'] = []
        if attchments:
            for i in attchments:
                ddict = {}

                att_url = i.get("href")
                if 'http://' in att_url or 'https://' in att_url:
                    ddict['download_url'] = att_url
                else:
                    ddict['download_url'] = urlpase.urljoin(base='http://www.ccgp-fujian.gov.cn/', url=att_url)
                if not ddict['download_url']:
                    continue

                ddict['download_filename'] = i.get_text() + '.html'
                ztbrawInfo_dict['attachments'].append(ddict)

        mysql_db_orm.insertInfo(ztbrawInfo_dict,hubInfo.id)
        ztbrawInfo_dict['content'] = len(ztbrawInfo_dict['content'])
        pprint.pprint(ztbrawInfo_dict)
        print('---------------------------')
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
            hub_main(timeL=str(datetime.date.today()))

    if input_1 == 'article':
        article_main()
