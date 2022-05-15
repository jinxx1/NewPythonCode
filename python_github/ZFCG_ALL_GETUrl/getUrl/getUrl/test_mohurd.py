# -*- coding: utf-8 -*-
from lxml import html
import lxml.html
etree = lxml.html.etree
from lxml import html
import re,pprint
import pymysql
import time,datetime

b = datetime.datetime.now().strftime("%Y-%m-%d")
nowTime = datetime.datetime.strptime(b, "%Y-%m-%d")
strnowTime = str(nowTime).split(' ')[0]
# strnowTime = '2019-09-24'

MYSQLINFO = {
    "HOST": "120.24.4.84",
    "DBNAME": "crawlURL",
    "USER": "xey",
    "PASSWORD": "85f0a9e2e63b47c0b56202824195fb70#AAA",
    "PORT":3306
}

def IEget(url):
    import win32com.client
    import time
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Navigate(url)
    ie.Visible = 0

    while ie.Busy:
        time.sleep(1)
    document = ie.Document
    document.close()
    ie.Quit()
    return document.body.innerHTML

def fireFox(url):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    driver = webdriver.Firefox()
    driver.get(url)
    print(driver.page_source)
    driver.close()

class MYSQLDB():
    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                           passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])

    def closeDB(self):
        self.db.close()

    def get_someInfo(self,tablesName,keystr,timeT):
        cursor = self.db.cursor()
        sqlCode = '''SELECT {} FROM {} where issueTime="{}"'''.format(keystr,tablesName,timeT)
        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()
        llist = []
        for i in seeAll:
            llist.append(i[0])
        cursor.close()
        return llist

    def insert_date(self,dictWord):
        cursor = self.db.cursor()
        keyList = dictWord.keys()

        llist = ['\"{}\"'.format(dictWord[i]) for i in keyList]
        keyvaule = ','.join(llist)
        keystr = ','.join(keyList)
        sqlcut = '''
        INSERT INTO chinaUniconUrl ({}) value ({})
        '''.format(keystr,keyvaule)

        # sqlCode = '''
        # INSERT INTO chinaUniconUrl (issueTime,collName,domain,from_Page,site,subclass,title,url) value ('{issueTime}','{collName}','{domain}','{from_Page}','{site}',
        # '{subclass}','{title}','{url}')
        # '''
        # sqlcut = sqlCode.format(
        #     collName = pymysql.escape_string(dictWord['collName']),
        #     domain = pymysql.escape_string(dictWord['domain']),
        #     from_Page = pymysql.escape_string(dictWord['from_Page']),
        #     issueTime = pymysql.escape_string(dictWord['issueTime']),
        #     site = pymysql.escape_string(dictWord['site']),
        #     subclass = pymysql.escape_string(dictWord['subclass']),
        #     title = pymysql.escape_string(dictWord['title']),
        #     url = pymysql.escape_string(dictWord['url'])
        # )

        cursor.execute(sqlcut)
        self.db.commit()
        cursor.close()
        print('录入完成')

def main():
    mysqldb = MYSQLDB()
    # keysList = ['id','site','domain','collName','from_Page','issueTime','subclass','title','url','remark']
    keys = 'url'
    tbNameList = 'chinaUniconUrl'
    mysqlLinkList = mysqldb.get_someInfo(tablesName=tbNameList, keystr=keys, timeT=strnowTime)
    urlist = [{'catName': '中国联通_结果公告',
               'url': 'http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?type=2&page={}'},
              {'catName': '中国联通_采购公告',
               'url': 'http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?type=1&page={}'},
              {'catName': '中国联通_单一来源采购征求意见公示',
               'url': 'http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?type=3&page={}'}]
    for num, i in enumerate(urlist):
        for PageNum in range(1, 10000):
            indexUrl = i['url'].format(str(PageNum))
            while True:
                try:
                    htmlCode = IEget(indexUrl)
                    break
                except:
                    time.sleep(3)
            brow = html.fromstring(htmlCode)
            Title = brow.xpath("//table//span/@title")
            n = 0
            for tit in Title:
                item = {}
                timeT = ''.join(brow.xpath("//*[@title = '{}']/../../td[not(@title)]/text()".format(tit)))
                regTime = ''.join(re.findall("\d{2,4}-\d{1,2}-\d{1,2}", timeT))
                if strnowTime == regTime:
                    linkT = ''.join(brow.xpath("//*[@title = '{}']/@onclick".format(tit)))
                    try:
                        regLink = re.findall("id=(.*?)\"", linkT)
                    except:
                        continue
                    item['url'] = "http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/detailNotice.jsp?id=" + ''.join(
                        regLink)
                    if item['url'] in mysqlLinkList:
                        continue
                    item['title'] = tit
                    # item['issueTime'] = datetime.datetime.strptime(regTime, "%Y-%m-%d")
                    item['issueTime'] = regTime
                    item['collName'] = 'monitorUrl'
                    item['site'] = '中国联通'
                    item['domain'] = 'www.chinaunicombidding.cn'
                    item['from_Page'] = indexUrl
                    item['subclass'] = i['catName']
                    item['remark'] = 0
                    mysqldb.insert_date(item)
                    n += 1
            if n == 0:
                break
    mysqldb.closeDB()

if __name__ == "__main__":
    # main()

    url = 'http://jzsc.mohurd.gov.cn/data/company'
    a = IEget(url)
    print(a)




    print('---- the end ----')