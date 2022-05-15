# -*- coding: utf-8 -*-
import datetime
from cicCrawl.settings import IMGROOT
from PIL import Image
from urllib import parse
import os, requests, re,json,pymysql,time,random

def get_timeYmd(date):
    ttime = date
    time_array = time.strptime(ttime, "%Y-%m-%d %H:%M:%S")
    timeL1 = int(time.mktime(time_array))
    timeL = time.localtime(int(timeL1))
    infodict = time.strftime("%Y%m%d", timeL)
    return infodict
def get_slug():
    ttime = str(int(time.time()) * 1000)
    ranStr = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', 26, )
    slugUrl = ttime + '_' + ''.join(ranStr)
    return slugUrl

def get_static(infodict, coverGet=True):

    # print(infodict['cover'])
    infodict['staticPath'] = ''
    infodict['timeYmd'] = get_timeYmd(infodict['publishTime'])
    infodict['slug'] = get_slug()
    imgregx = re.findall("<img.*?>", infodict['body'])
    if not imgregx:
        # print('no imgregx')
        return infodict

    for i in imgregx:
        try:
            imgSrc = re.findall("src=\"(.*?)\"", i)[0]
            imgUrl = '<img src="' + parse.urljoin(infodict['url'], imgSrc) + '">'
        except:
            # print('------------------------------37')
            continue
        infodict['body'] = infodict['body'].replace(i, imgUrl)

    contentImgurl = re.findall("<img.*?>", infodict['body'])
    if not contentImgurl:
        return infodict

    timePath = infodict['timeYmd'] + '/'
    filePath_slug = timePath + infodict['slug'] + '/'
    root = IMGROOT

    try:
        basePath = root + '/' + filePath_slug
        os.makedirs(basePath)
        infodict['staticPath'] = basePath
    except:
        print('excpt --- 50')
        basePath = root + '/' + timePath + infodict['slug'] + 'correction/'
        os.makedirs(basePath)
        infodict['staticPath'] = basePath

    for num, i in enumerate(contentImgurl):
        try:
            imgUrl = re.findall("img src=\"(.*?)\">", i, re.M | re.S)[0]

            if 'png' in imgUrl or 'PNG' in imgUrl:
                imgName = 'pic' + str(num) + '.png'
            elif 'gif' in imgUrl or 'GIF' in imgUrl:
                imgName = 'pic' + str(num) + '.gif'
            elif 'jpeg' in imgUrl or 'JPEG' in imgUrl:
                imgName = 'pic' + str(num) + '.jpeg'
            elif 'jpg' in imgUrl or 'JPG' in imgUrl:
                imgName = 'pic' + str(num) + '.jpg'
            else:

                continue

            imgSTATIC = up_download_ContentIMG(imgurl=imgUrl, name=imgName, basePath=basePath,
                                           filePath_slug=filePath_slug)
            if imgSTATIC:
                imgHtml = r'''<img src="{}">'''.format(imgSTATIC)
            else:
                continue
        except:
            # print('excpt --- 75')
            continue
        infodict['body'] = infodict['body'].replace(str(i), imgHtml)

    if coverGet and infodict['cover']:
        if 'png' in infodict['cover'] or 'PNG' in infodict['cover']:
            coverName = 'cover.png'
        elif 'gif' in infodict['cover'] or 'GIF' in infodict['cover']:
            coverName = 'cover.gif'
        elif 'jpeg' in infodict['cover'] or 'JPEG' in infodict['cover']:
            coverName = 'cover.jpeg'
        elif 'jpg' in imgUrl or 'JPG' in imgUrl:
            coverName = 'cover.jpg'
        else:
            coverName = ''

        if coverName:
            cover_STATIC = up_download_ContentIMG(imgurl=infodict['cover'], name=coverName, basePath=basePath,
                                              filePath_slug=filePath_slug)
            if cover_STATIC:
                infodict['cover'] = cover_STATIC
            else:
                infodict['cover'] = ''
        else:
            infodict['cover'] = ''
    else:
        infodict['cover'] = ''
    return infodict

def up_download_ContentIMG(imgurl, name, basePath, filePath_slug):

    try:

        imgbrow = requests.get(imgurl)

        print(imgbrow.status_code)
        print('--------------------------imgbrow.status_code----------------------')


        if imgbrow.status_code > 300:
            # print('excpt --- 106')
            return None

    except Exception as aaa:
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print('excpt --- aaaaaa')
        print(imgurl)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        return None

    with open(basePath + name, 'wb') as imgfile:
        imgfile.write(imgbrow.content)
        print('保存图片',basePath + name)

    if 'cover' in name:
        imgDict = {}
        imgDict['imgPath'] = basePath + name
        imgDict['imgName'] = name
        imgDict['root'] = basePath
        try:
            process_image_Backup(imgDict)
        except:
            pass
    url = 'http://xhimg.u1link.com/' + filePath_slug + name
    return url

def process_image_Backup(ddict, mwidth=272, mheight=152):
    if 'cover' in ddict['imgName']:
        imgName_out = ddict['imgName'].replace('coverBackup', 'cover')
        imgName_bei = ddict['imgName'].replace('cover', 'coverBackup')

    elif 'conver' in ddict['imgName']:
        imgName_out = ddict['imgName'].replace('converBackup', 'conver')
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






class CicMYSQLPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):

        self.db = pymysql.connect(self.host, self.user, self.password, self.database, port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):

        item = get_static(item)

        keysWord = "summary,cover,body,programa_dictionaries,publishTime,source,subtopic_dictionaries,title,url,created,updated,staticPath"
        valueWord = '''"{summary}","{cover}","{body}",{programa_dictionaries},"{publishTime}","{source}",{subtopic_dictionaries},"{title}","{url}","{created}","{updated}","{staticPath}"'''
        insert_code = '''INSERT INTO jou_journalism({}) VALUES ({});'''.format(keysWord, valueWord)
        TTime = str(datetime.datetime.now())
        inser_excut = insert_code.format(
            summary = pymysql.escape_string(item['summary']),
            body = pymysql.escape_string(item['body']),
            programa_dictionaries = item['programa_dictionaries'],
            subtopic_dictionaries = item['subtopic_dictionaries'],
            publishTime = pymysql.escape_string(item['publishTime']),
            source = pymysql.escape_string(item['source']),
            title = pymysql.escape_string(item['title']),
            url = pymysql.escape_string(item['url']),
            created = pymysql.escape_string(TTime),
            updated = pymysql.escape_string(TTime),
            staticPath = pymysql.escape_string(item['staticPath']),
            cover = pymysql.escape_string(item['cover'])
        )

        # self.cursor.execute(inser_excut)
        # self.db.commit()

        import pprint
        item['body'] = len(item['body'])
        pprint.pprint(item)
        print('--------------------------------------------')

        return item



class CiccrawlPipeline:
    def process_item(self, item, spider):
        return item
