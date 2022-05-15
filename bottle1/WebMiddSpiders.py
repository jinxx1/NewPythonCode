#-*-coding:utf-8
# from codespider import dateOut
# from newDef import dateOut
from SpiderTestModel import testSpider
from CssGetDef import *
from sql_in import mysql_indata,mysql_seach,mysql_yes
from bottle import route,run,static_file,error,abort,redirect,request,Response
import json
import datetime
import time

@route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        htmlstr = f.read()
        f.close()
    return htmlstr
@route('/get')
def getp():

    Index_Input_Url = str(request.query.url)
    Index_Input_pageUrl = str(request.query.pageUrl)
    Index_Input_Title = str(request.query.TitleList)
    Content_Input_Title = str(request.query.TitleContent)
    Content_Input_Word1 = str(request.query.Tag1)
    Content_Input_Word2 = str(request.query.Tag2)
    Content_Input_Word3 = str(request.query.Tag3)
    Content_Input_uPR = str(request.query.uPR)
    Content_Input_catName = str(request.query.catName)
    Content_Input_imgDownload = str(request.query.imgDownload)

    Content_Input_Url = []
    Content_Input_Url_1 = str(request.query.contenturl_1)
    Content_Input_Url.append(Content_Input_Url_1)
    Content_Input_Url_2 = str(request.query.contenturl_2)
    if Content_Input_Url_2:
        Content_Input_Url.append(Content_Input_Url_2)
    Content_Input_Url_3 = str(request.query.contenturl_3)
    if Content_Input_Url_3:
        Content_Input_Url.append(Content_Input_Url_3)
    Content_Input_Url_4 = str(request.query.contenturl_4)
    if Content_Input_Url_4:
        Content_Input_Url.append(Content_Input_Url_4)
    Content_Input_Url_5 = str(request.query.contenturl_5)
    if Content_Input_Url_5:
        Content_Input_Url.append(Content_Input_Url_5)
    Content_Input_Url_6 = str(request.query.contenturl_6)
    if Content_Input_Url_6:
        Content_Input_Url.append(Content_Input_Url_6)

    getDict = {
        'get_url': Index_Input_Url,
        'pageUrl': Index_Input_pageUrl,
        'get_TitleContent': Content_Input_Title,
        'get_contenturl': Content_Input_Url,
        'get_TitleList': Index_Input_Title,
        'get_Tag': Content_Input_Word1,
        'get_Tag2': Content_Input_Word2,
        'get_Tag3': Content_Input_Word3,
        'uPR': Content_Input_uPR,
        'catName': Content_Input_catName,
        'imgDownload': Content_Input_imgDownload
    }

    Content_Input_Word = [Content_Input_Word1,Content_Input_Word2,Content_Input_Word3]
    xpathCodeDict = dateOut(Index_Input_Url,Index_Input_pageUrl,Index_Input_Title,Content_Input_Url,Content_Input_Title,Content_Input_Word)
    sqlinDict = {**getDict, **xpathCodeDict}
    sqlId = mysql_indata(sqlinDict)

    a1 = '你输入的列表地址为：{}'.format(sqlinDict['get_url'])+ '</br>'
    a19 = '你输入的列表地址为：{}'.format(sqlinDict['pageUrl'])+ '</br>'
    a2 = '你输入的列表标题为：{}'.format(sqlinDict['get_TitleList'])+ '</br>'
    a3 = '你输入的样文链接为：{}'.format(sqlinDict['get_contenturl'])+ '</br>'
    a4 = '你输入的样文标题为：{}'.format(sqlinDict['get_TitleContent'])+ '</br>'
    a5 = '你输入的样文正文第一段节选为：{}'.format(sqlinDict['get_Tag'])+ '</br>'
    a6 = '你输入的样文正文中间段节选为：{}'.format(sqlinDict['get_Tag2'])+ '</br>'
    a7 = '你输入的样文正文任意段节选为：{}'.format(sqlinDict['get_Tag3'])+ '</br>'
    a8 = '网站名称：{}'.format(sqlinDict['SiteName'])+ '</br>'
    a9 = '网站主域名：{}'.format(sqlinDict['SiteUrl'])+ '</br>'
    a10 = '网站文字编码为：{}'.format(sqlinDict['CharSet'])+ '</br>'
    a11 = '入口页为：{}'.format(sqlinDict['startUrl'])+ '</br>'
    a12 = '入口页标题列表Xpath：{}'.format(sqlinDict['TitleList'])+ '</br>'
    a13 = '入口页标题链接Xpath：{}'.format(sqlinDict['LinkList'])+ '</br>'
    a14 = '正文页标题Xpath：{}'.format(sqlinDict['Content_Title'])+ '</br>'
    a15 = '正文页内容Xpath：{}'.format(sqlinDict['Content_Text'])+ '</br>'
    a16 = '本爬虫权重为：{}'.format(sqlinDict['uPR']) + '</br>'
    a17 = '本爬虫类别为：{}'.format(sqlinDict['catName']) + '</br>'
    a18 = '是否下载图片，（0 禁止下载，1 允许下载）您的选择是：{}'.format(sqlinDict['imgDownload']) + '</br>'


    word = a1+a2+a3+a4+a5+a6+a7+a8+a9+a10+a11+a12+a13+a14+a15+a16+a17+a18 + a19
    yesButton = '<p><a href="./test/{}" target="_blank">点此测试爬取结果</a></p>'.format(str(sqlId))
    seachID = '<p><a href="./id/{}" target="_blank">查看数据字典</a></p>'.format(str(sqlId))
    return word + yesButton + seachID



@route('/yes/<id>')
def yes(id):
    return mysql_yes(int(id))


@route('/test/<id>')
def test(id):
    xpathCodeDict= mysql_seach(id)[0]
    spiderTestConDictList = testSpider().testspider(xpathCodeDict)
    # pprint.pprint(spiderTestConDictList)
    enCode = xpathCodeDict['CharSet']

    import chardet


    testAll = ''
    for i in range(len(spiderTestConDictList['ContentTitle'])):
        # list_Title = '入口页显示标题为：' + spiderTestConDictList['ListTitle'][i] + '\n' + '</br>'
        # print(spiderTestConDictList['ContentTitle'][i])
        # print(type(spiderTestConDictList['ContentTitle'][i]))
        # fencoding1 = chardet.detect(spiderTestConDictList['ContentTitle'][i])
        # fencoding2 = chardet.detect(spiderTestConDictList['ListLink'][i])
        # fencoding3 = chardet.detect(spiderTestConDictList['ContentWord'][i])
        # print(fencoding1)
        zhong_Title = '文章标题为：' + spiderTestConDictList['ContentTitle'][i] + '\n' + '</br>'
        zhong_Link = '文章链接为：' + spiderTestConDictList['ListLink'][i] + '\n' + '</br>'
        zhong_Content = '文章正文为：' + spiderTestConDictList['ContentWord'][i] + '\n' + '</br>'
        cutPont = '--------------------------------------------------Page End-------------------------------------------------\n' + '</br>'
        i_All = zhong_Title + zhong_Link + zhong_Content + cutPont
        testAll = testAll + i_All

    yesButton = '<p><a href="/yes/{}" target="_blank">确认无误，可以提交</a></p>'.format(str(id))
    warning = '<p><b>此页面为爬虫测试页面。若抓取信息无误，请下拉到本页最末。点击确认连接。</b></p>'
    testAllFinal = warning + testAll + yesButton

    return (testAllFinal)



@route('/id/<id>')
def ids(id):
    resultes = mysql_seach(int(id))[0]
    resultes['Time_now'] = resultes['Time_now'].strftime('%Y-%m-%d %H:%M:%S')
    return resultes

@error(500)
def err(err):
    errorWord = '''
    <p><b>error  500</b></p>
    <p><b>出现抓取错误了。</b></p>
    <p><b>换篇样本文章试试</b></p>
    <p><b>注意，“列表页”和“样本文章内页”的标题请务必一致。尤其注意“副标题”或“两行标题”情况。这将导致抓取失败</b></p>
    <p><b>请换一篇样文试试，需要标题一致的样文</b></p>
    <p><b>换样文时，别忘把链接地址也更换掉。否则，程序也会出错</b></p>
    <p><b>在保证您输入信息无误的前提下，换了几次，还是无法抓取。那说明本网站有反爬虫措施。请将该网站交给靳潇处理。</b></p>
    '''
    return errorWord

@error(404)
def err(err):
    errorWord = '''
    <p><b>error  404</b></p>
    <p><b>别瞎搞！我根本没做这个页面</b></p>
    '''
    return errorWord



run(host='0.0.0.0',port=6801,debug=True,reloader=True)

# run(port=,debug=True,reloader=True)





# mysql建表信息
'''
base=dev_umxh

DROP TABLE IF EXISTS `MiddlewareXPATH`;
CREATE TABLE `MiddlewareXPATH` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `CharSet` varchar(20) DEFAULT '' COMMENT '页面编码格式',
  `Content_Text` varchar(200) DEFAULT '' COMMENT '样本内容页-正文-xpath代码',
  `Content_Title` varchar(200) DEFAULT '' COMMENT '样本内容页-标题-xpath代码',
  `LinkList` varchar(200) DEFAULT '' COMMENT '样本入口list页所有文章列表-xpath代码',
  `SiteName` varchar(200) DEFAULT '' COMMENT '网站中文名称',
  `SiteUrl` varchar(200) DEFAULT '' COMMENT '网站主域名',
  `TimeList` varchar(200) DEFAULT NULL COMMENT '样本入口list页所有文章列表-时间-xpath代码',
  `TitleList` varchar(200) DEFAULT NULL COMMENT '样本入口list页所有文章列表-标题-xpath代码',
  `cutPoint` varchar(10) DEFAULT '0' COMMENT '时间格式分隔符',
  `startUrl` varchar(200) DEFAULT '0' COMMENT '入口list页链接',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=286 DEFAULT CHARSET=utf8mb4;

'''
