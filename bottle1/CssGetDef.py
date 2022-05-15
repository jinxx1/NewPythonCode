#-*-coding:utf-8
import requests,os,sys,json
from lxml import html
import re,difflib
from fake_useragent import UserAgent
ua = UserAgent().random
import lxml.html
etree = lxml.html.etree
import pprint
from bs4 import BeautifulSoup


def getHtmlTrue(url,cookies=None):

    if isinstance(url,list):
        forurl = url[0]
        print('这就是list-url')
    else:
        forurl = url
        print('不是list-url')
    dict = {}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    try:
        if not cookies:
            indexBrow = requests.get(forurl,headers=headers)
            print('not cookies-url')
        else:
            indexBrow = requests.get(forurl, headers=headers,cookies=cookies)
            print('have cookies-url')

    except requests.exceptions.ConnectionError:
        print('requests.exceptions.ConnectionError----------------')
        return None

    if indexBrow.status_code > 400:
        return None
    else:
        print('开始进入dict输出')
        dict['html'] = indexBrow.text.encode(indexBrow.encoding,'ignore')
        dict['charset'] = indexBrow.encoding
        dict['cookies'] = indexBrow.cookies
        return dict

def splash_render(url):

    if isinstance(url,list):
        forurl = url[0]
        print('splash这就是list-url')
    else:
        forurl = url
        print('splash不是list-url')

    headers = [('User-Agent', ua)]


    params = {
        'url': forurl,
        'http_method': 'GET',
        'headers': headers,
        'html':1,
        'timeout':150,
        'wait':3,
        'images':0,
        'resource_timeout':100
    }
    for i in range(6):
        brow = requests.post(url='http://120.79.3.69:8050/render.json',
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(params))
        browJson = json.loads(brow.text)
        try:
            print(browJson['error'])
            print('渲染失败，重新渲染。共渲染5次。目前是第{}次'.format(i + 1))
            continue
        except:
            # print(browJson['html'])
            return browJson



    # from urllib.parse import quote
    # import requests, json, random
    #
    # ua = [
    #     "Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    #     "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    # ]
    # ua_random = random.choice(ua)
    # lua = '''
    #     function main(splash,args)
    #       splash:set_user_agent('%s')
    #       assert(splash:go('%s'))
    #       assert(splash:wait(0.5))
    #       local title = splash:evaljs("document.title")
    #       return {
    #         html = splash:html(),
    #         get_cookies = splash:get_cookies(),
    #         har = splash:har(),
    #         title = title
    #       }
    #       end''' % (ua_random, forurl)
    #
    # for i in range(10):
    #     print(i)
    #     if i ==9:
    #         return 'null'
    #     splashUrl = 'http://120.79.3.69:8050/execute?lua_source=' + quote(lua)
    #     SplashReturn = requests.get(url=splashUrl)
    #
    #     responesJson = json.loads(SplashReturn.text)
    #     errorYesOrNo = ''.join([x for x in responesJson.keys()])
    #     if 'error' in errorYesOrNo:
    #         continue
    #     else:
    #         return responesJson



# -------------------------------------------------
# def splash_render(url):
#     cmdWord = r'curl "http://120.79.3.69:8050/render.json?url={}&html=1&iframes=1&script=1&har=1&history=1&response_body=1&timeout=90"'.format(url)
#     for i in range(11):
#         if i == 10:
#             return 'null'
#         cmdWordRespons = os.popen(cmdWord)
#         responSTR = json.loads(cmdWordRespons.read())
#
#         try:
#             errorRespon = responSTR['error']
#             print(errorRespon)
#             continue
#         except:
#             if responSTR['childFrames']:
#                 responseHtml = responSTR['html']
#                 for i in responSTR['childFrames']:
#                     iframeHtml = i['html']
#                     iframeID = i['frameName']
#                     iframeWWord = "<.?frame.*?{}.*?</.*frame>".format(iframeID)
#                     regex = re.findall(iframeWWord, responseHtml)
#                     for reg in regex:
#                         newIframeHTML = "<iframe id = \"{}\">".format(iframeID) + iframeHtml + "</iframe>"
#                         responSTR['html'] = responseHtml.replace(reg,newIframeHTML)
#                 return responSTR
#             else:
#                 return responSTR
#
#     # from urllib.parse import quote
#     # import requests, json
#     # lua = '''
#     #     function main(splash,args)
#     #       splash.resource_timeout = 120.0
#     #       assert(splash:go('%s'))
#     #       assert(splash:wait(0.5))
#     #       local title = splash:evaljs("document.title")
#     #       return {
#     #         html = splash:html(),
#     #         get_cookies = splash:get_cookies(),
#     #         har = splash:har(),
#     #         title = title
#     #       }
#     #       end''' %(url)
#     #
#     # # assert(splash:wait(0.5))
#     # for i in range(10):
#     #     print(i)
#     #     if i ==9:
#     #         return 'null'
#     #     # splashUrl = 'http://localhost:8050/execute?lua_source=' + quote(lua)
#     #     # splashUrl = 'http://vpn.imgoodtalk.com:8050/execute?lua_source=' + quote(lua)
#     #
#     #     splashUrl = SPLASH_URL + 'execute?lua_source=' + quote(lua)
#     #     print('splash url--------------------:',splashUrl)
#     #     SplashReturn = requests.get(url=splashUrl)
#     #
#     #     responesJson = json.loads(SplashReturn.text)
#     #     # responesJson["splashUrl"] = splashUrl
#     #     # print(SplashReturn.text)
#     #     errorYesOrNo = ''.join([x for x in responesJson.keys()])
#     #     if 'error' in errorYesOrNo:
#     #         continue
#     #     else:
#     #         return responesJson

def getSiteNameAndDomain(soup):
    des1 = soup.find('meta',attrs={'name': 'SiteName'})
    des2 = soup.find('meta',attrs={'name': 'sitename'})
    des3 = soup.title.string
    if des1:
        return des1.get('content').replace('\n','').replace('\t','').replace('\r','')
    elif des2:
        return des2.get('content').replace('\n','').replace('\t','').replace('\r','')
    elif des3:
        return des3.replace('\n','').replace('\t','').replace('\r','')
    else:
        return '无法获取网站名称，请手动添加'

def ContentXpathGet(soup,inputWord,Content_Input_Url):
    ListLink_list = []
    findInputWord_all = soup.findAll(text=(re.compile(inputWord)))
    if len(findInputWord_all) > 1:
        longBest = 'q'
        for num, i in enumerate(findInputWord_all):
            if len(longBest) < len(i):
                longNum = num
                del findInputWord_all[longNum]
            else:
                return None
    for i in findInputWord_all:
        xpathCode = ''
        if len(i) > 800:
            continue
        for findInputWord in i.parents:
            label_num = strCreat(findInputWord, Content_Input_Url[0])
            if label_num and '/script' in label_num:
                print('label_1   发现script')
                continue
            elif label_num:
                xpathCode = label_num + xpathCode
            else:
                xpathCode = '/' + xpathCode + '//text()'
                ListLink_list.append(xpathCode.replace('[]', ''))
                break
    return ListLink_list



    # findInputWord_all = soup.findAll(text=(re.compile(inputWord)))
    #
    # if isinstance(findInputWord_all, list):
    #
    #
    # for findInputWord in findInputWord_all:
    #     label_1 = strCreat(findInputWord.find_parent(),Content_Input_Url[0])
    #     print('label_1----------------------',label_1)
    #     if label_1 and '/script' in label_1:
    #         # print('label_1   发现script')
    #         continue
    #     elif not label_1:
    #         continue
    #
    #     label_2 = strCreat(findInputWord.find_parent().find_parent(),Content_Input_Url[0])
    #     print('label_2----------------------',label_2)
    #     if label_2 and '/script' in label_2:
    #         # print('label_2   发现script')
    #         continue
    #     if not label_2:
    #         xpathCode = '/' + label_1
    #         break
    #     else:
    #         xpathCode = '/' + label_2 + '/' + label_1
    #         break
    # print('xpathCode-------------------------------------------',xpathCode)
    # return xpathCode.replace('[]', '')

def strCreat(soup,inputstr):
    # print('soup.name////////////////////////////',soup.name)
    # print('soup.attrs////////////////////////////',soup.attrs)

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

        elif isinstance(value,str) and difflib.SequenceMatcher(None, value, inputstr).quick_ratio() > 0.3:
            # print('strCrea开始-----------------')
            # print(value)
            # print(inputstr)
            # print('--------------------------------------',difflib.SequenceMatcher(None, value, inputstr).quick_ratio())
            #
            # print('--------------------------------------',difflib.SequenceMatcher(None, value, inputstr).quick_ratio() > 0.3)
            # print(oneWord)
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
        cutWORD = re.findall("http.*//.*?/", link)[0]
        TrueUrl = link.replace(cutWORD, '').replace('?', '\?')
        findInputWordall = soup.findAll(href=(re.compile(TrueUrl)))
        # print('33333333333333333333333333333333333333333333333333333333333---列表页link--开始')
        # print("输入的link为：",TrueUrl)
        # print(findInputWordall)
        # print('33333333333333333333333333333333333333333333333333333333333---列表页link--结束')
        if not findInputWordall:
            continue
        for i in findInputWordall:
            xpathCode=strCreat(i,link)
            for findInputWord in i.parents:
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
    # print('33333333333333333333333333333333333333333333333333333333333---列表页title--开始')
    # print("输入的inputWord为：", inputWord)
    # print(findInputWord_all)
    # print('33333333333333333333333333333333333333333333333333333333333---列表页title--结束')
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

def dateOut(Index_Input_Url,Index_Input_pageUrl,Index_Input_Title,Content_Input_Url,Content_Input_Title,Content_Input_Word):
    dict = {}
    dict['splash_Content'] = 0
    dict['splash_list'] = 0
    indexHtml = getHtmlTrue(Index_Input_Url)
    ContentHtml = getHtmlTrue(Content_Input_Url)

    if not ContentHtml:
        # dict['Error'] = '入口页面没有打开'
        print('入口页面没有打开')
        return None
    else:
        ContentSoup = BeautifulSoup(ContentHtml['html'], 'lxml')
        Content_Title = XpathGet(ContentSoup, Content_Input_Title,Content_Input_Url[0])
        if Content_Title:
            Content_TitleXpathStr = [x for x in Content_Title if '///' not in x]
            dict['Content_Title'] = '|'.join(Content_TitleXpathStr)
        else:
            dict['Content_Title'] = 0

        Content_Word = []
        for n in Content_Input_Word:
            Content_Word_xpath = ContentXpathGet(ContentSoup,n,Content_Input_Url[0])
            print(Content_Word_xpath)
            if Content_Word_xpath:
                for i in Content_Word_xpath:
                    Content_Word.append(i)

        Content_Word2 = sorted(set(Content_Word), key=Content_Word.index)
        if Content_Word2:
            Content_Word3 = [xx for xx in Content_Word2]
            dict['Content_Text'] = '|'.join(Content_Word3)
        else:
            dict['Content_Text'] = 0

    if not indexHtml:
        print('正文页面没有打开')
        dict['Content_Title'] = '正文页面没有打开'
        dict['Content_Text'] = '正文页面没有打开'
        return None
    else:
        soup = BeautifulSoup(indexHtml['html'], 'lxml')
        dict['SiteName'] = getSiteNameAndDomain(soup)
        dict['startUrl'] = Index_Input_Url
        dict['CharSet'] = indexHtml['charset']
        listTitle = XpathGet(soup,Index_Input_Title,Content_Input_Url[0])

        if listTitle:
            dict['TitleList'] = '|'.join(listTitle)
        else:
            dict['TitleList'] = 0

        listlink = XpathListLinkGet(soup,Content_Input_Url)
        listlink_2 = sorted(set(listlink), key=listlink.index)
        if listlink_2:
            listlink_3 = [xx for xx in listlink_2]
            dict['LinkList'] = '|'.join(listlink_3)
        else:
            dict['LinkList'] = 0
        try:
            dict['SiteUrl'] = dict['startUrl'].replace('https://','').replace('http://','').split('/')[0]
        except:
            dict['SiteUrl'] = '没获取到网站域名，请在入口链接最后面，加个  / '

    if dict['LinkList'] == 0 or dict['TitleList'] == 0:
        splashRender = splash_render(Index_Input_Url)
        if splashRender=='null':
            dict['TitleList'] = 'splash没有成功渲染目标网站，请重新尝试'
            dict['LinkList'] = 'splash没有成功渲染目标网站，请重新尝试'
            dict['splash_list'] = 1
            return dict

        soup = BeautifulSoup(splashRender['html'], 'lxml')
        listTitle = XpathGet(soup, Index_Input_Title,Content_Input_Url[0])

        if listTitle:
            dict['TitleList'] = '|'.join(listTitle)
        else:
            dict['TitleList'] = '获取不到--列表页--文章标题'

        listlink = XpathListLinkGet(soup, Content_Input_Url)
        listlink_2 = sorted(set(listlink), key=listlink.index)
        if listlink_2:
            listlink_3 = [xx for xx in listlink_2]
            dict['LinkList'] = '|'.join(listlink_3)
        else:
            dict['LinkList'] = '获取不到--列表页--文章连接'
        dict['splash_list'] = 1



    if dict['Content_Title'] == 0 or dict['Content_Text'] == 0:
        splashRender = splash_render(Content_Input_Url[0])

        if splashRender=='null':
            dict['Content_Title'] = 'splash没有成功渲染目标网站，请重新尝试'
            dict['Content_Text'] = 'splash没有成功渲染目标网站，请重新尝试'
            dict['splash_Content'] = 1
            return dict


        ContentSoup = BeautifulSoup(splashRender['html'], 'lxml')
        Content_Title = XpathGet(ContentSoup, Content_Input_Title, Content_Input_Url[0])
        if Content_Title:
            Content_TitleXpathStr = [x for x in Content_Title if '///' not in x]
            dict['Content_Title'] = '|'.join(Content_TitleXpathStr)
        else:
            dict['Content_Title'] = '没有获取到文章内页标题，请检查是否粘贴有误'

        Content_Word = []
        for n in Content_Input_Word:
            Content_Word_xpath = ContentXpathGet(ContentSoup, n, Content_Input_Url[0])
            if Content_Word_xpath:
                for i in Content_Word_xpath:
                    Content_Word.append(i)

        Content_Word2 = sorted(set(Content_Word), key=Content_Word.index)
        if Content_Word2:
            Content_Word3 = [xx for xx in Content_Word2]
            dict['Content_Text'] = '|'.join(Content_Word3)
        else:
            dict['Content_Text'] = '没有获取到文章内页正文，请查看是否带着链接信息一起粘贴过来的'

        dict['splash_Content'] = 1
        dict['pageUrl'] = str(Index_Input_pageUrl)

    return dict


if __name__ == "__main__":


    Index_Input_Url = 'https://new.qq.com/ch/tech/'
    Index_Input_Title = '界首富贝索斯加速抛售亚马逊股'
    Content_Input_Url = ['https://new.qq.com/omn/20190806/20190806A07ZBF00.html',
                         'https://new.qq.com/omn/TEC20190/TEC2019080600450100.html',
                         'https://new.qq.com/omn/20190806/20190806A02VHI00.html'
                         ]

    Content_Input_Title = '界首富贝索斯加速抛售亚马逊股'

    Content_Input_Word = ['富贝索斯正在变现他所持有的亚马逊股',
                          '前仍然拥有超过5700万股亚马逊股',
                          '为无家可归的家庭提供帮助，并支持学']


    # Index_Input_Url = 'http://www.zjzfcg.gov.cn/purchaseNotice/index.html?categoryId=3001'
    # Index_Input_Title = '台州市公安局集聚区分局集聚区350兆警用无线数字集群系统通信资源租用服务的'
    # Content_Input_Url = ['http://www.zjzfcg.gov.cn/innerUsed_noticeDetails/index.html?noticeId=5966981']
    #
    #
    # Content_Input_Title = '限公司关于台州市公安局集聚区分局集聚区350兆警用无线数字集群系统通信资源'
    # Content_Input_Word = ['TPTZ-2019-TZ0704',
    #                       '列入失信被执行人、重大税收违法案件当事人名单、政府采购严重违法失信行为',
    #                       '3、同级政府采购监督管理部门名称：']


    aa = dateOut(Index_Input_Url=Index_Input_Url,
                 Index_Input_Title=Index_Input_Title,
                 Content_Input_Url=Content_Input_Url,
                 Content_Input_Title = Content_Input_Title,
                 Content_Input_Word=Content_Input_Word)
    pprint.pprint(aa)
    print(aa)

