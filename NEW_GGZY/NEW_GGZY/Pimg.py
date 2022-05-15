# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFont
import pandas as pd
import numpy as np
import requests,os,sys,json
from lxml import html
import re,difflib

from bs4 import BeautifulSoup
import lxml.html
etree = lxml.html.etree


line = '----------------------------------------------------'

def imgDF(imglocalPath):

    im = Image.open(imglocalPath)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    pix = im.load()
    wi, hi = im.size
    col = ['w_' + str(x) for x in range(wi)]
    row = ['h_' + str(x) for x in range(hi)]

    arr = []
    for h in range(hi):
        colarr = []
        for w in range(wi):
            rgb = pix[w, h]
            colarr.append(rgb)
        arr.append(colarr)
    df = pd.DataFrame(arr, columns=col, index=row)

    return df

def getMaxRGB(df):
    maxRGB = {}
    bb = False
    for ii in df.columns:
        a1 = df.groupby(by=[ii],as_index=False)[ii].agg({'cnt':'count'})
        for i in range(len(a1)):
            ddict = {}
            ddict['value'] = a1.loc[i][0]
            ddict['cnt'] = a1.loc[i][1]
            cc = pd.DataFrame([ddict['cnt']],index=[ddict['value']],columns=['cnt'])
            if not bb:
                cTemp = cc
                bb = True
            else:
                cTemp = cTemp.add(cc,fill_value = 0)
    rgbGet = cTemp.sort_values(by='cnt',ascending=False).head(2)

    maxRGB['one'] = rgbGet.index[0]
    maxRGB['two'] = rgbGet.index[1]
    return maxRGB

def getNewIMG_DF(df,maxRGB):
    def rgbFunc(arrlike):
        cha = 80
        rr1 = np.abs(arrlike[0] - maxRGB['two'][0]) < cha
        gg1 = np.abs(arrlike[1] - maxRGB['two'][1]) < cha
        bb1 = np.abs(arrlike[2] - maxRGB['two'][2]) < cha
        dup = rr1 and gg1 and bb1
        if arrlike == maxRGB['one']:
            # arrValue = maxRGB['one']
            arrValue = (0,0,0)
        elif dup:
            # arrValue = maxRGB['two']
            arrValue = (255,255,255)
        else:
            # arrValue = maxRGB['one']
            arrValue = (0, 0, 0)
        return arrValue

    bb = False
    for ii in df.columns:
        tempdf = df[ii].apply(rgbFunc)
        if not bb:
            newDF = tempdf
            bb = True
        else:
            newDF = pd.concat([newDF,tempdf],axis=1)
    return newDF

def new_image(newimgDF):
    newimgPage = 'BBBBB.png'
    color = (0,0,0)
    width = len(newimgDF.columns)
    height = len(newimgDF.index)
    new_img = Image.new('RGB',(width,height),color)

    draw = ImageDraw.Draw(new_img)
    for w in range(width):
        for h in range(height):
            xy = (w,h)
            df_col = 'w_' + str(w)
            df_ind = 'h_' + str(h)
            rgb = newimgDF[df_col].loc[df_ind]
            draw.point(xy=xy,fill=rgb)
    new_img.save(newimgPage)
    del new_img
    return newimgPage

def postImg(imgPath):
    df = imgDF(imgPath)
    maxRGB = getMaxRGB(df)
    newimgDF = getNewIMG_DF(df,maxRGB)
    path = new_image(newimgDF)
    return path


def getToken():
    tokenAPI = 'https://aip.baidubce.com/oauth/2.0/token'
    tokendate = {
        'grant_type': 'client_credentials',
        'client_id': 'sLZvQ7sS4WUPIZ9ZzGZeANg4',
        'client_secret': 'iqFPG7e1Hw1MTDImzDjuptcHwdayUzLU'
    }
    brow = requests.post(url=tokenAPI, data=tokendate)
    jsonT = json.loads(brow.text)
    return jsonT['access_token']

def getImgCode(imgPath):
    import base64
    token = '?access_token=' + getToken()
    apiUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic' + token
    # apiUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/webimage' + token
    HEA = {'Content-Type': 'application/x-www-form-urlencoded'}

    with open(imgPath, 'rb') as file:
        im = file.read()
    img = base64.b64encode(im)

    PostDate = {'image': img, 'language_type': 'CHN_ENG'}
    # PostDate = {'image':img}
    # pp = urllib.urlencode(PostDate)
    brow = requests.post(url=apiUrl, headers=HEA, data=PostDate)
    jsonT = json.loads(brow.text)
    return jsonT

def fujianWord(Referer,cooikes,cishu):
    llist = []
    for i in range(cishu):
        llist.append('1')
    cshu = ''.join(llist)

    imgPath = 'http://www.ccgp-fujian.gov.cn/noticeverifycode/?' + cshu
    print('imgPath',imgPath)
    imgHEA = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.ccgp-fujian.gov.cn',
        'Cookie':cooikes,
        'Referer':Referer,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
    }
    imglocalPath = 'AAAAAAAAAAAAA.png'

    brow = requests.get(url=imgPath, headers=imgHEA)
    with open(imglocalPath, 'wb')as file:
        file.write(brow.content)

    pathimg = postImg(imglocalPath)
    retuword = getImgCode(pathimg)
    a1 = retuword['words_result'][0]['words']
    if a1 and len(a1) == 4:
        wword = a1
    else:
        print('识别失败----------' + a1)
        wword = ''
    return wword

if __name__ == '__main__':
    HEA = {
        'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
    }

    href = 'http://www.ccgp-fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/?page=1'
    tempUrl = 'http://www.ccgp-fujian.gov.cn/3500/noticelist/{notlist}/?csrfmiddlewaretoken={token}&zone_code=&zone_name=&croporgan_name=&project_no=&fromtime=&endtime=&gpmethod=&agency_name=&title=&notice_type=&open_type=&verifycode={yzma}'
    
    # yzUrl = tempUrl.format(notlist=notlist, token=csrf, yzma=yzma)

    brow1 = requests.get(url = href,headers=HEA)

    # print(brow1.text)
    coki = brow1.cookies
    html = etree.HTML(brow1.text)

    # html= brow1.text.encode(brow1.encoding, 'ignore')


    result = etree.tostring(html)
    try:
        csrf = html.xpath("//input[@name = 'csrfmiddlewaretoken']/@value")[0]
        print(csrf)
    except:
        print(brow1.text)


    # ContentSoup = BeautifulSoup(html, 'lxml')
    # print(html)

    # a = ContentSoup.find(input)
    # print(a)

    # imglocalPath = 'AAAAAAAAAAAAA.png'
    # postImg(imglocalPath)
    #
    # a = fujianWord()
    # print(a)








