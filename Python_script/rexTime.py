# -*- coding: utf-8 -*-
from datetime import datetime
import re

def strTime2dateTime(timeSTR):
    regexTimeStr = ''
    try:
        a =re.findall(r"\d{4}年\d{1,2}月\d{1,2}日",timeSTR)[0]
        regexTimeStr = a.replace('年', '-').replace('月', '-').replace('日', '')
    except:
        pass

    if regexTimeStr:
        timeStr = regexTimeStr
    elif '长期' in timeSTR:
        timeStr = '2999-12-31'
    elif find_zh(timeSTR) or len(timeSTR)<8:
        return ''
    else:
        timeStr = str(timeSTR).replace('/','-').replace('\\','-').replace('_','-').replace('.','-')

    timeL = [int(x) for x in timeStr.strip('-').split('-')]

    if len(timeL)>2 and timeL[2]>1000:
        dayint = timeL[0]
        timeL[0] = timeL[2]
        timeL[2] = dayint

    if 100 < timeL[0] < 1000:
        return ''

    try:
        Date_Time = datetime(timeL[0], timeL[1], timeL[2])

    except:
        Date_Time = ''

    return Date_Time


def find_zh(word):
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    word = word
    match = zh_pattern.search(word)
    return match

def regFloat(word):
    try:
        a = filter(lambda ch: ch in '0123456789.', str(word))
        stra = ''.join([x for x in a])
    except:
        stra = ''
    return stra

def regIDandCode(inputword):
    temp = 'AAABBcccdddeeewww0123456789fffhhhjjjzzzBBCCC'
    word = inputword.replace('；',temp).replace('\n',temp).replace('.',temp).replace('\\',temp).replace('/',temp).replace('-',temp).replace(';',temp).replace(':',temp)
    try:
        a = filter(lambda ch: ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', str(word))
        stra = ''.join([x for x in a])
    except:
        stra = ''
    return stra.replace(temp,'\n')


if __name__ == "__main__":
    pass