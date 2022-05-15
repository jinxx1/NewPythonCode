import datetime
import os.path
import pprint
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import lxml.html
import sys, json, re
import sqlalchemy
import requests
import pandas as pd
from getmysqlInfo import jsonInfo
from mkdir import mkdir
from redisBloomHash import bl, bh
from crawltools import *
from requests_obj import *
from uxue_orm import *
import platform, sys, os, json

mysystem = platform.system()
if mysystem == 'Windows':
    root = "D:/PythonCode/mypythonpath"
elif mysystem == "Linux":
    root = "/home/terry/anaconda3/lib/python3.7/site-packages/mtools"
else:
    raise 'not Windows or Linux'

MYSQLINFO = jsonInfo['uxuepai_sql']
conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME='jxtest')

mysqlcon = sqlalchemy.create_engine(conStr)


def pandas_insermysql(itmeList, subclass, process_stauts=0):
    newList = []
    for i in itmeList:
        ddict = {}
        ddict['page_url'] = i['url']
        ddict['subclass'] = subclass
        ddict['issue_time'] = i['time']
        newList.append(ddict)
    df = pd.DataFrame(newList)
    df.to_sql(name='listform10086', con=mysqlcon, if_exists='append', index=False)
    for info in newList:
        bh.insert(info['page_url'])


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    ddict = {}
    try:
        ddict['title'] = soup.h1.get_text()
    except:
        return None
    try:
        ddict['content'] = str(soup.find(attrs={'class': 'zb_table'}))
    except:
        return None
    hrefall = soup.find_all(href=re.compile("commonDownload"))
    attachmentListJsonList = []
    for nn in hrefall:
        dic = {}
        download_url = nn.get('href')
        dic['download_url'] = "https://b2b.10086.cn" + download_url
        dic['download_filename'] = nn.get_text()
        attachmentListJsonList.append(dic)
    if attachmentListJsonList:
        ddict['attachmentListJson'] = attachmentListJsonList
    return ddict


def get_urlList():
    excWord = "SELECT id,page_url,issue_time,subclass,process_status FROM listform10086 WHERE process_status =0 ORDER BY issue_time DESC limit 300;"
    alltoup = mysqlcon.execute(excWord)
    llist = []
    for n in alltoup:
        ddict = {}
        ddict['id'] = n[0]
        ddict['page_url'] = n[1]
        ddict['issue_time'] = str(n[2])
        ddict['subclass'] = n[3]
        ddict['process_status'] = n[4]
        llist.append(ddict)
    return llist


def update_stats(artID, statusint):
    excWord = '''UPDATE listform10086 SET process_status={statusint} WHERE id={id};'''.format(statusint=statusint,
                                                                                              id=artID)
    mysqlcon.execute(excWord)


def urlListUrl():
    wword = '''采购公告	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2
资格预审公告	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=3
候选人公示	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=7
中选结果公示	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=16
单一来源采购信息公告	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=1'''.split('\n')
    # wword = '''采购公告	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2'''.split('\n')
    llist = []
    for i in wword:
        n = i.split('\t')
        ddict = {}
        ddict['subclass'] = n[0]
        ddict['listUrl'] = n[1]
        llist.append(ddict)
    return llist


def get_IDandTIME(html, subclass):
    # 获取hub列表
    artcle_urls = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id={}'
    resID = re.findall("selectResult\(\'(.*?)\'\)", html)
    soup = BeautifulSoup(html, 'lxml')
    article_info = []
    for id in resID:
        page_url = artcle_urls.format(id)
        all_tr = soup.find_all(attrs={'onclick': "selectResult('{id}')".format(id=id)})
        for i in all_tr:
            try:
                timeWord = re.findall("(\d{4}-\d{1,2}-\d{1,2})", str(i))[0]
                timeWord = get_timestr(timeWord)
                break
            except:
                continue
        ddict = {}
        ddict['id'] = id
        ddict['url'] = page_url + "&ux_" + timeWord.split(' ')[0]
        ddict['time'] = timeWord

        ddict['subclass'] = subclass
        article_info.append(ddict)

    dupurl_original = [x['url'] for x in article_info]
    dupurl_List = urlIsExist(dupurl_original)

    info = []
    if dupurl_List:
        for i in dupurl_List:
            for arti in article_info:
                if i == arti['url']:
                    if bl.exists(arti['url']) or bh.exists(arti['url']):
                        continue
                    info.append(arti)
    return info


def main_hub():
    brow = requests.get('http://120.79.3.69:8050/')
    if brow.status_code != 200:
        print('Please contact the jinxiao')
        return None
    else:
        pass

    stealthPath = os.path.join(root, "wd/stealth.min.js")
    chrodriverPath = os.path.join(root, "wd/chromedriver")
    # proxIP = "118.24.219.151:16818"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(chrodriverPath, options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    with open(stealthPath, 'r') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
    for num, i in enumerate(urlListUrl()):

        try:
            driver.get(i['listUrl'])
        except Exception as ff:
            print(ff)
            driver.execute_script('window.stop')
            driver.quit()
            exit()

        time.sleep(3)
        mark = 0
        while True:
            if "zb_table_tr" not in driver.page_source:
                mark += 1
                if mark == 10:
                    driver.execute_script('window.stop')
                    driver.quit()

                driver.refresh()
                time.sleep(3)
            else:
                source = driver.page_source
                break
        browList = get_IDandTIME(source, i['subclass'])

        pandas_insermysql(itmeList=browList, subclass=i['subclass'].strip())
        print(i['subclass'], len(browList), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    driver.execute_script('window.stop')
    driver.quit()
    print('===================本次抓取全部完成===================', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def main_artcle():
    mysql_db_orm = mysql_orm()
    llist = get_urlList()

    brow = requests.get('http://120.79.3.69:8050/')
    if brow.status_code != 200:
        print('Please contact jinxiao')
        return None
    else:
        pass

    print('llist  :', len(llist))

    if not llist:
        return None
    # return None
    stealthPath = os.path.join(root, "wd/stealth.min.js")
    chrodriverPath = os.path.join(root, "wd/chromedriver")
    # proxIP = "118.24.219.151:16818"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(chrodriverPath, options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    with open(stealthPath, 'r') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

    for num, i in enumerate(llist):
        page_url = i['page_url'].replace("?ux_", "&ux_")
        try:
            driver.get(i['page_url'])
        except Exception as ff:
            print(ff)
            continue

        time.sleep(3)

        content_info = get_content(driver.page_source)
        try:
            if not driver.page_source or not content_info['content']:
                continue
        except:
            continue

        item = {}
        item['title'] = content_info['title']
        item['content'] = content_info['content']
        item['subclass'] = i['subclass']
        item['issueTime'] = i['issue_time']
        item['url'] = page_url
        item['site'] = "b2b.10086.cn"

        a = save_api(item)
        update_stats(artID=int(i['id']), statusint=1)
        item['content'] = len(item['content'])
        pprint.pprint(item)
        print(a)

    driver.quit()


def notcontentGet():
    ztb_RawInfo = ZtbRawInfo

    mysql_db_orm = mysql_orm()

    excWord = '''SELECT z.id,z.page_url FROM ztbRawInfo z LEFT JOIN ztbRawInfoContent c ON z.id = c.raw_data_id WHERE site = 'b2b.10086.cn' AND issue_time = '2022-03-08 00:00:00' AND c.id is null;'''
    # list1 = [a for a in mysql_db_orm.session.execute(excWord)]
    list1 = [(43006098, "https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=836523&ux_2022-03-08")]
    if not list1:
        print('not')
        return None
    stealthPath = os.path.join(root, "wd/stealth.min.js")
    chrodriverPath = os.path.join(root, "wd/chromedriver")
    # proxIP = "118.24.219.151:16818"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(chrodriverPath, options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    with open(stealthPath, 'r') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

    for i in list1:
        raw_id = i[0]
        page_url = i[1]
        try:
            driver.get(page_url)
        except Exception as ff:
            print(ff)
            continue

        time.sleep(3)

        content_info = get_content(driver.page_source)
        try:
            if not driver.page_source or not content_info['content']:
                continue
        except:
            continue

        print(content_info)
        return None
        contentinsert = mysql_db_orm.ztbRawInfoContent_add_single(content=content_info['content'], rawid=raw_id)
        print(contentinsert)
        if contentinsert and contentinsert != 2:
            mysql_db_orm.session.query(ZtbHubInfo).filter(ZtbHubInfo.id == raw_id).update({"craw_status": 1})
            mysql_db_orm.session.commit()
            pass

        if 'attachmentListJson' in content_info.keys():
            mysql_db_orm.ztbInfoAttaChment_add_single(info=content_info['attachmentListJson'],
                                                      rawid=raw_id)


if __name__ == '__main__':
    main_artcle()
    exit()
    notcontentGet()
    exit()
