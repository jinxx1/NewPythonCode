# -*- coding: utf-8 -*-
import requests
import json
import pprint
from bs4 import BeautifulSoup
HEA = {
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8',
'Connection':'keep-alive',
'Content-Length':'228',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Host':'www.cebpubservice.com',
'Origin':'http://www.cebpubservice.com',
'Referer':'http://www.cebpubservice.com/ctpsp_iiss/searchbusinesstypebeforedooraction/getSearch.do?tabledivIds=searchTabLi2',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',
}
data = {
'businessType': '招标公告',

'row': '10000',
'searchName': '',
'searchArea': '',
'searchIndustry': '',
'centerPlat': '',
'searchTimeStart': '',
'searchTimeStop': '',
'timeTypeParam': '',
'bulletinIssnTime': '',
'bulletinIssnTimeStart': '',
'bulletinIssnTimeStop': '',

}
url = "http://www.cebpubservice.com/ctpsp_iiss/searchbusinesstypebeforedooraction/getStringMethod.do"


def ip_proxy():
    apiurl = "http://dps.kdlapi.com/api/getdps/?orderid=901233217497055&num=10&pt=1&format=json&sep=1"
    apiget = requests.get(url=apiurl)
    infoall = json.loads(apiget.text)
    ipList = infoall['data']['proxy_list']
    ip_dict_list = []
    for n in ipList:
        ddict = {}
        ddict['http'] = n
        ip_dict_list.append(ddict)
    return ip_dict_list




    # {"msg": "","code": 0,"data": {"count": 6,
    #         "proxy_list": [
    #             "183.166.132.192:22356",
    #             "117.65.127.22:20569",
    #             "120.15.18.30:16740",
    #             "110.89.122.17:15752",
    #             "27.159.165.69:20145",
    #             "115.226.157.69:16815"]}}

for numPage in range(1,38):
    data['pageNo'] = str(numPage)
    # ip_list = ip_proxy()
    aa = 'http://101.26.196.109:18462'
    ipproxy = {'http': aa, 'https': aa}
    brow = requests.post(url, headers=HEA, data=data,proxies=ipproxy)
    if '您的IP地址在短时间内频繁访问该页面导致' in brow.text:
        print('ip地址被封')
        break
    if brow.status_code != 200:
        print(brow.status_code)
    jsonT = json.loads(brow.text)

    title = 'cepubList_{}.json'.format(str(numPage))
    with open(title,'w',encoding='utf-8') as jf:
        json.dump(jsonT, jf,ensure_ascii=False)
    break
