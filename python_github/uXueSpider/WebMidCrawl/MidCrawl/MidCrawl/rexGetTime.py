# -*- coding: utf-8 -*-
import re,time,datetime



def timeReMark(timtext):
    timetext=timtext.strip()
    timeTrue = ''
    timeWord1 =timetext.split(' ')
    try:
        time1 = timeWord1[1].split(':')
    except IndexError:
        timeTrue = timeWord1[0] + " 00:00:00"
    if not timeTrue:
        if len(time1) == 1:
            timeTrue = timeWord1[0] + ' ' + time1[0] + ":00:00"
        elif len(time1) == 2:
            timeTrue = timeWord1[0] + ' ' + time1[0] + ':' + time1[1] + ":00"
        elif len(time1) == 3:
            timeTrue = timeWord1[0] + ' ' + time1[0] + ':' + time1[1] + ':' + time1[2][0:2]
        else:
            timeTrue = timeWord1[0] + ' ' + time1[0] + ':' + time1[1] + ':' + time1[2][0:2]
    return timeTrue

def rexTimeGet(content):
    timesReg = [
        r"\d{4}-\d{2}-\d{2} ",
        r"\d{4}年\d{2}月\d{2}日",
        r"\d{4}\.\d{2}\.\d{2}",
    ]
    rTIME = ''
    for reg in timesReg:
        gotRexTupList = re.findall(reg,content)
        # print(gotRexTupList)
        if len(gotRexTupList)>0:
            for i in gotRexTupList:
                timeList = i.strip()
                rTIME = timeList.replace('年', '-').replace('月', '-').replace('日', '').replace('_', '-').replace('/','-').replace('.','-')
                getINTtime = int(rTIME.replace('-',''))
                todayINTtime = int(str(datetime.date.today()).replace('-',''))
                if 20000000 < getINTtime <=todayINTtime:
                    return timeReMark(rTIME)
                else:
                    rTIME = ''
                    continue
    if not rTIME:
        return timeReMark(str(datetime.date.today()))



if __name__ == "__main__":
    pass