# -*- coding: utf-8 -*-

import requests,json,pprint
import time,datetime,re
import pandas as pd
import os,random
from PIL import Image as Image
from bs4 import BeautifulSoup
import sqlalchemy
import emoji,jieba
from flask import Flask
from flask import request,jsonify
import json
from flask import render_template

app = Flask(__name__)

def mysqlcon128():
    with open('MYSQLINFO.json', 'r') as f:
        MYSQLINFO = json.loads(f.read())
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'NAME'])
    return sqlalchemy.create_engine(conStr)
mysqldb = mysqlcon128()

def request_URL(url):
    brow = requests.get(url)
    return brow.text

def getUrlslug():
    ttime = str(int(time.time()) * 1000)
    ranStr = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', 26, )
    slugUrl = ttime + '_' + ''.join(ranStr)
    return slugUrl

def precessweixinContent(html):
    ALLHTML = ''
    soup = BeautifulSoup(html,"lxml")
    ALLLIST = soup.find_all(class_= "rich_media_content")
    for i in ALLLIST:
        ALLHTML = ALLHTML + str(i)

    ContentWord = emoji.demojize(str(ALLHTML))
    retContentWord = processHTMLimg(ContentWord)
    return retContentWord

def processHTMLimg(html):
    retuHtml = str(html)
    soup = BeautifulSoup(html,"lxml")
    for i in soup.find_all('img'):
        imgUrl = i.get('data-src')
        if imgUrl:
            # print("imgUrl")
            # print(imgUrl)
            replaceWord = "<img {}>".format(str(imgUrl))
            retuHtml = retuHtml.replace(str(i),replaceWord)
    return retuHtml

def get_keysList():
    get_catKeys= mysqldb.execute("select id,keysJson from U1LINK_post_cat")
    llist = []
    for i in get_catKeys:
        ddict = {}
        ddict['ID'] = i[0]
        ddict['json'] = json.loads(i[1])
        llist.append(ddict)
    # 更新jieba词典
    dup = []
    for i in llist:
        kkeys = i['json']['single']
        for nn in kkeys:
            if nn in dup:
                continue
            else:
                dup.append(nn)

        if i['json']['both']:
            for nn in i['json']['both']:
                for nnn in nn:
                    if nnn in dup:
                        continue
                    else:
                        dup.append(nnn)
    for i in dup:
        jieba.add_word(i)

    return llist

def get_type(title,keysList = None):
    if not keysList:
        keysList = get_keysList()

    jiebacutlist = jieba.lcut_for_search(title)
    for num, keyList in enumerate(keysList):
        retC = list(set(jiebacutlist).intersection(set(keyList['json']['single'])))
        if retC:
            typenum = keyList['ID']
            break
        elif not retC and keyList['json']['both']:
            for num, bothkeys in enumerate(keyList['json']['both']):
                if bothkeys[0] in jiebacutlist and bothkeys[1] in jiebacutlist:
                    typenum = keyList['ID']
                    break
        else:
            typenum = 2

    return typenum

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

def main(inputUrl):

    request_brow = request_URL(inputUrl.strip())

    title = re.findall(r"title.*content=\"(.*?)\"",request_brow)[0]
    description = re.findall(r"description.*content=\"(.*?)\"", request_brow)[0]
    image = re.findall(r"image.*content=\"(.*?)\"", request_brow)[0]
    weixinID = re.findall(r"var.nickname.=.\"(.*?)\"", request_brow)[0]
    ArtUrl = re.findall(r"url.*content=\"(.*?)\"", request_brow)[0]

    ddict = {}
    ddict['timeYmd'] = time.strftime('%Y%m%d', time.localtime(int(time.time())))
    ddict['title'] = title + "_微信转载"
    ddict['weixinID'] = weixinID
    ddict['type'] = get_type(title)
    ddict['slug'] = getUrlslug() + '_weixin'
    ddict['cover'] = image
    ddict['summary'] = description
    ddict['created'] = str(datetime.datetime.now())
    ddict['updated'] = str(datetime.datetime.now())
    ddict['body'] = precessweixinContent(request_brow).replace('visibility: hidden','')
    ddict['ArtUrl'] = ArtUrl
    ddict['publish'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))


    dfINFO = get_static(infodict=ddict)
    dfall = pd.DataFrame([dfINFO])
    dfall.to_sql(name='U1LINK_post', con=mysqlcon128(), if_exists='append', index=False,chunksize=1000)


    if dfINFO['type'] == 1:
        dfINFO['type'] = '5G产业'
    if dfINFO['type'] == 2:
        dfINFO['type'] = '通信服务'
    if dfINFO['type'] == 3:
        dfINFO['type'] = '智慧灯杆'
    if dfINFO['type'] == 4:
        dfINFO['type'] = '能源电力'
    if dfINFO['type'] == 5:
        dfINFO['type'] = '无类型'
    if dfINFO['type'] == 6:
        dfINFO['type'] = '工业互联'
    if dfINFO['type'] == 7:
        dfINFO['type'] = '新基建'
    if dfINFO['type'] == 8:
        dfINFO['type'] = '行业政策'
    if dfINFO['type'] == 9:
        dfINFO['type'] = '大咖说'
    if dfINFO['type'] == 10:
        dfINFO['type'] = '资本市场'

    if len(dfINFO['summary']) <1:
        dfINFO['summary'] = '无简介'
    # dfINFO['body'] = "content.html"
    word = '''
<p></p>
<p></p>
<p> 完整链接地址：{ArtUrl}</p>
<p> 缩略图地址：{cover}</p>
<p> 标题：{title}</p>
<p> 简介：{summary}</p>
<p> 来源：{type}</p>
<p> 分类：{weixinID}</p>
    '''.format(ArtUrl = dfINFO['ArtUrl'],
               cover = dfINFO['cover'],
               title = dfINFO['title'],
               summary = dfINFO['summary'],
               weixinID = dfINFO['type'],
               type = dfINFO['weixinID'])
    return word
@app.route('/postapi',methods=['POST'])
def postPage():
    Index_Input_Url = str(request.values.get('url')).strip()
    if request.method == 'POST':
        if 'https://mp.weixin.qq.com/' in Index_Input_Url or 'http://mp.weixin.qq.com/' in Index_Input_Url:
            try:
                htmlword = main(Index_Input_Url)
                return htmlword
            except Exception as ff:
                return ff
        else:
            return "<p>请用https://mp.weixin.qq.com/.....或者http://mp.weixin.qq.com/....</p>的链接"
    else:
        return "<p>请用post形式</p>"

@app.route('/')
def index():
    html = '''
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>微信文章手工上传</title>
<style>
input{
outline-style: none ;
border: 1px solid #ccc; 
border-radius: 3px;
padding: 13px 14px;
width: 820px;
font-size: 14px;
font-weight: 500;
font-family: "Microsoft soft";
}
</style>
</head>
<div>
<form method = "post" action = "/postapi">
<input type = "text" name="url" required="required" rows="20" cols="30"/>
<ul>请输入微信链接</ul>
<button type='submit'>提交</button>
</form>
</div>
</html>
        '''
    return html
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5010)







