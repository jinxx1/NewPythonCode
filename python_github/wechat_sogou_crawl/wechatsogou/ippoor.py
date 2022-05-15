# -*- coding: utf-8 -*-
import requests

def ipPool():
    ipPool = requests.get(url='http://localhost:8091/random').text
    proxies = {'http': ipPool}
    # proxies = ipPool
    return proxies

a = requests.get(url='https://www.baidu.com/',proxies=ipPool())
a = requests.get(url='https://www.baidu.com/')
print(ua.text.encode('utf-8').decode('utf-8'))