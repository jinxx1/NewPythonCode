# -*- coding: utf-8 -*-

import telnetlib
import requests
from bs4 import BeautifulSoup
import time
import pprint,json



xicidaili_list = ['https://www.xicidaili.com/nn',
                'https://www.xicidaili.com/wt',
                'https://www.xicidaili.com/wn',
                'https://www.xicidaili.com/nt',
                'https://www.xicidaili.com/qq']

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
socket_timeout = 3
checkIPurl = "http://www.ccgp-jiangxi.gov.cn/web/"

def checkIP_baidu(ip,port,protcol):
    iproxystr = protcol + "://" + ip + ":" + port
    iproxy = {
        protcol : iproxystr
    }
    try:
        brow = requests.get(url=checkIPurl,proxies = iproxy,timeout = 3)
        if brow.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def checkIP_telnet(ip,port,protcol):
    iproxystr = protcol + "://" + ip

    try:
        telnetlib.Telnet(ip,port=port,timeout=3)
    except:
        return False
    else:
        return True

def get_real_pip(llist = xicidaili_list):
    for num,url in enumerate(llist):
        brow = requests.get(url=url,headers = {'User-agent':user_agent})
        soup = BeautifulSoup(brow.text,'lxml')

        alltable = soup.find(attrs={'id':'ip_list'})
        alltr = alltable.find_all('tr')

        for tr in alltr:
            ddict = {}
            tdw = tr.find_all('td')
            try:
                ddict['ip'] = tdw[1].string
                ddict['port'] = tdw[2].string
                ddict['protcol'] = tdw[5].string.lower()
            except:
                continue

            ipchenkcode = checkIP_telnet(ip=ddict['ip'],port=ddict['port'],protcol=ddict['protcol'])
            # print(ipchenkcode)
            # print(ddict)
            # print('---------------------')
            if ipchenkcode:
                ipchenkcode_baidu = checkIP_baidu(ip=ddict['ip'],port=ddict['port'],protcol=ddict['protcol'])
                if ipchenkcode_baidu:
                    yield ddict
            else:
                continue
def proxy_ip():
    for ipdict in get_real_pip():
        iproxystr = ipdict['protcol'] + "://" + ipdict['ip'] + ":" + ipdict['port']
        iproxy = {
            ipdict['protcol']: iproxystr
        }
        return iproxy


if __name__ == '__main__':
    import json
    url = "http://localhost:5010/wxAPI/"
    posturl = "https://mp.weixin.qq.com/s/itMq7HV_TcahdDM-J72Uug"
    postdate = {'url':posturl}

    brow = requests.post(url=url,data=postdate)
    print(brow.text)


    exit()

    url = "http://www.ccgp-jiangxi.gov.cn/web/jyxx/002006/002006001/20200506/d3207e2c-7ad5-42f9-83f2-ceea4043f4bb.html"
    rowxy = {'https': 'https://124.112.105.99:4216'}

    brow = requests.get(url,proxies = rowxy)
    print(brow.text)
    print(brow.status_code)

