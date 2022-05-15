# -*- coding: utf-8 -*-

import pprint
import requests
import lxml
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator


from bs4 import BeautifulSoup
import pandas as pd
#显示所有列
##列名与数据对其显示
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
##显示所有列
pd.set_option('display.max_columns', None)
##显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 15000)


def Pdf2Txt(Path=None):

    pmp_chn = r'D:\PMP_about\PMBOK_6_chn.pdf'
    pmp_eng = r'D:\PMP_about\PMBOK_6_eng.pdf'
    Path = pmp_eng

    #来创建一个pdf文档分析器
    parser = PDFParser(Path)
    #创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr=PDFResourceManager()
        # 设定参数进行分析
        laparams=LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device=PDFPageAggregator(rsrcmgr,laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter=PDFPageInterpreter(rsrcmgr,device)
        # 处理每一页
        for Num,page in enumerate(PDFPage.create_pages(document)):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout=device.get_result()
            print('---------------------------', Num)
            for num,x in enumerate(layout):


                if (isinstance(x, LTTextBoxHorizontal)):
                    print(x.get_text().encode('utf-8').decode('utf-8'))
                #     with open(Save_name.format(str(Num)),'a') as f:
                #         f.write(x.get_text()+'\n')


def hellokittycnCrawl():
    BASEURL = 'http://hellokittycn.com/'
    with open('pmp_left.txt','r',encoding='utf-8') as file:
        html_left = file.read()
    soup = BeautifulSoup(html_left,'lxml')
    levle_1 = soup.find_all(attrs={'aria-level':'1'})
    llist_1 = [{'l1_title':l1.a.get_text(),'l1_url':l1.a.get('href'),'l1_pageid':int(l1.get('id'))} for l1 in levle_1]
    df_1 = pd.DataFrame(llist_1)

    levle_2 = soup.find_all(attrs={'aria-level':'2'})
    llist_2 = []
    for i in levle_2:
        ddict = {}
        name = i.a.get_text()
        ddict['l2_url'] = i.a.get('href')
        ddict['l2_id'] = name.split(' ')[0]
        ddict['l2_title'] = ''.join(name.split(' ')[1:])
        ddict['l2_pageid'] = int(i.get('id'))
        ddict['l1_pageid'] = int(i.find_previous(attrs={'aria-level':'1'}).get('id'))
        llist_2.append(ddict)
    df_2 = pd.DataFrame(llist_2)
    df_12 = pd.merge(df_1,df_2,on='l1_pageid')

    levle_3 = soup.find_all(attrs={'aria-level':'3'})
    llist_3 = []
    for i in levle_3:
        ddict = {}
        name = i.a.get_text()
        ddict['l3_url'] = i.a.get('href')
        ddict['l3_id'] = name.split(' ')[0]
        ddict['l3_title'] = ''.join(name.split(' ')[1:])
        ddict['l3_pageid'] = int(i.get('id'))
        ddict['l2_pageid'] = int(i.find_previous(attrs={'aria-level':'2'}).get('id'))
        llist_3.append(ddict)
    df_3 = pd.DataFrame(llist_3)


    levle_4 = soup.find_all(attrs={'aria-level':'4'})
    llist_4 = []
    for i in levle_4:
        ddict = {}
        name = i.a.get_text()
        ddict['l4_url'] = i.a.get('href')
        ddict['l4_id'] = name.split(' ')[0]
        ddict['l4_title'] = ''.join(name.split(' ')[1:])
        ddict['l4_pageid'] = int(i.get('id'))
        ddict['l3_pageid'] = int(i.find_previous(attrs={'aria-level':'3'}).get('id'))
        llist_4.append(ddict)
    df_4 = pd.DataFrame(llist_4)


    levle_5 = soup.find_all(attrs={'aria-level':'5'})
    llist_5 = []
    for i in levle_5:
        ddict = {}
        name = i.a.get_text()
        ddict['l5_url'] = i.a.get('href')
        ddict['l5_id'] = name.split(' ')[0]
        ddict['l5_title'] = ''.join(name.split(' ')[1:])
        ddict['l5_pageid'] = int(i.get('id'))
        ddict['l4_pageid'] = int(i.find_previous(attrs={'aria-level':'4'}).get('id'))
        llist_5.append(ddict)
    df_5 = pd.DataFrame(llist_5)

    df_12 = pd.merge(df_1, df_2, on='l1_pageid',copy=True,how='outer')
    df_123 = pd.merge(df_12,df_3,on='l2_pageid',copy=True,how='outer')
    df_1234 = pd.merge(df_123,df_4,on='l3_pageid',copy=True,how='outer')
    df = pd.merge(df_1234,df_5,on='l4_pageid',copy=True,how='outer')


    return df



if __name__ == '__main__':
    a = hellokittycnCrawl()
    a.to_csv('pmp.csv',encoding='utf_8_sig')
    print(a)
    pass


