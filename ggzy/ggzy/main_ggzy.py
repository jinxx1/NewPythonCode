# -*- coding: utf-8 -*-
import os,time,datetime
crawlNamePath = 'crawlNamePath.txt'
while True:
    with open(crawlNamePath) as f:
        str = f.read()
    crawlList = [i for i in str.split('\n')]

    for crawlName in crawlList:
        # start_stamp = time.time()
        # start = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start_stamp))
        excWord = '''nohup scrapy crawl {} -a goon="no" >/dev/null 2>&1 &'''.format(crawlName)
        os.system(excWord)
        # end_stamp = time.time()
        # end = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(end_stamp))
        # duration_stamp = end_stamp - start_stamp
        # duration = datetime.timedelta(seconds=duration_stamp)
    time.sleep(3600)