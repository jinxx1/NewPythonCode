# -*- coding: utf-8 -*-
import requests,json,pprint
import redis,time,datetime,re,sys
from io import BytesIO
import pandas as pd
import threading,os,sys,random
from PIL import Image as Image
from bs4 import BeautifulSoup
import pymysql
import sqlalchemy
import emoji,io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

from weixinToken2db import mysqlcon,run_main,TOKENINFO
from getWebArticle import mysqlcon128


def WX_Token(name = None):
    a = mysqlcon.execute('select * from weixinToken where id=1')
    ddict = {}
    for num,i in enumerate(a):
        if num >0:
            break
        ddict['uxuepai88'] = i[1]
        ddict['5G'] = i[2]
        ddict['energy'] = i[3]
        ddict['light'] = i[4]
    if not name:
        return ddict
    elif name == 'uxuepai88':
        return ddict['uxuepai88']
    elif name == '5G':
        return ddict['5G']
    elif name == 'energy':
        return ddict['energy']
    elif name == 'light':
        return ddict['light']
    else:
        return None

def getAllmediaid():
    a = mysqlcon128().execute('SELECT DISTINCT title FROM U1LINK_post;')
    return tuple([x[0] for x in a])

def getImgContent(imgurl):
    ddict = {}
    imgbrow = requests.get(imgurl)
    aa = BytesIO(imgbrow.content)
    ddict['imgCoverByes'] = BytesIO(imgbrow.content)
    iimg = ImagePIL.open(aa).size
    argV = iimg[0]/iimg[1]
    if round(argV,1) < 1.2:
        ddict['imgCoverYN'] = 1#正方形小兔
    else:
        ddict['imgCoverYN'] = 0

    # ddict['imgCoverByes'] = imgurl
    return ddict

def getUrlslug():
    ttime = str(int(time.time()) * 1000)
    ranStr = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', 26, )
    slugUrl = ttime + '_' + ''.join(ranStr)
    return slugUrl

def processHTMLimg(html):
    retuHtml = str(html)
    soup = BeautifulSoup(html,'lxml')
    for i in soup.find_all('img'):
        imgUrl = i.get('data-src')
        if imgUrl:
            # print("imgUrl")
            # print(imgUrl)
            replaceWord = "<img {}>".format(str(imgUrl))
            retuHtml = retuHtml.replace(str(i),replaceWord)
    return retuHtml

def getTime(num):
    for n in range(num,0,-1):
        yesterday = datetime.datetime.today() + datetime.timedelta(-n)
        yesterday_format = yesterday.strftime('%Y-%m-%d')
        yield yesterday_format

def yesList(name,days):
    llist = []
    get_wxPostedAriticle = mysqlcon128().execute('select title,url from wxPostedAriticle where name = "{}"'.format(name))
    retDict = {}
    retDict['titleList'] = []
    retDict['urlList'] = []
    for i in get_wxPostedAriticle:
        retDict['titleList'].append(i[0])
        retDict['urlList'].append(i[1])

    apiUrl = 'https://api.weixin.qq.com/datacube/getarticletotal?access_token={}'.format(WX_Token(name))
    for timeT in getTime(days):
        apiDate = {"begin_date": timeT,"end_date": timeT}
        apiBrow = requests.post(url=apiUrl, data=json.dumps(apiDate))
        apiBrow.encoding = 'utf-8'
        try:
            apijsonT = json.loads(apiBrow.text)['list']
        except:
            return None
        for i in apijsonT:
            ddict = {}
            if i['title'] in retDict['titleList'] or i['url'] in retDict['urlList']:
                continue
            ddict['title'] = i['title']
            ddict['url'] = i['url']
            ddict['ref_date'] = i['ref_date']
            ddict['name'] = name
            retDict['titleList'].append(ddict['title'])
            retDict['urlList'].append(ddict['url'])
            llist.append(ddict)
    df = pd.DataFrame(llist)

    try:
        df.to_sql(name='wxPostedAriticle', con=mysqlcon128(), if_exists='append', index=False)
    except:
        pass
    return retDict

def get_static(infodict,coverGet = True):

    contentImgurl = re.findall("<img.*?>", infodict['body'])
    if not contentImgurl:
        return infodict

    timePath = infodict['timeYmd'] + '/'
    filePath_slug = timePath + infodict['slug'] + '/'
    root = os.path.abspath(os.path.dirname(__file__))
    try:
        basePath = root + '/' + filePath_slug
        os.makedirs(basePath)
    except:
        basePath = root + '/' + timePath + infodict['slug'] + 'correction/'
        os.makedirs(basePath)
    infodict['staticPath'] = basePath
    #
    # with open(basePath + '/content0.html','w',errors='ignore') as file:
    #     file.write(infodict['body'])
    #     file.flush()



    for num,i in enumerate(contentImgurl):
        try:
            imgUrl = re.findall("img.(.*?)>", i,re.M|re.S)[0]
            if '=png' in imgUrl or '=PNG' in imgUrl:
                imgName = 'pic' + str(num) + '.png'
            elif '=gif' in imgUrl or '=GIF' in imgUrl:
                imgName = 'pic' + str(num) + '.gif'
            elif '=jpeg' in imgUrl or '=JPEG' in imgUrl:
                imgName = 'pic' + str(num) + '.jpeg'
            else:
                imgName = 'pic' + str(num) + '.jpg'
            imgSTATIC = up_download_ContentIMG(imgurl=imgUrl,name=imgName,basePath=basePath,filePath_slug=filePath_slug)
            imgHtml = r'''<img src="{}">'''.format(imgSTATIC)
        except:
            continue
        infodict['body'] = infodict['body'].replace(str(i), imgHtml).replace(u'\xa0', u' ').replace(u'\u25b7', u' ')
    if coverGet:
        if 'png' in infodict['cover'] or 'PNG' in infodict['cover']:
            coverName = 'cover.png'
        elif 'gif' in infodict['cover'] or 'GIF' in infodict['cover']:
            coverName = 'cover.gif'
        elif 'jpeg' in infodict['cover'] or 'JPEG' in infodict['cover']:
            coverName = 'cover.jpeg'
        else:
            coverName = 'cover.jpg'


        cover_STATIC = up_download_ContentIMG(imgurl=infodict['cover'], name=coverName, basePath=basePath, filePath_slug=filePath_slug)
        infodict['cover'] = cover_STATIC
    else:
        infodict['cover'] = ''
    try:
        del infodict['timeYmd']
    except:
        pass
    with open(basePath + '/content.html','w',encoding='utf-8',errors='ignore') as file:
        file.write("<head><meta charset=\"UTF-8\"><title>{}</title></head>".format(infodict['title']) + infodict['body'])
        file.flush()
    # with open(basePath + '/ORT_content.html','w',errors='ignore') as file:
    #     file.write(infodict['oriContent'])
    #     file.flush()
    return infodict

def up_download_ContentIMG(imgurl, name, basePath, filePath_slug):
    imgbrow = requests.get(imgurl)

    with open(basePath + name, 'wb') as imgfile:
        imgfile.write(imgbrow.content)

    if 'cover' in name:
        imgDict = {}
        imgDict['imgPath'] = basePath + name
        imgDict['imgName'] = name
        imgDict['root'] = basePath
        process_image_Backup(imgDict)

    url = 'http://static.u1link.com/ArticleImg/' + filePath_slug + name
    return url

def process_image_Backup(ddict, mwidth=180, mheight=140):

    if 'cover' in ddict['imgName']:
        imgName_out = ddict['imgName'].replace('coverBackup','cover')
        imgName_bei = ddict['imgName'].replace('cover', 'coverBackup')

    elif 'conver' in ddict['imgName']:
        imgName_out = ddict['imgName'].replace('converBackup','conver')
        imgName_bei = ddict['imgName'].replace('conver', 'coverBackup')
    else:
        return None

    imgPath = ddict['imgPath']
    image = Image.open(imgPath)
    image.save(ddict['root'] + '/' + imgName_bei)
    w, h = image.size

    if w <= mwidth and h <= mheight:
        print(imgPath, 'is OK.')
        return None

    if (1.0 * w / mwidth) > (1.0 * h / mheight):
        scale = 1.0 * w / mwidth
        new_im = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)

    else:
        scale = 1.0 * h / mheight
        new_im = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)

    new_im.save(ddict['root'] + '/' + imgName_out)
    return ddict['root'] + '/' + imgName_out

def precessweixinContent(html,title):
    orthtml = html
    soup = BeautifulSoup(html, 'lxml')
    ALLHTML = soup.find('body')
    ContentWord = emoji.demojize(str(ALLHTML))
    retContentWord = processHTMLimg(ContentWord)
    return retContentWord





if __name__ == '__main__':

    dupcut = getAllmediaid()
    # dupcut = ()
    brk = 0
    allList = []
    for num,name in enumerate(TOKENINFO):
        # if name != '5G':
        #     continue
        yesInfo = yesList(name=name,days=3)
        if not yesInfo:
            # print('yesInfo  error')
            continue
        offsetNum = 0
        while True:
            if brk > 5:
                brk = 0
                break
            # brk = 600
            countNum = 1
            getType = 'news'
            newsApiDate = {
                "type": getType,
                "offset": offsetNum,
                "count": countNum
            }
            newsApi = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={}'.format(
                WX_Token(name))
            newBrow = requests.post(url=newsApi, data=json.dumps(newsApiDate))
            newBrow.encoding = 'utf-8'
            if 'errcode' in newBrow.text:
                # print('errorDate--------------------',name)
                # print(newBrow.text)
                # print('errorDate--------------------', name)
                break
            newsjsonT = json.loads(newBrow.text)['item']


            for num, i in enumerate(newsjsonT):
                ddict = {}
                ddict['media_id'] = i['media_id']
                ddict['publish'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(i['update_time'])))
                for nn in i['content']['news_item']:
                    if nn['title'] in dupcut:
                        # print('title in dupcut')
                        brk += 1
                        continue
                    if nn['title'] in yesInfo['titleList'] or nn['url'] in yesInfo['urlList']:

                    # if True:
                        ddict['timeYmd'] = time.strftime('%Y%m%d', time.localtime(int(i['update_time'])))
                        ddict['title'] = nn['title']
                        ddict['weixinID'] = TOKENINFO[name]['weixinCHNAME']
                        ddict['type'] = TOKENINFO[name]['type']
                        ddict['slug'] = getUrlslug() + '_weixin'
                        ddict['cover'] = nn['thumb_url']
                        ddict['summary'] = nn['digest']
                        ddict['created'] = str(datetime.datetime.now())
                        ddict['updated'] = str(datetime.datetime.now())
                        ddict['oriContent'] = nn['content']
                        try:
                            ddict['body'] = precessweixinContent(nn['content'],title=ddict['title'])
                        except:
                            # print('body error')
                            continue
                        ddict['ArtUrl'] = nn['url']


                        if brk > 0:
                            brk = brk - 1
                        try:
                            dfINFO = get_static(infodict=ddict)
                        except:
                            continue
                        if 'qpic.cn' in dfINFO['cover']:
                            del dfINFO['cover']

                        try:
                            del dfINFO['timeYmd']
                        except:
                            pass

                        del dfINFO['oriContent']
                        allList.append(dfINFO)

                        print('dfINFO')
                        print(dfINFO)
                        print('--------------------------')

            offsetNum = offsetNum + countNum + 1


    try:
        dfall = pd.DataFrame(allList)
        dfall.drop_duplicates('ArtUrl','first',inplace = True)
        dfall.to_sql(name='U1LINK_post', con=mysqlcon128(), if_exists='append', index=False,chunksize=1000)
    except AttributeError:
        print('AttributeError------weixin')
