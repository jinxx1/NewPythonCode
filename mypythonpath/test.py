# -*- coding: utf-8 -*-


import sys, re, os, json, pprint, chardet, cchardet, time, datetime, lxml, requests
from urllib import parse as urlpase
from bs4 import BeautifulSoup
import platform

sys_code = platform.system()
if sys_code == 'Windows':
    sys.path.append(r"D:\PythonCode\mypythonpath")
from mkdir import mkdir
from redisBloomHash import bl, bh
from getmysqlInfo import jsonInfo
from crawltools import *
from reqSession import *
from uxue_orm import *

my_Session = mysql_orm()

while True:
    exc = '''SELECT id,download_url FROM ztbInfoAttachment WHERE download_url like "%javascript%encodeURI%" limit 1000'''
    aa = my_Session.session.execute(exc)
    # if len([x for x in aa]) == 0:
    #     break
    # print(len([x for x in aa]))
    llist = []
    for i in aa:
        ddict = {}
        attch_id = i[0]
        attch_url = i[1]
        try:
            attch_newurl = re.findall("encodeURI\(\'(.*?)&fileName", attch_url)[0]
        except Exception as ff:
            print(i)
            print(ff)
            print('```````````````````````````````')
            continue

        ddict['id'] = attch_id
        ddict['download_url'] = attch_newurl
        llist.append(ddict)
    print(len(llist))
    if len(llist)==0:
        break
    my_Session.session.bulk_update_mappings(ZtbInfoAttaChment, llist)
    print('-------------------------------------')
    time.sleep(3)
