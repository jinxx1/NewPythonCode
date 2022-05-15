# -*- coding: utf-8 -*-
import scrapy
import platform
import requests
import random, json
import datetime
import collections

def jsonload(jsonPath):
    with open(jsonPath, 'r', encoding='utf-8') as jf:
        jsonLoad = json.load(jf)
        jf.close()
    return jsonLoad


class llclass():
    a = '1'

    def func(self):
        self.a = 2


def aaa(zz=0):
    if zz == 0:
        a = 1
        b = 2
        return a, b
    else:
        return None, None


import datetime


def get_week():
    today = datetime.date.today()
    month = today.month
    year = today.year
    day = today.day
    weekday = today.weekday()

    start = today + datetime.timedelta(0 - weekday)
    end = today + datetime.timedelta(6 - weekday)

    start = datetime.datetime(start.year, start.month, start.day)
    end = datetime.datetime(end.year, end.month, end.day)

    return str(start).replace('00:00:00','').strip(), str(end).replace('00:00:00','').strip()





def get_date_list(starttime='20151101', endtime='20151210'):
    '''计算输入的起始日期和结束日期之间的所有日期'''

    datelist = []
    d1 = datetime.datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    d2 = datetime.datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    for i in range((d2 - d1).days + 1):
        d3 = d1 + datetime.timedelta(days=i)
        datelist.append(str(d3.strftime("%Y-%m-%d")))

    return datelist
def date_list_fun(starttime='20151101', endtime='20151210'):
    '''计算输入的起始日期和结束日期之间的所有日期'''
    _u = datetime.timedelta(days=1)
    startdate = datetime.datetime.strptime(starttime, '%Y%m%d')
    enddate = datetime.datetime.strptime(endtime, '%Y%m%d')
    n = 0
    date_list = []
    if startdate <= enddate:

        while 1:
            _time = startdate + n * _u
            date_list.append(_time.strftime('%Y:%m:%d'))
            n = n + 1
            if _time == enddate:
                break
    return date_list


def allweeks(year=2015):
    '''计算一年内所有周的具体日期,从1月1号开始，12.31号结束
    输出如{1: ['20190101','20190106'],...} 只有六天
    '''
    start_date = datetime.datetime.strptime(str(year) + '0101', '%Y-%m-%d')
    end_date = datetime.datetime.strptime(str(year) + '1231', '%Y-%m-%d')
    _u = datetime.timedelta(days=1)
    n = 0
    week_date = {}
    while 1:
        _time = start_date + n * _u
        w = str(int(_time.strftime('%W')) + 1)
        week_date.setdefault(w, []).append(_time.strftime('%Y-%m-%d'))
        n = n + 1
        if _time == end_date:
            break
    week_date_start_end = {}
    for i in week_date:
        week_date_start_end[i] = [week_date[i][0], week_date[i][-1]]
    return week_date


def all_weeks(year=2015):
    '''计算一年内所有周的具体日期,每周都是7天，可能最后一周到 下年
     week_date 输出如{1: ['20181231', '20190101', '20190102', '20190103', '20190104', '20190105', '20190106'],...}
     计算一年内所有周的起始日期
     week_date_start_end {1: ['20181231','20190106'],...}
     '''

    start_date = datetime.datetime.strptime(str(int(year) - 1) + '1224', '%Y%m%d')
    end_date = datetime.datetime.strptime(str(int(year) + 1) + '0107', '%Y%m%d')
    _u = datetime.timedelta(days=1)
    n = 0
    week_date = {}
    while 1:
        _time = start_date + n * _u
        y, w = _time.isocalendar()[:2]
        if y == year:
            week_date.setdefault(w, []).append(_time.strftime('%Y-%m-%d'))
        n = n + 1
        if _time == end_date:
            break
    week_date_start_end = {}
    for i in week_date:
        week_date_start_end[i] = [week_date[i][0], week_date[i][-1]]
    return week_date, week_date_start_end



if __name__ == '__main__':
    llist = ['','','','','']
    llist = [x for x in llist if x]
    print('llist',llist)
    if llist:
        print('yes')
    else:
        print('no')
    word = '_'.join(llist)
    print('word',word)
    exit()




    # urlBase = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={pageindex}&bidSort=&buyerName=&projectId=&pinMu=&bidType=&dbselect=bidx&kw=&start_time={date}&end_time={date}&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName='
    # geturl = urlBase.format(pageindex = 1,date = '2020:02:02')
    # print(geturl)
    # exit()
    import pandas as pd
    df = pd.read_json(path_or_buf='ccgp_date.json',orient='index')

    count = 0
    for i in range(0,len(df)):
        yes = False
        for n in ['2018','2019','2020']:
            if n in df.loc[i].date:
                yes = True
                break
        if not yes:
            continue
        print(df.loc[i])


        count+=int(df.loc[i].allPageNum)-1
        # print(df.loc[i])
        print('-----------------')
    print(count*20,count*20 + i*20)


    exit()
    a = date_list_fun(starttime='20130101',endtime='20200602')
    llist = []
    for num,i in enumerate(a):
        # if num >1:
        #     break
        ddict = {}
        ddict['mark'] = 0
        ddict['date'] = str(i)
        ddict['artNum'] = 1
        ddict['allPageNum'] = 0
        llist.append(ddict)
    df = pd.DataFrame(llist)
    df.to_json(path_or_buf='ccgp_date1.json',orient='index')