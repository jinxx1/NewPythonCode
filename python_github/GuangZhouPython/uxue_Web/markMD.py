#! /usr/bin/python
# -*- coding: utf-8 -*-
from db import *
import re
import os,sys,shutil
import urllib.request
import jieba
import requests,json
from fake_useragent import UserAgent
from config import COOKIES_DATA
import datetime,time,random,csv
from PIL import Image

def ContentImgUpdate(getContent,Num1):
    for i in range(len(getContent)):
        ContentWord = getContent[i]['Content']
        numList = int(getContent[i]['numList'])
        # pathoo = r'/<img src="P'
        # tihuan = ContentWord.replace(pathoo,'/P')
        # print(tihuan)
        # Content_url_update(db, tihuan, Num1, numList)
        Picture_num = '<img src="Picture'
        if Picture_num in ContentWord:
            Picture_TrueUrl = picURL + Picture_num
            ContentTureUrl = ContentWord.replace('Picture',Picture_TrueUrl)
            Content_url_update(db,ContentTureUrl, Num1,numList)


if __name__=="__main__":

    b = wenzhang_infoA(db, zhuanyi=1,shejiMD=0)
    nn = 0
    for xix in b:
        Num1 = xix['artcleNum']
        if nn>1:
            break
        try:
            artcleNumMD = Num1
            getList = get_list(db,Num1)
            titleMD = getList[0]['TitleT']
            categoryMD = getList[0]['categoriesChineseName']
            authorimgMD = getList[0]['authorImg']
            timeCUT = getList[0]['dataTime'].split('-')
            urlMD = "/post/" + timeCUT[0] + "/" + timeCUT[1] + "/" + getList[0]['artcleNum']
            path1 = os.path.split(os.path.realpath(__file__))
            picURL = path1[0] + r'/static/WeiXinGZH/' + getList[0]['wx_hao'] + "/" + artcleNumMD.split('_')[0] + "/" + artcleNumMD + "/"
            getContent = get_content(db,Num1)
            # 把Picture.jpg变成  /xxx/xxxx/xxxx/xxx/Picture.jgp
            ContentImgUpdate(getContent,Num1)
            # 清洗文章筛除文章简介
            for i in getContent:
                partOne = ''
                BadWord1 = r'<img src=' in i['Content']
                BadWord2 = '点击上方' in i['Content']
                BadWord3 = ''
                BadWord = BadWord1 or BadWord2 or BadWord3
                if BadWord:
                    continue
                elif partOne:
                    summaryMD = partOne + i['Content']
                    break
                elif len(i['Content']) < 15:
                    partOne = i['Content']
                    continue
                else:
                    summaryMD = i['Content']
                    break




            # 确定预览图用哪张

            # 筛选预览图
            imgCover = Image.open(getList[0]['articlePreviewImg'])
            imgCover_array = imgCover.load()
            imgCover_X = float(imgCover.size[0])
            imgCover_Y = float(imgCover.size[1])
            Bl_img = imgCover_X/imgCover_Y
            if 1.30 < Bl_img < 1.70:
                articlepreviewimgMD = getList[0]['articlePreviewImg']
            else:
                dirImg = os.listdir(getList[0]['imgPath'])
                for ImgFile in dirImg:
                    if ImgFile != 'index.html' and ImgFile != 'cover.jpg' and 'gif' not in ImgFile:
                        ImgFile = ImgFile.replace('jpg.jpg','jpg').replace('png.png','png')
                        imgFile = Image.open(getList[0]['imgPath'] + ImgFile)
                        imgFile_X = float(imgFile.size[0])
                        imgFile_Y = float(imgFile.size[1])
                        Bl_imgFile = imgFile_X / imgFile_Y
                        if 1.30 < Bl_imgFile < 1.70:
                            articlepreviewimgMD = getList[0]['imgPath'] + ImgFile
                            break
                        elif 1.30 < Bl_imgFile < 1.85:
                            articlepreviewimgMD = getList[0]['imgPath'] + ImgFile
                            break
                        else:
                            articlepreviewimgMD = getList[0]['articlePreviewImg']
                Cover_Img_update(db,articlepreviewimgMD,Num1)

            Tags = get_tags(db,Num1)
            if not Tags:
                Tags_insert(db,'新闻报道',10000,Num1)
                Tags = get_tags(db, Num1)
            tagList = []

            for i in range(len(Tags)):
                if i >3:
                    break
                tagEvery = Tags[i]['tags0']
                tagList.append(tagEvery)

            tagMD0 = 'tag:' + tagList[0]
            tagMD1 = '       ' + tagList[1]
            tagMD2 = '       ' + tagList[2]
            tagMD3 = '       ' + tagList[3]

            H1 = 'title:' + titleMD
            H2 = 'summary:' + summaryMD
            H3 = 'url:' + Num1
            H4 = 'datetime:' + getList[0]['dataTime']
            H5 = 'category:' + categoryMD
            H6 = 'articlepreviewimg:' + articlepreviewimgMD
            H7 = 'authorimg:' + authorimgMD
            tagMD0 = 'tag:' + tagList[0]
            tagMD1 = '       ' + tagList[1]
            tagMD2 = '       ' + tagList[2]
            tagMD3 = '       ' + tagList[3]
            path_MD = './source/_postsBak/' + Num1 + ".md"
            with open(path_MD,'a',encoding='utf-8',newline='') as f:
                f.writelines(H1 + '\n')
                f.writelines(H2 + '\n')
                f.writelines(H3 + '\n')
                f.writelines(H4 + '\n')
                f.writelines(H5 + '\n')
                f.writelines(H6 + '\n')
                f.writelines(H7 + '\n')
                f.writelines(tagMD0 + '\n')
                f.writelines(tagMD1 + '\n')
                f.writelines(tagMD2 + '\n')
                f.writelines(tagMD3 + '\n')
                f.writelines('\n')
                f.writelines('\n')
                f.writelines('\n')
                f.writelines('##' + titleMD)
            shejiMD_retune_1(db,Num1)



            # nn +=1

        except IndexError:
            # print(Num1)
            continue





#
#
# # 改正错误
#     a = get_list(db)
#     for aa in a:
#         artcleNumMD = aa['artcleNum']
#         articlePreviewImg = aa['articlePreviewImg']
#         imgPath = aa['imgPath']
#         authorImg = aa['authorImg']
#         OKword = r'E:/python_github/GuangZhouPython/uxue_Web'
#         BADword = r'E:python_githubGuangZhouPythonuxue_Web'
#         if BADword in articlePreviewImg:
#             tihuan1 = articlePreviewImg.replace(BADword,OKword)
#             cursor = db.cursor()
#             update_content1 = "update weblist set articlePreviewImg = '{}' where artcleNum='{}';".format(tihuan1, artcleNumMD)
#             cursor.execute(update_content1)
#             db.commit()
#             db.rollback()
#
#         if BADword in imgPath:
#             tihuan2 = imgPath.replace(BADword,OKword)
#             cursor = db.cursor()
#             update_content2 = "update weblist set imgPath = '{}' where artcleNum='{}'".format(tihuan2, artcleNumMD)
#             cursor.execute(update_content2)
#             db.commit()
#             db.rollback()
#
#         if BADword in authorImg:
#             tihuan2 = authorImg.replace(BADword, OKword)
#             cursor = db.cursor()
#             update_content2 = "update weblist set authorImg = '{}' where artcleNum='{}'".format(tihuan2, artcleNumMD)
#             cursor.execute(update_content2)
#             db.commit()
#             db.rollback()
#
#     db.close()