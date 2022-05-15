# -*- coding: utf-8 -*-
import pprint,json,random,os,datetime
from NEW_GGZY.Exist import urlIsExist
from urllib import parse
# TF只要不为1，便关闭链接筛选
def TMEPTEST(TF = 2):
    TEMPWORD = ''
    # if TF == 1:
    #     num = random.randint(10000,99999)
    #     TEMPWORD = 'temp' + str(num)
    return TEMPWORD
#BPointYesOrNo断点续传开关。如果需要断点续传True，否则为Falsh
def getTXT(txtname,urlDict,BPointYesOrNo = False):
    getDict = {}
    if BPointYesOrNo == False:
        getDict['urlDict'] = urlDict
        getDict['Num'] = 1
        return getDict
    else:
        try:
            with open(r'breakpoint/{}.txt'.format(txtname),'r',encoding='utf-8') as filetxt:
                dataT = filetxt.read()
                dictT = json.loads(dataT.replace(r"'","\""))
                getDict['Num'] = dictT['Num']
                del dictT['Num']
                pointT = 0
                for n,x in enumerate(urlDict):
                    if dictT == x:
                        pointT = n
                        break
                getDict['urlDict'] = urlDict[pointT:]
                return getDict
        except:
            print('没有读取到txt文件！！！！！！！！！！！！！！！！！！！！！！！')
            getDict['urlDict'] = urlDict
            getDict['Num'] = 1
            return getDict

def writeTXT(txtname,word,BPointYesOrNo = False):
    if BPointYesOrNo==False:
        return None
    with open(r'breakpoint/{}.txt'.format(txtname), 'w', encoding='utf-8') as filetxt:
        filetxt.write(word)


def remarkList(list):
    newList = []
    for i in list:
        if 'javascript'in i:
            continue
        i = i.replace(' ','').replace('\n','').replace('\t','').replace('\r','')
        if i:
            newList.append(i)
    return newList

def errorLOG(DICT):
    os.getcwd('./ERRORLOG')
    try:
        with open(r'ERRORLOG/ERROR.json', 'r+',encoding='utf-8') as f:
            old = f.read()
            f.seek(0,0)
            json.dump(DICT, f, ensure_ascii=False, sort_keys=True, indent=4)
            f.write('|#|')
            f.write(old)
    except FileNotFoundError:
        with open(r'ERRORLOG/ERROR.json', 'w',encoding='utf-8') as filetxt:
            filetxt.seek(0, 0)
            json.dump(DICT,filetxt,ensure_ascii=False,sort_keys=True, indent=4)
            filetxt.write('|#|')



def time_replace(timeWord,keysList):
    timestr = timeWord
    for key in keysList:
        timestr = timestr.replace(key,'-')
    return timestr

def duplicateUrl(linkList, url):

    # 去重模块

    urlTemp = [{'oldUrl':i,'newUrl':parse.urljoin(url, i)} for n,i in enumerate(linkList)]
    duplicateUrl = [x['newUrl'] for x in urlTemp]
    urllist = urlIsExist(duplicateUrl)

    link = []
    for ul in urllist:
        for te in urlTemp:
            if ul==te['newUrl']:
                link.append(te['oldUrl'])
    return link


def timeReMark(timtext):
    Date_Time = "2000-01-01 00:00:00"
    import re
    if not timtext:
        return Date_Time

    try:
        Ymd = re.findall("\d{2,4}-\d{1,2}-\d{1,2}",timtext)[0]
    except:
        return Date_Time

    splitYmd = [int(x) for x in Ymd.split('-')]

    try:
        dupliYmd = [int(n) for n in timtext.replace(Ymd,'').strip().split(':')]
    except:
        Date_Time = datetime.datetime(splitYmd[0], splitYmd[1], splitYmd[2])
        return str(Date_Time)



    if len(dupliYmd) == 1:
        Date_Time = datetime.datetime(splitYmd[0], splitYmd[1], splitYmd[2], dupliYmd[0])

    elif len(dupliYmd) == 2:
        Date_Time = datetime.datetime(splitYmd[0], splitYmd[1], splitYmd[2], dupliYmd[0], dupliYmd[1])

    else:
        Date_Time = datetime.datetime(splitYmd[0], splitYmd[1], splitYmd[2], dupliYmd[0], dupliYmd[1], dupliYmd[2])

    return str(Date_Time)


if __name__ == "__main__":
    # strWord = '2019-1-3 01:00:11'
    strWord = '2019-1-3 00'
    print(timeReMark(strWord))