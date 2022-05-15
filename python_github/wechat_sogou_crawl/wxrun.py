# -*- coding: utf-8 -*-
import time,datetime
import os

while True:
    nowtime = str(datetime.datetime.now().time().replace(microsecond=0)).replace(':', '')
    timeweek = datetime.datetime.now().isoweekday()
    if timeweek < 6 and 80000 < int(nowtime) < 2000000:
        os.system('python2 updatemp.py')
        time.sleep(3000)
    else:
        time.sleep(3600)
