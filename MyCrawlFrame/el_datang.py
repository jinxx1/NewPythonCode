# -*- coding: utf-8 -*-
import json
import pprint
import sys, re
import time, datetime
import requests
import lxml
import pprint
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
from wdobj import wdriver
from reqSession import req_session

minfo = {
    "craw_id": "www.cdt-ec.com",
    "site": "www.cdt-ec.com",
    "siteCname": "大唐电子商务中心",
    "HEA": '''Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Content-Length: 132
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: _uab_collina=164645451498362828991708; acw_tc=2760778a16465668287475927e7ecb313cb510ca29eedd23408afc1fac2791; acw_sc__v2=62249dee31654fa44ad6dbaa8a0521c767bec817; JSESSIONID=4F98458A6E790DBFB680114C15B66C65; ssxmod_itna=eqUxgDniqGq400DzhKRx0KeKWqIAaZ7YxYTP0QHDl=0oxA5D8D6DQeGTbnYQNIN32o4haqa=0iE56+0QgRaKi2OPusq3ox0aDbqGkAnzb4GG0xBYDQxAYDGDDPCDj4ibDYfzODjBItzZCq=D3qDwDB=DmqG2Kn=Dm4DfDDdyigx4z06MS32xHeDSigUxK0=DjqGgDBdtFaTDGwaHsAXMK6W83hDDCEmxB1DeBPqhQDGWFx6qNeGuDG=5LMLPg=UVRLjw=xhaYMvbIAfxiEhezDP=QOopK7eWWxqQChxifV4oib+5DD3y6AWgTDD=; ssxmod_itna2=eqUxgDniqGq400DzhKRx0KeKWqIAaZ7YxYTP0QD6ERcD05box03qCN7no77QpXDnRD8NAhbYv+nDKe2bmt61W7Ep=rxa7Fw7cKn8y6ssbQ3r2xgb1Bcfsrul1SBYeKVlbtyH8Bp29K7D/S+D4E209QRU98LolBu2quL6lbdQ9Ybb0Gu6K=M05EERoVkW+ecYdpqiWda2QNat7HcUFv=UZ/mKKLdb+n=tQQpW7xS9xbpaOZqFkp1775/98oKW7=lFpuF9zH+xLwcAEpPEkqFd6q5luNCX9EtlehlFX=+M=u=lwp1GaHPC7ksLMi9qrhL8YkiKTPD7jmgGHYYzrGjQDPWqKGmxjY40DIGDqDROiDq=rPl2TYRqYrwGqaODWa4qlDo4j5DT+0Gx221W4HRDwYA57b+7GsbqteW80D0cus7pOG3qiGZQrARmPmWGnTWQqkAG2rum2TulcdbDhSNDjKDeLINAD7GLCex4D===
Host: www.cdt-ec.com
Origin: https://www.cdt-ec.com
Referer: https://www.cdt-ec.com/notice/moreController/toMore?globleType=0
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
X-Requested-With: XMLHttpRequest''',
    "transmitCookies": False,
    "cookies": None,
    "wdurl": "https://www.cdt-ec.com/notice/moreController/toMore?globleType=0",
}
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'

wdriver_obj = wdriver(UserAgent)


# wdCookiess = wd_getCookie(minfo['wdurl'], UserAgent)
# minfo['cookies'] = wdCookiess


def hub_main(timeL):
    mysql_db_orm = mysql_orm()
    reqSession = req_session(minfo)
    pageS = 100

    listCode = [
        # {'catname': "招标公告", "messagetype": 0},
        # {'catname': "变更公告", "messagetype": 1},
        # {'catname': "中标候选人", "messagetype": 2},
        # {'catname': "中标结果", "messagetype": 3},
        {'catname': "采购公告", "messagetype": 4},
        # {'catname': "采购结果", "messagetype": 5}
    ]
    posturl = "https://www.cdt-ec.com/notice/moreController/getList"

    wdriver = wdriver_obj.get_driver()

    for lo in listCode:
        breakMark = 0
        whileTrue = True
        pi = 1
        while whileTrue:
            postdate = {
                'page': pi,
                'limit': pageS,
                'messagetype': lo['messagetype'],
                'startDate': timeL,
                'endDate': timeL
            }
            originBrow = reqSession.PostResult(posturl=posturl, postdate=postdate, jsonT=1)
            jsonT = originBrow['data']
            mark = 0

            hubinfoList = []
            if len(jsonT) == 0:
                whileTrue = False
                continue
            for info in jsonT:
                ZtbHubInfo_obj = ZtbHubInfo()
                ZtbHubInfo_obj.page_url = 'https://www.cdt-ec.com/notice/moreController/moreall?id=' + info['id']
                # if bl.exists(ZtbHubInfo_obj.page_url) or bh.exists(ZtbHubInfo_obj.page_url):
                # 	mark += 1
                # 	continue
                ZtbHubInfo_obj.site = minfo['site']
                ZtbHubInfo_obj.ztb_ztbInfoType_infoType = lo['catname']
                ZtbHubInfo_obj.province_name = ''
                ZtbHubInfo_obj.subclass = ''
                try:
                    ZtbHubInfo_obj.issue_time = get_timestr(info['publish_time'])
                    ZtbHubInfo_obj.title = info['message_title']
                except:
                    print('title or isstime  error')
                    continue
                try:
                    ZtbHubInfo_obj.ztb_project_tenderer = info['bid_tenderer']
                except KeyError as ff:
                    try:
                        ZtbHubInfo_obj.ztb_project_tenderer = info['purchase_unit']
                    except KeyError as ff1:
                        print(ff1)
                        pass
                    pass
                try:
                    ZtbHubInfo_obj.ztb_ztbInfo_buyTenderEndTime = get_timestr(info['deadline'])
                except KeyError as ff:
                    print(ff)
                    pass

                hhtml = reqSession.GetReHtml(url=ZtbHubInfo_obj.page_url, html=True)
                soup = BeautifulSoup(hhtml, 'lxml')
                regex = re.findall("getGgUrl\((.*?)\)\+", soup.prettify())
                print(soup.prettify())
                print(regex)
                print(ZtbHubInfo_obj.page_url)
                print('-----------------------------------------')
                time.sleep(sleepSec(2, 4))

            # 	hubinfoList.append(ZtbHubInfo_obj.__dict__)
            # if hubinfoList:
            # 	aa = mysql_db_orm.ztbhubinfo_all_insert(hubinfoList)
            # 	print(aa)

            # log1 = f"{lo['catname']}"
            # log = f"本页{len(jsonT)}条，未录{len(jsonT) - mark}篇，共{originBrow['count']}篇，第{pi}页，{timeL}"
            # print(log1)
            # print(log)
            # print('--------------------------------------------')
            #
            # if mark == len(jsonT):
            # 	breakMark += 1
            # 	print("breakMark += 1", breakMark)
            # else:
            # 	breakMark = 0
            #
            # if breakMark == 7:
            # 	whileTrue = False
            # 	continue
            #
            # if originBrow['count'] % pageS == 0:
            # 	allPage = originBrow['count'] // 20
            # else:
            # 	allPage = originBrow['count'] // 20 + 1
            # if pi >= allPage:
            # 	whileTrue = False
            # 	continue
            # else:
            # 	pi += 1
            time.sleep(sleepSec(3, 5))


def article_main():
    reqSession = req_session(minfo)

    if not get_hubList:
        return None
    for hubInfo in get_hubList:
        # if bl.exists(hubInfo.page_url):
        # 	continue
        urll = hubInfo.page_url
        urll = "https://www.cdt-ec.com/notice/moreController/moreall?id=1048600"
        # urll= "https://www.cdt-ec.com/notice/moreController/moreall?id=1031120"
        # hhtml = requests.get(url=urll,headers=a_headers)
        # print(hhtml.text)
        hhtml = reqSession.GetReHtml(url=urll, html=True)
        soup = BeautifulSoup(hhtml, 'lxml')
        # print(soup.prettify())
        print(urll)

        ztbrawInfo_dict = {}

        hunbInfo_dict = hubInfo.__dict__
        for keyName in hunbInfo_dict.keys():
            if hunbInfo_dict[keyName]:
                ztbrawInfo_dict[keyName] = hunbInfo_dict[keyName]

        articleDetail_html = soup.find('div', attrs={"class": "container"})
        regex = re.findall("getGgUrl\((.*?)\)\+", soup.prettify())
        print(regex)

        # print('-------------------------------------')

        # attchements = reqSession.GetReHtml(regex[0],html=False)
        # att_headers = attchements.headers
        # attName_ori = re.findall("filename=(.*?)",att_headers['Content-Disposition'])
        # print(attchements.headers)
        # print(att_headers['Content-Disposition'])
        # print(attName_ori)
        # print(attchements.content)

        # print('99999999999999999999999999999999999999999999999999999999999999')
        time.sleep(3)
        continue

        json_html = json.loads(articleDetail_html)

        content_soup = BeautifulSoup(json_html['content'], 'lxml')
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


def article_main():
    mysql_db_orm = mysql_orm()
    hminfo = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Cookie: _uab_collina=164645451498362828991708; acw_tc=2760778616466396045746640efd8783d2571068546d922e1cdcd7017d133d; JSESSIONID=49D8227BA0C15EB649ECE4A5AEFB4118; ssxmod_itna=Qq0xg7iQdYT4nDlSp+oG=XM17DyDDu0DuaeqfPDsoDcexA5D8D6DQeGTrnNeGvG7n4exNfKt0+xKG7rjO+p==QApfIVfDB3DEx0=bvmDYYCDt4DTD34DYDix5DLDmeD+INKDdjpk5NkuDAQDQ4GyDitDKdi9Di3DA4Dj7kDi4h6SBS0DTeDSKAUP7qDMD7tD/fpTxh=DGqaaxOXSD1x870qDC2hChYydeRDDbrPu3jiDtqD97CtXbQyySMU2eFQa7i+s7GGYj3hxbBG5eowT78EeDhfm73wxzGxqDgp3R34iDD3cLGhYKiDD; ssxmod_itna2=Qq0xg7iQdYT4nDlSp+oG=XM17DyDDu0Duaeq3ikEq7DlpCDjbdhQwb+dAQidoRzju50dU/owyGhYO0eATzY=3PBRfnzzTLTm3OR7dbmHo3K7Xxv=XCQW0Lk4Xd8L5r5tfOSMXyH876aHCXgcFDb7+lrKH/o5Fd8vk59ymdK7wKfvCFSBkYRyH19om5PF8LoSGHbovvFBEfPE7XIc7gg5N1EFNNm7kv+M6nFOjEbQfu4CpBEBrl3lft+gAbN80tNOOURCyNRIvOd1E7o7b98ZBGkB9P4mUED07KCxDcDqNoD+xxZG8nsXPYqZ2X5BNO7DiDGcDG7G7520D4oxnTDD
Host: www.cdt-ec.com
Referer: https://www.cdt-ec.com/notice/moreController/toMore?globleType=0
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'''

    a_headers = dict(line.split(": ", 1) for line in hminfo.split("\n") if line != '')

    # a_headers['Cookie'] = wdCookiess
    # pprint.pprint(a_headers)

    # minfo['Referer'] = 'https://www.cdt-ec.com/notice/moreController/toMore?globleType=0'
    # pprint.pprint(minfo)
    reqSession = req_session(minfo)

    get_hubList = mysql_db_orm.session.query(ZtbHubInfo).filter(ZtbHubInfo.craw_status == 0,
                                                                ZtbHubInfo.site == minfo['site']).order_by(
        ZtbHubInfo.issue_time.desc()).limit(100).all()
    if not get_hubList:
        return None
    for hubInfo in get_hubList:
        # if bl.exists(hubInfo.page_url):
        # 	continue
        urll = hubInfo.page_url
        # urll = "https://www.cdt-ec.com/notice/moreController/moreall?id=1048600"
        # urll= "https://www.cdt-ec.com/notice/moreController/moreall?id=1031120"
        # hhtml = requests.get(url=urll,headers=a_headers)
        # print(hhtml.text)
        hhtml = reqSession.GetReHtml(url=urll, html=True)
        soup = BeautifulSoup(hhtml, 'lxml')
        # print(soup.prettify())
        print(urll)

        ztbrawInfo_dict = {}

        hunbInfo_dict = hubInfo.__dict__
        for keyName in hunbInfo_dict.keys():
            if hunbInfo_dict[keyName]:
                ztbrawInfo_dict[keyName] = hunbInfo_dict[keyName]

        articleDetail_html = soup.find('div', attrs={"class": "container"})
        regex = re.findall("getGgUrl\((.*?)\)\+", soup.prettify())
        print(regex)

        # print('-------------------------------------')

        # attchements = reqSession.GetReHtml(regex[0],html=False)
        # att_headers = attchements.headers
        # attName_ori = re.findall("filename=(.*?)",att_headers['Content-Disposition'])
        # print(attchements.headers)
        # print(att_headers['Content-Disposition'])
        # print(attName_ori)
        # print(attchements.content)

        # print('99999999999999999999999999999999999999999999999999999999999999')
        time.sleep(3)
        continue

        json_html = json.loads(articleDetail_html)

        content_soup = BeautifulSoup(json_html['content'], 'lxml')
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


if __name__ == '__main__':
    # article_main()
    # exit()

    timel = [
        # "2022-03-01",
        #      "2022-03-02",
        #      "2022-03-03",
        #      "2022-03-04",
        #      "2022-03-05",
        #      "2022-03-06",
        "2022-03-07",
    ]
    for t in timel:
        hub_main(t)

    exit()

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
