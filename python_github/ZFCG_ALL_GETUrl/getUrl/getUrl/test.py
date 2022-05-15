# -*- coding: utf-8 -*-
import requests

url = 'http://httpbin.org/get'
brow = requests.get(url=url)
print(brow.text)