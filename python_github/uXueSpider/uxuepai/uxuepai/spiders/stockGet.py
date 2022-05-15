# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import html
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import os
from uxuepai.items import UxuepaiItem
import pymysql
import time
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())

# ToDayTime = '2019-02-24'
import lxml.html
etree = lxml.html.etree
import json


def mysql_seach():
    db = pymysql.connect(
        host="120.79.192.168",
        db="dev_umxh",
        user="xey",
        passwd="85f0a9e2e63b47c0b56202824195fb70#AAA",
        charset="utf8",
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    search_date = "SELECT * FROM Stockinfo"
    cursor.execute(search_date)
    resultes = cursor.fetchall()
    return resultes

def machtodaydate(url):
    daytime = ToDayTime.replace('-','')
    db = pymysql.connect(
        host="120.79.192.168",
        db="umxh",
        user="xey",
        passwd="85f0a9e2e63b47c0b56202824195fb70#AAA",
        charset="utf8",
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    search_date = "SELECT id FROM ztbInfo WHERE spiderKey = {} and page_url = '{}'".format(int(daytime),url)
    cursor.execute(search_date)
    resultes = cursor.fetchall()
    cursor.close()
    db.close()
    return resultes

def readPDF(filepath,Save_name):
    # 来创建一个pdf文档分析器
    Path = open(filepath,'rb')
    parser = PDFParser(Path)
    # 创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr = PDFResourceManager()
        # 设定参数进行分析
        laparams = LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 处理每一页
        word = []
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    ss = x.get_text().encode('UTF-8','replace').decode("UTF-8",'replace')#.replace(u'\uf050',u'').replace(u'\uf052',u'').replace(u'\uf0a3',u'').replace(u'\uf06c',u'')
                    ii = ss.strip().replace('\n', '')
                    if len(ii) > 1:
                        with open('%s' % (Save_name), 'a',encoding='utf-8') as f:
                            f.writelines('<p>' + ii + '</p>')
                            f.flush()
        with open('%s' % (Save_name), 'r', encoding='utf-8') as f:
            wordAll = f.read()
    Path.close()
    return wordAll

class StockgetSpider(scrapy.Spider):
    name = 'stockGet'
    allowed_domains = ['cninfo.com.cn']
    def start_requests(self):
        stockAll = mysql_seach()
        for stockNum in stockAll:
            url = 'http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey={}&sdate=&edate=&isfulltext=false&sortName=nothing&sortType=desc&pageNum=1'.format(stockNum['charT'])
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):

        jsonR = json.loads(response.body_as_unicode()).get('announcements')
        for everyOne in jsonR:
            if ToDayTime in everyOne['adjunctUrl']:
                PDFurl = 'http://www.cninfo.com.cn/' + everyOne['adjunctUrl']
                if not machtodaydate(PDFurl):
                    PDFid = everyOne['announcementId']
                    PDFtitle = everyOne['announcementTitle'].replace('<em>','').replace('</em>','')
                    PDFcompany = everyOne['secName']
                    PDFlocal = r"./PDF/{}.PDF".format(PDFid)
                    TEXTlocal = r"./TEXT/{}.txt".format(PDFid)
                    rr = requests.get(PDFurl, stream=True)
                    with open(PDFlocal, "wb") as file:
                        file.write(rr.content)
                        file.close()
                    word = readPDF(PDFlocal, TEXTlocal)
                    os.remove(PDFlocal)
                    os.remove(TEXTlocal)
                    item = UxuepaiItem()
                    item['NameTOTALItem'] = '上市公司公告：' + PDFcompany
                    item['TitleItem'] = PDFtitle
                    item['LinkItem'] = PDFurl
                    item['TimeItem'] = int(ToDayTime.replace('-', ''))
                    item['WordItem'] = word
                    item['WebNameWord'] = 'cninfo'
                    yield item




