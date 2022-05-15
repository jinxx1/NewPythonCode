# coding: utf-8
import requests
import json
import os, sys
import datetime, time

'''
https://www.jsdati.com/
联众打码平台
    brow = main(api_username='uservice',
         api_password='Xey123456!@#$%^',
         file_name=pathfile,
         api_post_url="http://v1-http-api.jsdama.com/api.php?mod=php&act=upload",
         yzm_min='4',
         yzm_max='4',
         yzm_type='1105',
         tools_token='')

'''

Api_username = 'uservice'
Api_password = 'Xey123456!@#$%^'
Api_post_url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"


def img_main(file_name, yzm_min, yzm_max, yzm_type, tools_token,savePath):

    '''
            main() 参数介绍
            api_username    （API账号）             --必须提供
            api_password    （API账号密码）         --必须提供
            file_name       （需要识别的图片路径）   --必须提供
            api_post_url    （API接口地址）         --必须提供
            yzm_min         （识别结果最小长度值）        --可空提供
            yzm_max         （识别结果最大长度值）        --可空提供
            yzm_type        （识别类型）          --可空提供
            tools_token     （V1软件Token）     --可空提供
    '''
    # api_username =
    # api_password =
    # file_name = 'c:/temp/lianzhong_vcode.png'
    # api_post_url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"
    # yzm_min = '1'
    # yzm_max = '8'
    # yzm_type = '1303'
    # tools_token = api_username
    # proxies = {'http': 'http://127.0.0.1:8888'}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
        # 'Content-Type': 'multipart/form-data; boundary=---------------------------227973204131376',
        'Connection': 'keep-alive',
        'Host': 'v1-http-api.jsdama.com',
        'Upgrade-Insecure-Requests': '1'
    }
    files = {
        'upload': (file_name, open(file_name, 'rb'), 'image/png')
    }

    data = {
        'user_name': Api_username,
        'user_pw': Api_password,
        'yzm_minlen': yzm_min,
        'yzm_maxlen': yzm_max,
        'yzmtype_mark': yzm_type,
        'zztool_token': tools_token
    }
    s = requests.session()
    # r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False, proxies=proxies)
    r = s.post(Api_post_url, headers=headers, data=data, files=files, verify=False)

    txtfile = savePath + "result.txt"
    with open(txtfile, 'w', encoding='utf-8') as ff:
        ff.write(r.text)
        ff.flush()

    return r.text


def download_vcode(imgurl = '', cookies_jar=None, headers=None,savePath = ''):
    timestr = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    if not imgurl or not savePath:
        print('必须加入imgurl和savePath')
        return None

    if not headers:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    isExists = os.path.exists(savePath)
    if not isExists:
        os.makedirs(savePath)
    imgsplit = imgurl.split('.')[-1]
    if imgsplit.lower() == 'jpg':
        imgfile = savePath + "donwload_{}.jpg".format(timestr)
    elif imgsplit.lower() == 'png':
        imgfile = savePath + "donwload_{}.png".format(timestr)
    elif imgsplit.lower() == 'gif':
        imgfile = savePath + "donwload_{}.gif".format(timestr)
    else:
        imgfile = savePath + "donwload_{}.png".format(timestr)
    try:
        s = requests.session()
        if cookies_jar:
            resp = s.get(imgurl, headers=headers, verify=False, cookies=cookies_jar)
        else:
            resp = s.get(imgurl, headers=headers, verify=False)
        with open(imgfile, 'wb') as f:
            f.write(resp.content)
        return imgfile.replace('\\', '/')
    except Exception as e:
        return None


if __name__ == '__main__':


    # exit()

    timestr = time.strftime("%Y%m%d_%H%M%S", time.localtime())

    pathabs = os.path.abspath('.')
    if 'spiders' in pathabs:
        pathabs = os.path.abspath('..')
    print(pathabs)

    savePath = pathabs.replace('\\', '/') + "/lianzhong_shibie/{}/".format(timestr)
    print(savePath)
    imgsrc = 'http://www.ccgp-fujian.gov.cn/noticeverifycode/?1'
    imgPath = download_vcode(imgurl=imgsrc,savePath=savePath)