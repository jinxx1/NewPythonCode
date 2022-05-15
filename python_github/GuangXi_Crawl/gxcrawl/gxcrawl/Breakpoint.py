# -*- coding: utf-8 -*-
import pprint,json,random,os,sys
# sys.path.append("C:/PthonCode/python_github/GuangZhouPython/GGZY/GGZY/runScrapy.py")

# from runScrapy import BREAKPOINT
# print(BREAKPOINT)

# if sys.argv[2] == 'breakpoint=True':
#     tORf = 1
#     TF = 1
# else:
#     tORf = 0
#     TF = 0

tORf = 1
TF = 1
# TF只要不为1，便关闭链接筛选
def TMEPTEST(TF = TF):
    TEMPWORD = ''
    if TF == 1:
        num = random.randint(10000,99999)
        TEMPWORD = 'temp' + str(num)
    return TEMPWORD


#BPointYesOrNo断点续传开关。如果需要断点续传True，否则为Falsh
def getTXT(txtname,urlDict,BPointYesOrNo = tORf):
    getDict = {}
    if BPointYesOrNo == 0:
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
def writeTXT(txtname,word,BPointYesOrNo = tORf):
    if BPointYesOrNo == 0:
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


if __name__ == "__main__":

    i = {
    "Breakpoint": {
        "catName": "茂名市_交易信息_土地矿产_市直_补充公告_土地",
        "url": "http://218.15.22.157/mmzbtb/jyxx/033004/033004001/033004001002/033004001002001/"
    },
    "ListPageNow": "本页第14条，共14条",
    "Num": 2,
    "articleTime": "2013-11-27",
    "articleTitle": "茂名市国有建设用地使用权挂牌出让补充公告2013-047",
    "catName": "茂名市_交易信息_土地矿产_市直_补充公告_土地",
    "depth": 1,
    "download_latency": 0.42588329315185547,
    "download_slot": "218.15.22.157",
    "download_timeout": 180.0,
    "error": "该页面没有获取到文章链接",
    "errorUrl": "http://218.15.22.157/mmzbtb/jyxx/033004/033004001/033004001002/033004001002001/?Paging=2",
    "url": "http://218.15.22.157/mmzbtb/jyxx/033004/033004001/033004001002/033004001002001/?Paging={}"
}

    errorLOG(i)


