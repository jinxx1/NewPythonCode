#-*-coding:utf-8
import requests
from lxml import html
import re
import csv
import time
import lxml.html
etree = lxml.html.etree
from  urllib.parse import urljoin
from filterHtml import filter_tags
import pprint
from sql_in import mysql_indata,mysql_seach,mysql_yes
from CssGetDef import *

class testSpider():
    def testspider(self,Date):
        if Date['splash_list']==1:
            rList = splash_render(Date['startUrl'])
        else:
            rList = getHtmlTrue(Date['startUrl'])
        brow = html.fromstring(rList['html'])
        ListLink = brow.xpath(Date['LinkList'])
        myDict = {
            'ListTitle':'',
            'ListLink':'',
            'ContentTitle':'',
            'ContentWord':'',
        }
        myDictList = {
            'ListTitle':[],
            'ListLink':[],
            'ContentTitle':[],
            'ContentWord':[],
        }
        NumArticle = 0
        for i,url in enumerate(ListLink):
            if NumArticle > 10:
                break
            # else:
            #     myDict['ListLink'] = '该文域名与样本入口域名严重不符'
            #     myDictList['ListLink'].append(myDict['ListLink'])

            NumArticle += 1
            myDict['ListLink'] = urljoin(Date['startUrl'],url)
            myDictList['ListLink'].append(myDict['ListLink'])
            myDict['ListTitle'] = ''
            myDictList['ListTitle'].append(myDict['ListTitle'])

            if Date['splash_Content']==1:
                rContent = splash_render(myDict['ListLink'])
            else:
                rContent = getHtmlTrue(myDict['ListLink'])

            brow1 = html.fromstring(rContent['html'])
            # word1 = brow1.xpath(Date['Content_Text'].replace('//text()','').replace('/text()',''))
            word_xxpath = brow1.xpath(Date['Content_Text'])
            word1 = [i for i in word_xxpath]

            try:
                myDict['ContentTitle'] = brow1.xpath(Date['Content_Title'])[0]#.decode("utf8","ignore")
                myDictList['ContentTitle'].append(myDict['ContentTitle'])
            except IndexError:
                myDict['ContentWord'] = 'ERROR:该页与样本样式严重不符'
                myDictList['ContentWord'].append(myDict['ContentWord'])
                continue

            wo = '\n'.join(word1)

            myDict['ContentWord'] = wo

            myDictList['ContentWord'].append(myDict['ContentWord'])

        return myDictList


if __name__ == '__main__':
    import sys
    xpathCodeDict = mysql_seach(751)[0]
    print(xpathCodeDict)
    # a = sys.argv[1]
    # xpathCodeDict = mysql_seach(a)[0]
    spiderTestConDictList = testSpider().testspider(xpathCodeDict)
    pprint.pprint(spiderTestConDictList)

