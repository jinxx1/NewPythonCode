#! /usr/bin/python
# -*- coding: utf-8 -*-
from db import *
import re
import os,sys,shutil
import urllib.request
import jieba
import requests,json
from fake_useragent import UserAgent
from config import COOKIES_DATA,ROOT
import datetime,time,random,csv

def remark_contentText(a):

    a1 = a[0]['wordT'].replace(u'/>',u'/><br  />').replace(u'<img',u'<br  /><img')
    wordword = a1.split('<br  />')
    NewContent = []
    for str1 in wordword:
        if len(str1)>1:
            pattern = re.findall(u'<br.*/>', str1)
            if pattern:
                str1 = str1.replace(pattern[0],u'')
            NewContent.append(str1.replace('&nbsp;',''))
    path = a[0]['ret_path']
    folder = path.replace('index.html','').replace('wechat_sogou_crawl-master','uxue_Web_wxSpiders')
    folderFile = os.listdir(folder)
    picturePic = []
    for i in folderFile:
        patten = re.findall(u'Picture',i)
        if patten:
            NumP = i.replace(patten[0],u'').split('.')[0]
            picturePic.append(i)
    for nn in range(len(picturePic)):
        x = nn+1

        if str(x) not in picturePic[nn]:
            picturePic.insert(nn,'Picture'+str(x))

    nNum = 0
    NewContentNum = 0
    for ww in NewContent:
        if '<img src=' in ww:
            if picturePic[nNum] not in ww:
                # print(ww)
                # print(folder)
                try:
                    srcUrl = re.findall(u"\<img src=\"(.*?)\?\" \/\>",ww)[0]
                    print(srcUrl)
                    PicName = ''
                    if '_jpg' or '_JPG' or 'jpeg' or 'JPEG' in srcUrl:
                        PicName = picturePic[nNum] + ".jpg"
                        wwT = u'<img src="' + PicName+ u'" />'
                    elif '_png' or '_PNG' in srcUrl:
                        PicName = picturePic[nNum] + ".png"
                        wwT = u'<img src="' + PicName+ u'" />'
                    elif '_gif' or '_GIF' in srcUrl:
                        PicName = picturePic[nNum] + ".gif"
                        wwT = u'<img src="' + PicName+ u'" />'
                    else:
                        wwT = ''
                    urllib.request.urlretrieve(srcUrl, folder + '{}'.format(PicName))
                except:
                    wwT = ''

                NewContent[NewContentNum] = wwT
            nNum +=1
        NewContentNum+=1

    return NewContent

def title_jieba(db,Num):
    listJieba = []
    b = wenzhang_info(db,Num)
    ua = UserAgent()
    headers = {'user-agent':ua.random}
    f = COOKIES_DATA
    cookies = {}
    for line in f.split(';'):
        name,value = line.strip().split('=',1)
        cookies[name] = value
    for i in b:
        jjba = jieba.lcut(i['title'])

        for wordjieba in jjba:
            if len(wordjieba) > 1:

                dict = {
                    # wordjieba:genera[0]['all']['avg']
                    wordjieba: 0
                }
                listJieba.append(dict)

            #
            # if len(wordjieba)>1:
            #     url = 'http://index.baidu.com/api/SearchApi/index?'
            #     dataword = {
            #         'word':wordjieba,
            #         'area':'0',
            #         'days':'30'
            #     }
            #     secSlepp = random.randint(1,5)
            #     time.sleep(secSlepp)
            #     redu = requests.post(url=url,data=dataword,headers=headers,cookies=cookies).text
            #     jsonT = json.loads(redu)
            #     try:
            #         genera = jsonT['data']['generalRatio']
            #     except TypeError:
            #         continue
            #
            #     if int(genera[0]['all']['avg'])>100:
            #         dict={
            #             # wordjieba:genera[0]['all']['avg']
            #         }
            #         listJieba.append(dict)
    return listJieba


def get_mysql_Content(Num):
    resuList = from_mysql_inputArtcleNum_get_content(Num)
    pprint.pprint(resuList)
    ContentList = []
    imgword = Num + "/" + "Picture1"
    ContentWeb = ''
    for i in range(len(resuList)):
        ContentList.append(resuList[i]['Content'])
    for everyContent in ContentList:
        if Num in everyContent:
            CutContent = everyContent.split('static')
            Badword = r'/<img src="Picture'

            if Badword in CutContent[1]:
                aa = CutContent[1].replace(Badword,r"/Picture")
                turContentIMG =r'<img src="' +ROOT + 'static' + aa
                ContentWeb =ContentWeb + turContentIMG.replace('jpg.jpg','jpg').replace('gif.gif','gif')

        else:
            TrueContent = '<p>' + everyContent + '</p>'
            ContentWeb =ContentWeb + TrueContent
    return ContentWeb








if __name__ == "__main__":






    WEB_DATE = {
        'Title':'',
        'acticleNum':'',
        'wx_hao':'',
        'categoriesChineseName':'',
        'tags':'',
        'imgPath':'',
        'Content':'',
        'dataTime':'',
        'articlePreviewImg':'',
        'authorImg':''
    }

    b = wenzhang_infoA(db,zhuanyi=0,shejiMD=0)

    for xix in b:
        WEB_DATE['Title'] = xix['title']
        ttime = xix['date_time']
        WEB_DATE['dataTime'] = str(ttime.date())
        ARTICLENUM = xix['artcleNum']

        WEB_DATE['acticleNum'] = ARTICLENUM
        mp_id = xix['mp_id']
        mpinfo = mp_info(db, mp_id)[0]
        WEB_DATE['wx_hao'] = mpinfo['wx_hao']
        WEB_DATE['categoriesChineseName'] = mpinfo['name']
        path1 = os.path.split(os.path.realpath(__file__))
        pppath = r'/static/images'
        authorImg = path1[0] + pppath + '/' + mpinfo['wx_hao'] + ".jpg"
        WEB_DATE['authorImg'] = authorImg.replace(r'\\','/')
        localIndexList = local_index_list(db,ARTICLENUM)
        WEB_DATE['Content'] = remark_contentText(localIndexList)
        pathYuanLai = localIndexList[0]['ret_path'].replace('index.html','').replace('wechat_sogou_crawl-master','uxue_Web_wxSpiders')
        path = localIndexList[0]['ret_path'].split('WeiXinGZH')
        webContentFold = path1[0] + "/quiet/static/" + 'WeiXinGZH' + path[1].replace('index.html', '')
        try:
            os.makedirs(webContentFold)
        except FileExistsError:
            print('got it')
            continue
        dir1 = os.listdir(pathYuanLai)
        for i in dir1:
            YuanlaiFile = pathYuanLai + i
            NewFile = webContentFold + i
            shutil.copyfile(YuanlaiFile,NewFile)
            zhuanyi_retune_1(db,ARTICLENUM)
            try:
                os.rmdir(pathYuanLai)
            except:
                pass
            if 'cover' in NewFile:
                WEB_DATE['articlePreviewImg'] = NewFile.replace(r'\\','/')
        WEB_DATE['imgPath'] = webContentFold.replace(r'\\','/')
        try:
            WEB_DATE['tags'] = title_jieba(db, ARTICLENUM)
        except:
            WEB_DATE['tags'] =  [{'新闻报道': 100000}]

        wxinfo_info_mysql(db,WEB_DATE)
        Content_into_mysql(db,WEB_DATE)
        tags_into_mysql(db,WEB_DATE)

        pprint.pprint(WEB_DATE)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


    print('----------------------THE END----------------------')









    db.close()

