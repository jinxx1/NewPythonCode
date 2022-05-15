# -*- coding: utf-8 -*-
import jieba


from u1webcrwal.u1parse import get_3days_title,string_similar
from u1webcrwal.settings import IMGROOT
from PIL import Image
from urllib import parse
import os, requests, re,json,pymysql

def update_jieba(cursor):
    cursor.execute("select id,keysJson from U1LINK_post_cat")
    get_catKeys = cursor.fetchall()
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

def get_static(infodict, coverGet=True):
    infodict['staticPath'] = ''
    imgregx = re.findall("<img.*?>", infodict['body'])
    if not imgregx:
        return infodict

    for i in imgregx:
        try:
            imgSrc = re.findall("src=\"(.*?)\"", i)[0]
            imgUrl = "<img " + parse.urljoin(infodict['ArtUrl'], imgSrc) + ">"
        except:
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
        basePath = root + '/' + timePath + infodict['slug'] + 'correction/'
        os.makedirs(basePath)
        infodict['staticPath'] = basePath

    for num, i in enumerate(contentImgurl):
        try:
            imgUrl = re.findall("img.(.*?)>", i, re.M | re.S)[0]

            if 'png' in imgUrl or 'PNG' in imgUrl:
                imgName = 'pic' + str(num) + '.png'
            elif 'gif' in imgUrl or 'GIF' in imgUrl:
                imgName = 'pic' + str(num) + '.gif'
            elif 'jpeg' in imgUrl or 'JPEG' in imgUrl:
                imgName = 'pic' + str(num) + '.jpeg'
            else:
                continue

            imgSTATIC = up_download_ContentIMG(imgurl=imgUrl, name=imgName, basePath=basePath,
                                           filePath_slug=filePath_slug)
            if imgSTATIC:
                imgHtml = r'''<img src="{}">'''.format(imgSTATIC)
            else:
                continue
        except:
            continue
        infodict['body'] = infodict['body'].replace(str(i), imgHtml)

    if coverGet and infodict['cover']:
        if 'png' in infodict['cover'] or 'PNG' in infodict['cover']:
            coverName = 'cover.png'
        elif 'gif' in infodict['cover'] or 'GIF' in infodict['cover']:
            coverName = 'cover.gif'
        elif 'jpeg' in infodict['cover'] or 'JPEG' in infodict['cover']:
            coverName = 'cover.jpeg'
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
        if imgbrow.status_code > 300:
            return None
    except:
        return None

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

class U1U1WebcrwalMYSQLPipeline():
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
        self.keysList = update_jieba(self.cursor)
        self.three_days_title = get_3days_title()
        aaa = len(self.three_days_title)
        # print('首次：',aaa)
    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        print('进入pipilinke')

        for cutTile in self.three_days_title:
            similarity_index = string_similar(item['title'],cutTile)
            if similarity_index > 0.90:
                # print(item['title'])
                # print(cutTile)
                # print('*****************重复了。',similarity_index)
                return item

        self.three_days_title.append(item['title'])
        # print('过程中：',len(self.three_days_title))


        item = get_static(item)
        keysWord = "ArtUrl,body,cover,created,media_id,publish,slug,summary,title,type,updated,weixinID,staticPath"
        valueWord = '''"{ArtUrl}","{body}","{cover}","{created}","{media_id}","{publish}","{slug}","{summary}","{title}",{type},"{updated}","{weixinID}","{staticPath}"'''

        insert_code = '''INSERT INTO U1LINK_post({}) VALUES ({});'''.format(keysWord, valueWord)

        inser_excut = insert_code.format(
            ArtUrl=pymysql.escape_string(item['ArtUrl']),
            body=pymysql.escape_string(item['body']),
            cover=pymysql.escape_string(item['cover']),
            created=pymysql.escape_string(item['created']),
            media_id=pymysql.escape_string(item['media_id']),
            publish=pymysql.escape_string(item['publish']),
            slug=pymysql.escape_string(item['slug']),
            summary=pymysql.escape_string(item['summary']),
            title=pymysql.escape_string(item['title']),
            type=item['type'],
            updated=pymysql.escape_string(item['updated']),
            weixinID=pymysql.escape_string(item['weixinID']),
            staticPath=pymysql.escape_string(item['staticPath']),
        )
        # self.cursor.execute(inser_excut)
        # self.db.commit()


        print('网站：',item['weixinID'])
        print('爬虫名称：',item['media_id'])
        print('标题：',item['title'])
        print('类别：', item['type'])
        print('链接：',item['ArtUrl'])
        print('正文长度：',len(item['body']))
        if item['cover']:
            print('有标题图')
        else:
            print('无标题图')
        print('文章发布时间：', item['publish'])
        print('文章入库时间：', item['created'])
        print(item['body'])
        print('-----------------------------')
        return item


class U1WebcrwalPipeline(object):
    def process_item(self, item, spider):
        return item
