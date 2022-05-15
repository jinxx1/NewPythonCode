#-*-coding:utf-8
import pprint,json,sys
from urllib.parse import quote
import pymysql,requests,sys
from sql_in import mysql_seach
from bs4 import BeautifulSoup
import re, os

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8'
           }

def splash_render(url):
    from urllib.parse import quote
    import requests, json, random

    ua = [
        "Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    ]
    ua_random = random.choice(ua)
    lua = '''
        function main(splash,args)
          splash:set_user_agent('%s')
          assert(splash:go('%s'))
          assert(splash:wait(0.5))
          local title = splash:evaljs("document.title")
          return {
            html = splash:html(),
            get_cookies = splash:get_cookies(),
            har = splash:har(),
            title = title
          }
          end''' % (ua_random, url)

    for i in range(10):
        print(i)
        if i ==9:
            return 'null'
        splashUrl = 'http://120.79.3.69:8050/execute?lua_source=' + quote(lua)
        SplashReturn = requests.get(url=splashUrl)

        responesJson = json.loads(SplashReturn.text)
        errorYesOrNo = ''.join([x for x in responesJson.keys()])
        if 'error' in errorYesOrNo:
            continue
        else:
            return responesJson


def indexJson(keyword,vauleword,jsonDict):
    """
    说明测试
    """
    if len(keyword)>1:
        keyStr = keyword
    if len(vauleword)>1:
        vauleStr = vauleword
    if len(keyword)<1 and len(vauleword)<1:
        return '请添加键名或值'

    harList = jsonDict['har']['log']['entries']

    for tup in harList:
        for key_0,vaule_0 in tup['request'].items():
            if key_0 == keyStr:
                print(key_0)
                print(vaule_0)
                print('----------------')

        # else:
        #     if not isinstance(vaule_0,str):
        #         print('contiun')

        # print(type(jsonDict[i]))

def strCreat(soup,inputstr):
    # print(soup.attrs)
    # print(soup.name)
    # print(len(soup.attrs))
    if soup.name == 'html' or soup.name == 'script':
        return None
    elif soup.name == 'title' or soup.name == 'Title' or soup.name == 'TITLE':
        return '/' + soup.name

    oneWord = '/' + soup.name
    if len(soup.attrs) < 1:
        return oneWord
    listWord = []
    valueList = []
    for key, value in soup.attrs.items():
        # print('value-------------',value)
        if key == 'href':
            if len(soup.attrs) == 1:
                return oneWord
            else:
                continue

        elif len(value) > 1 and isinstance(value,str) and value in inputstr:

            return oneWord

        elif key == 'id' and len(value) > 1:
            Word1 = '@' + key + '=' + '\'' + value + '\''
            xpathWord = oneWord + '[' + Word1 + ']'
            return xpathWord

        elif key == 'name' and len(value) > 1:
            Word1 = '@' + key + '=' + '\'' + value + '\''
            xpathWord = oneWord + '[' + Word1 + ']'
            return xpathWord

        elif isinstance(value, list):
            Word1 = '@' + key + '=' + '\'' + '{}' + '\''
            for xx in value:
                valueList.append(xx)
            classPath = ' '.join(valueList)
            listWord.append(Word1.format(classPath))
        else:
            if len(value) < 15:
                Word1 = '@' + key + '=' + '\'' + value + '\''
            else:
                continue
            listWord.append(Word1)

    andWord = ' and '.join(listWord)
    xpathWord = oneWord + '[' + andWord + ']'
    return xpathWord.replace('[]', '')

def XpathListLinkGet(soup, Content_Input_Url):

    ListLink_list = []
    for link in Content_Input_Url:
        print(link)
        cutWORD = re.findall("http.*//.*?/", link)[0]
        print(cutWORD)
        TrueUrl = link.replace(cutWORD, '').replace('?', '\?')
        print(TrueUrl)
        findInputWordall = soup.findAll(href=(re.compile(TrueUrl)))
        print('findInputWordall')
        print(findInputWordall)
        if not findInputWordall:
            continue
        for i in findInputWordall:
            print('i****name------', i.name,i.attrs)
            xpathCode=strCreat(i,link)
            for findInputWord in i.parents:
                print('name------',findInputWord.name,findInputWord.attrs)
                label_num = strCreat(findInputWord,link)
                if label_num:
                    xpathCode= label_num + xpathCode
                else:
                    xpathCode = '/' + xpathCode + '/@href'
                    ListLink_list.append(xpathCode.replace('[]', ''))
                    break
    return ListLink_list

def XpathGet(soup, inputWord,Content_Input_Url):
        ListLink_list = []
        findInputWord_all = soup.findAll(text=(re.compile(inputWord)))
        if not findInputWord_all:
            return None
        for i in findInputWord_all:
            xpathCode = ''
            if len(i) > 800:
                continue
            for findInputWord in i.parents:
                label_num = strCreat(findInputWord,Content_Input_Url[0])

                if label_num and '/script' in label_num:
                    print('label_1   发现script')
                    continue
                elif label_num:
                    xpathCode= label_num + xpathCode
                else:
                    xpathCode = '/' + xpathCode + '//text()'
                    ListLink_list.append(xpathCode.replace('[]', ''))
                    break
        return ListLink_list

def Content_Splash_request(url):
    cmdWord = r'curl "http://120.79.3.69:8050/render.json?url={}&html=1&iframes=1&script=1&har=1&history=1&response_body=1&timeout=90"'.format(url)
    for i in range(11):
        if i == 10:
            return 'null'
        cmdWordRespons = os.popen(cmdWord)
        responSTR = json.loads(cmdWordRespons.read())
        try:
            errorRespon = responSTR['error']
            print(errorRespon)
            continue
        except:

            if responSTR['childFrames']:
                responseHtml = responSTR['html']
                for i in responSTR['childFrames']:
                    iframeHtml = i['html']
                    iframeID = i['frameName']
                    iframeWWord = "<.?frame.*?{}.*?</.*frame>".format(iframeID)
                    regex = re.findall(iframeWWord, responseHtml)
                    for reg in regex:
                        newIframeHTML = "<iframe id = \"{}\">".format(iframeID) + iframeHtml + "</iframe>"
                        responSTR['html'] = responseHtml.replace(reg,newIframeHTML)
                return responSTR
            else:
                return responSTR


if __name__ == '__main__':
    # url = r'http://www.zjzfcg.gov.cn/purchaseNotice/index.html?categoryId=3001'
    # url = r'https://www.baidu.com/'
    # url = r'https://new.qq.com/ch/tech/'
    # a = splash_render(url)
    # print(a)
    # aaa = Content_Splash_request(url)
    # print(aaa.keys())
    # print(aaa)
    # print(sys.getsizeof(aaa))
    # import re
    #
    # hhtml = '''//body/div[@class='qq_conent clearfix']/div[@class='LEFT']/div[@class='content clearfix']/div[@class='content-article']/p[@class='one-p']//text()'''
    #
    # a = re.sub("/p.*//text\(\)",'',hhtml)
    # print(a)
    aa = 'https://www.ericsson.com/en/newsroom/latest-news/?typeFilters=1%2C2%2C3%2C4&locs=68304&pageNum={}'
    print(aa.format(2))










