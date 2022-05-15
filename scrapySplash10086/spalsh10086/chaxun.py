
# -*- coding: utf-8 -*-
import json,pprint
from getmysqlInfo import jsonInfo
from mkdir import mkdir
from redisBloomHash import bl

from crawltools import *
from requests_obj import *
from uxue_orm import *


resultroot = r"C:\Users\jinxx1\Desktop\20220216.json"
with open(resultroot,'r',encoding='utf-8') as ff:

	jsonT= json.load(ff)

llist = []
for i in jsonT['RECORDS']:
	if i['page_url'] in llist or '&ux_' not in i['page_url']:
		continue
	else:
		llist.append(i['page_url'])


pprint.pprint(llist)
print(len(llist))

