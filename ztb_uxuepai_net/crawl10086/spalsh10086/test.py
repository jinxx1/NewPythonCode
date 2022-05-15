# coding=utf-8
import re
from bs4 import BeautifulSoup

def get_IDandTIME(html):
    llist = []
    artcle_urls ='https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id={}'
    resID = re.findall("selectResult\(\'(.*?)\'\)",html)
    soup = BeautifulSoup(html,'lxml')
    for id in resID:
        all_tr = soup.find_all(attrs={'onclick': "selectResult('{id}')".format(id=id)})
        for i in all_tr:

            try:
                timeWord = re.findall("(\d{4}-\d{1,2}-\d{1,2})",str(i))[0]
                timeWord = get_timestr(timeWord)
            except:
                print('no timeWord')
                continue
            ddict = {'id':id,'time':timeWord,'url':artcle_urls.format(id)}
            llist.append(ddict)

    return llist

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    ddict = {}

    try:
        time1 = soup.find_all(attrs={'id':'time'})[0]
    except:
        print('no time')
        return None
    ddict['issueTime'] = time1.get_text().replace(' 星期四 ',' ').replace(' 星期一 ',' ').replace(' 星期二 ',' ').replace(' 星期三 ',' ').replace(' 星期五 ',' ').replace(' 星期六 ',' ').replace(' 星期日 ',' ')

    try:
        ddict['title'] = soup.h1.get_text()
    except:
        print('no title')
        return None

    try:
        ddict['content'] = str(soup.find(attrs={'class':'zb_table'}))
    except:
        return None

    return ddict

def get_timestr(date,outformat = "%Y-%m-%d",combdata = False):
    import time
    time_array = ''
    format_string = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H",
        "%Y-%m-%d",
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
    timeL1 = int(time.mktime(time_array))
    timeL = time.localtime(timeL1)
    if combdata:
        return time.strftime(outformat, timeL),timeL1
    else:
        return time.strftime(outformat,timeL)



if __name__ == '__main__':
    pass