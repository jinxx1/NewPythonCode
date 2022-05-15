# -*- coding: utf-8 -*-
import pprint
from bs4 import BeautifulSoup
import re, requests, json
import time
import json
from bs4 import BeautifulSoup
import execjs, js2py
import datetime
from crawltools import *

path = 'hhtml.txt'

with open(path,'r',encoding='utf-8') as ff:
    hhtml = ff.read()

soup = BeautifulSoup(hhtml,'lxml')
info_all = soup.find('div',attrs={'class':'wrapTable'}).find_all('tr',attrs={'class':'gradeX'})

csrtoken = soup.find('input',attrs={"name":"csrfmiddlewaretoken"}).get("value")
print(csrtoken)

wword = '公开招标'
from urllib.parse import quote
text = quote(wword,'utf-8')
print(text)
exit()

for info in info_all:

    ele = info.find_all('td')
    location = str(ele[0].get_text())
    tender = str(ele[2].get_text())
    url_temp= ele[3].find('a').get('href')
    title = ele[3].find('a').get_text()
    time = str(ele[0].get_text())
    # print(location)
    # print(tender)
    # print(url_temp)
    # print(title)
    # print(time)
    # print('--------------------------------------')

# print(soup.prettify())
get_pageCountEle = soup.find('button',attrs={"type":"button"},text=re.compile("末页"))
if get_pageCountEle:
    pageCount = int(re.findall("page=(\d{1,10})",get_pageCountEle.get('onclick'))[0])
else:
    pageCount = 0
print(get_pageCountEle)
print(pageCount)



import datetime,time

today = datetime.date.today() #获得今天的日期
lastday = today + datetime.timedelta(days=1)
time_str = '2022-03-01'
timeStartArray = time.strptime(time_str,'%Y-%m-%d')
timeStartStamp = time.mktime(timeStartArray)
endStamp = int(timeStartStamp) + 86400
timeStart = time.localtime(timeStartStamp)
endStart = time.localtime(endStamp)

print(time.strftime("%Y-%m-%d",timeStart))
print(time.strftime("%Y-%m-%d",endStart))



# print(today,lastday)
