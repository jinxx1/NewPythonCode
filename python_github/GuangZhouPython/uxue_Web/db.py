#! /usr/bin/python
# -*- coding: utf-8 -*-
import pprint
import datetime
import pymysql
from config import DB_MYSQL


db = DB_MYSQL



def local_index_list(db,artcleNum=False,zhuanyi=False):#从文章编号获取文章正文信息
    cursor = db.cursor()
    if artcleNum and zhuanyi:
        search_date = "SELECT * FROM local_index_list WHERE artcleNum='{}' and zhuanyi='{}';".format(artcleNum,zhuanyi)
    elif zhuanyi:
        search_date = "SELECT * FROM local_index_list WHERE zhuanyi='{}';".format(zhuanyi)
    elif artcleNum:
        search_date = "SELECT * FROM local_index_list WHERE artcleNum='{}';".format(artcleNum)
    else:
        search_date = "SELECT * FROM local_index_list"


    cursor.execute(search_date)
    resultes = cursor.fetchall()

    return resultes

def wenzhang_infoA(db,zhuanyi=0,shejiMD=0):#从文章编号获取文章所有信息
    cursor = db.cursor()
    search_date = "SELECT * FROM wenzhang_info WHERE zhuanyi={} and shejiMD={};".format(zhuanyi,shejiMD)

    cursor.execute(search_date)
    resultes = cursor.fetchall()
    return resultes
    # if artcleNum and zhuanyi:
    #     search_date = "SELECT * FROM wenzhang_info WHERE artcleNum='{}' and zhuanyi='{}'".format(artcleNum,zhuanyi)
    # elif zhuanyi:
    #     search_date = "SELECT * FROM wenzhang_info WHERE zhuanyi='{}'".format(zhuanyi)
    # elif artcleNum:
    #     search_date = "SELECT * FROM wenzhang_info WHERE artcleNum='{}'".format(artcleNum)
    # else:
    #     search_date = "SELECT * FROM wenzhang_info WHERE zhuanyi={}".format(0)

def wenzhang_info(db, artcleNum):  # 从文章编号获取文章所有信息
    cursor = db.cursor()
    search_date = "SELECT * FROM wenzhang_info WHERE artcleNum='{}';".format(artcleNum)

    cursor.execute(search_date)
    resultes = cursor.fetchall()
    return resultes

def mp_info(db,id=False):
    cursor = db.cursor()
    if id:
        search_date = "SELECT * FROM mp_info WHERE _id='{}';".format(id)
    else:
        search_date = "SELECT * FROM mp_info"
    cursor.execute(search_date)
    resultes = cursor.fetchall()
    return resultes

def zhuanyi_retune_1(db,articlNum):
    cursor = db.cursor()
    name = [
        'local_index_list',
        'wenzhang_info'
    ]
    for n in name:
        update_zhuanyi = "update {} set zhuanyi = 1 where artcleNum='{}';".format(n,articlNum)
        cursor.execute(update_zhuanyi)
        db.commit()
        db.rollback()

    return ("update_zhuanyi OK")


def shejiMD_retune_1(db,articlNum):
    cursor = db.cursor()
    update_zhuanyi = "update wenzhang_info set shejiMD = 1 where artcleNum='{}';".format(articlNum)
    cursor.execute(update_zhuanyi)
    db.commit()
    db.rollback()

    return ("update_zhuanyi OK")



def Content_url_update(db,ContentTureUrl,artcleNumMD,numList):
    cursor = db.cursor()
    update_content = "update webcontent set Content = '{}' where artcleNum='{}' and numList={};".format(ContentTureUrl,artcleNumMD,numList)
    cursor.execute(update_content)
    db.commit()
    db.rollback()
    return ("update_zhuanyi OK")

def Cover_Img_update(db,Imgpath,artcleNumMD):
    cursor = db.cursor()
    update_content = "update weblist set articlePreviewImg = '{}' where artcleNum='{}';".format(Imgpath,artcleNumMD)
    cursor.execute(update_content)
    db.commit()
    db.rollback()
    return ("update_zhuanyi OK")

def Tags_insert(db,tags,tagsValue,artcleNumMD):
    cursor = db.cursor()
    inserValue = "INSERT INTO webtags (tags0,tags0Vaule,artcleNum) VALUES ('{}',{},'{}');".format(tags,tagsValue,artcleNumMD)
    cursor.execute(inserValue)
    db.commit()
    db.rollback()
    return ("update_zhuanyi OK")





def tags_into_mysql(db,webDict):
    cursor = db.cursor()
    titleT = webDict['Title']

    acticleNum = webDict['acticleNum']
    for i in webDict['tags']:
        a = list(i.keys())[0]
        b = i[a]

        inserValue = "INSERT INTO webtags (tags0,tags0Vaule,artcleNum,INTOMYSQLTIME) VALUES ('{}',{},'{}','{}');".format(a,b,acticleNum,datetime.datetime.now())
        cursor.execute(inserValue)
        db.commit()
        db.rollback()


def Content_into_mysql(db,webDict):
    cursor = db.cursor()
    titleT = webDict['Content']
    acticleNum = webDict['acticleNum']
    numList = 0
    for i in webDict['Content']:
        inserValue = "INSERT INTO webcontent (Content,numList,artcleNum,intomysqlTIME) VALUES ('{}',{},'{}','{}');".format(i,numList,acticleNum,datetime.datetime.now())
        cursor.execute(inserValue)
        db.commit()
        db.rollback()

        numList+=1

def wxinfo_info_mysql(db,webDict):
    cursor = db.cursor()

    inserValue = "INSERT INTO weblist (TitleT,artcleNum,wx_hao,categoriesChineseName,imgPath,dataTime,articlePreviewImg,authorImg,INTOMYSQLTIME)" \
                                " VALUES ('{TitleT}','{artcleNum}','{wx_hao}','{categoriesChineseName}','{imgPath}','{dataTime}','{articlePreviewImg}','{authorImg}','{INTOMYSQLTIME}');"


    excut = inserValue.format(
        TitleT = webDict['Title'],
        artcleNum = webDict['acticleNum'],
        wx_hao = webDict['wx_hao'],
        categoriesChineseName = webDict['categoriesChineseName'],
        imgPath = webDict['imgPath'],
        dataTime = webDict['dataTime'],
        articlePreviewImg = webDict['articlePreviewImg'],
        authorImg = webDict['authorImg'],
        INTOMYSQLTIME = datetime.datetime.now()
    )
    cursor.execute(excut)
    db.commit()
    db.rollback()

def get_content(db,artcleNum):
    cursor = db.cursor()
    Sdate = " select * from webcontent where artcleNum='{}';".format(artcleNum)
    cursor.execute(Sdate)
    resultes = cursor.fetchall()
    return resultes


def from_mysql_inputArtcleNum_get_content(artcleNum):
    cursor = db.cursor()
    Sdate = " select * from webcontent where artcleNum='{}';".format(artcleNum)
    cursor.execute(Sdate)
    resultes = cursor.fetchall()
    return resultes


def get_list(db, artcleNum=False):
    cursor = db.cursor()
    if artcleNum:
        Sdate = " select * from weblist where artcleNum='{}';".format(artcleNum)
    else:
        Sdate = " select * from weblist "
    cursor.execute(Sdate)
    resultes = cursor.fetchall()
    return resultes

def get_tags(db, artcleNum):
    cursor = db.cursor()
    Sdate = " select * from webtags where artcleNum='{}';".format(artcleNum)
    cursor.execute(Sdate)
    resultes = cursor.fetchall()
    return resultes



def into_TOP5_MYSQL(dict):
    cursor = db.cursor()
    insertTime = datetime.datetime.now()
    articleNum = dict['articleNum']




    inserValue = '''INSERT INTO top5 (insertTime,siteLocal,articleNum,PicLocal,articleLink,summy,titleT) VALUES ('{insertTime}','{siteLocal}','{articleNum}','{PicLocal}','{articleLink}','{summy}','{titleT}');'''

    format_inserValue = inserValue.format(
    insertTime = insertTime,
    siteLocal = dict['siteLocal'],
    articleNum = articleNum,
    PicLocal = dict['PicLocal'],
    articleLink = dict['articleLink'],
    summy=dict['summy'],
    titleT=dict['titleT']
    )

    cursor.execute(format_inserValue)
    db.commit()
    db.rollback()



def get_top5_dict():
    cursor = db.cursor()

    wordList = ['topleft','topright','downleft','downmidd','downright']
    showDict = {}
    for wordTag in wordList:
        wordEcut = "select * from top5 where siteLocal='{}' order by insertTime DESC limit 1;".format(wordTag)
        cursor.execute(wordEcut)
        resultes = cursor.fetchall()[0]
        imgTemp = resultes['PicLocal'].split('static')
        imgTrue = 'static' + imgTemp[1]

        showDict[wordTag + '_PicLocal'] =imgTrue
        showDict[wordTag + '_articleLink'] = resultes['articleLink']
        showDict[wordTag + '_titleT'] = resultes['titleT']
        showDict[wordTag + '_summy'] = resultes['summy']

    return showDict








if __name__=="__main__":


    pprint.pprint(get_top5_dict())




