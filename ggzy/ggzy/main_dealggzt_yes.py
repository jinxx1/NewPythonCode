# -*- coding: utf-8 -*-
import os,time
for i in range(1000):
    excWord = '''nohup scrapy crawl dealggzy -a goon="yes" >/dev/null 2>&1 &'''
    os.system(excWord)
    time.sleep(600)