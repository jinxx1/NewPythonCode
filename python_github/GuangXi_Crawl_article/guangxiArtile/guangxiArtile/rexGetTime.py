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
        "\d{4}-\d{2}-\d{2}",
        r"\d{4}年\d{2}月\d{2}日",
        r"\d{4}\.\d{2}\.\d{2}",
    ]

    rTIME = ''
    for reg in timesReg:
        gotRexTupList = re.findall(reg,content)
        if len(gotRexTupList)>0:
            for i in gotRexTupList:
                rTIME = i.strip()
                return rTIME

    if not rTIME:
        return 'null'

def getfiletype(fileurl):
    typeReg = ["\.zip","\.rar","\.tar","\.gz","\.bz2","\.7z","\.pdf","\.xls","\.xlsx","\.xlsm","\.doc","\.docx","\.ppt","\.jpg","\.jpeg","\.png","\.gif","\.txt"]
    for reg in typeReg:
        gotRexTupList = re.findall(reg.lower(),fileurl.lower())
        if gotRexTupList:
            filetype = gotRexTupList[0]
            break
        else:
            filetype = 'unknow_filetype'
    return filetype


if __name__ == "__main__":
    pass