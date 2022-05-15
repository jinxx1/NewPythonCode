# -*- coding: utf-8 -*-

import platform
import requests
import json
import os
import time,re
import random
import pymysql
from bs4 import BeautifulSoup
from PIL import Image
import jieba


import sqlalchemy

def no_script(htmll):
    scrWord = re.findall("<script.*?>.*?</script>",htmll,re.M|re.S)
    for i in scrWord:
        htmll = htmll.replace(i,'')
    scrWord = re.findall("<link.*?>",htmll,re.M|re.S)
    for i in scrWord:
        htmll = htmll.replace(i,'')
    scrWord = re.findall("<meta.*?>",htmll,re.M|re.S)
    for i in scrWord:
        htmll = htmll.replace(i,'')
    scrWord = re.findall("<style.*?>.*?</style>",htmll,re.M|re.S)
    for i in scrWord:
        htmll = htmll.replace(i,'')
    scrWord = re.findall("<!-.*?>*?->",htmll,re.M|re.S)
    for i in scrWord:
        htmll = htmll.replace(i,'')

    return htmll

def no_Html(wword):
    tagList = ['p','div','a','span','strong','table','tr','td','font','ul','li','hr',
               'ol','dl','dt','dd','em','small','h1','h2','h3','h4','h5','h6','h7',
               'h8','h9','main','article','section']

    wword = no_script(wword)
    for i in tagList:
        wword = re.sub("<{}.*?>".format(i),"<{}>".format(i),wword)
    for n in range(5):
        for i in tagList:
            wword = wword.replace('&nbsp;', '').replace('<br>', '').replace('</br>', '').replace('\n', '')
            wword = re.sub("<{}>\s+".format(i),"<{}>".format(i),wword)
            wword = re.sub(">\s+<","><",wword,re.M|re.S)
            wword = re.sub("<{word}></{word}>".format(word = i),"",wword,re.M|re.S)
    soup = BeautifulSoup(wword,'lxml')
    strHtml = str(soup.prettify())
    return strHtml.replace('</body>','').replace('</html>','').replace('<html>','').replace('<body>','')

# 自动获取简介
def get_Summary(html):
    soup = BeautifulSoup(html, 'lxml')
    noneSummary = ''
    soupList = soup.find_all('p')
    if not soupList:
        soupList = soup.find_all('a')
    if not soupList:
        soupList = soup.find_all('span')
    if not soupList:
        return noneSummary

    allWord = []
    for num,htmlBODY in enumerate(soupList):
        decodeWord = htmlBODY.get_text().replace('\u00A0','').replace('\u0020','').replace('\u3000','').replace('\n','').replace('\t','').replace('\r','')
        allWord.append(decodeWord.strip('，').strip(''))

    decodeWord = ''.join(allWord)
    returnSummaryWord = decodeWord[0:60] + "..."

    if len(returnSummaryWord) > 10:
        return returnSummaryWord.replace('%','%%')
    else:
        return noneSummary

# 事件格式变成  2010-01-01 01:01:01
def get_timestr(date,outformat = "%Y-%m-%d",combdata = False):
    import time
    time_array = ''
    format_string = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H",
        "%Y-%m-%d",
        "（%Y-%m-%d %H:%M:%S）",
        "（%Y-%m-%d %H:%M）",
        "（%Y-%m-%d %H）",
        "（%Y-%m-%d）",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %H",
        "%Y/%m/%d",
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d %H:%M",
        "%Y.%m.%d %H",
        "%Y.%m.%d",
        "%Y年%m月%d日 %H:%M:%S",
        "%Y年%m月%d日 %H:%M",
        "%Y年%m月%d日 %H",
        "%Y年%m月%d日",
        "%Y_%m_%d %H:%M:%S",
        "%Y_%m_%d %H:%M",
        "%Y_%m_%d %H",
        "%Y_%m_%d",
        "%Y%m%d%H:%M:%S",
        "%Y%m%d %H:%M:%S",
        "%Y%m%d %H:%M",
        "%Y%m%d %H",
        "%Y%m%d",
        "%Y%m%d%H%M%S",
        "%Y%m%d %H%M%S",
        "%Y%m%d %H%M",
        "%Y%m%d %H",
        "%Y%m%d",
        "%Y\%m\%d %H:%M:%S",
        "%Y\%m\%d %H:%M",
        "%Y\%m\%d %H",
        "%Y\%m\%d",
        "%Y年%m月%d日%H:%M:%S",
        "%Y年%m月%d日%H:%M",
        "%Y年%m月%d日%H",
        "%Y年%m月%d日",
    ]
    for i in format_string:
        try:
            time_array = time.strptime(date, i)
        except:
            continue

    if not time_array:
        return None
    # print(date)
    # print(time_array)
    timeL1 = int(time.mktime(time_array))
    timeL = time.localtime(timeL1)
    if combdata:
        return time.strftime(outformat, timeL),timeL1
    else:
        return time.strftime(outformat,timeL)

# 链接过滤
def depcut(llist):
    crawlList = [x['url'] for x in llist]
    nomysqllist = urlIsExist(crawlList)
    allist = []
    for i in nomysqllist:
        for n in llist:
            if i == n['url']:
                allist.append(n)
    return allist

#关键字筛选
def diff(Title):
    listB = ['5G', '6G', 'AI', 'AR', 'eMBB', 'eMTC', 'IOT', 'IP网', 'Lora', 'LPN', 'LPWA', 'LPWAN', 'M2M', 'MIMO', 'mMTC', 'NR', 'NSA组网', 'SA组网', 'STN', 'uRLLC', 'VR', '波束赋形', '车联网', '城域网', '大数据', '电波传播', '独立组网', '短波通信', '个人通信', '共建共享', '光传输', '光交换', '光器件', '光通信', '毫米波', '核心网', '基础设施', '基站', '交换网', '接入网', '频谱利用', '区块链', '人工智能', '通信电源', '通信技术', '通信建设工程', '通信网络技术', '通信系统', '通信线路', '网络安全', '网络技术', '网络切片', '微波通信', '卫星通信', '无人驾驶', '无线电', '无线接入', '物联网', '新基建', '信息安全', '信息通信', '虚拟现实', '业务网', '移动通信', '云计算', '增强现实', '智能互联', '驻地网', '自动驾驶']
    # 求交集的两种方式
    listA = jieba.cut(Title,cut_all=True)
    # retA = [i for i in listA if i in listB]
    retB = list(set(listA).intersection(set(listB)))
    if retB:
        return retB
    else:
        return None
    # 求并集
    # retC = list(set(listA).union(set(listB)))
    #
    # # 求差集，在B中但不在A中
    # retD = list(set(listB).difference(set(listA)))
    # retE = [i for i in listB if i not in listA]


if __name__ == '__main__':
    tstr = '（2020-09-21）'
    a = get_timestr(tstr,"%Y-%m-%d %H:%M:%S")
    print(a)

