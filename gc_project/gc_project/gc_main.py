# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/26
import os, time, datetime

command_list = [
#    'scrapy crawl gc_clcg >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_dlzb >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_gdjd >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_gzdz >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_gept >/home/gzcez/w_code/log/gc.log 2>&1 &',
    'scrapy crawl gc_mh >/home/gzcez/w_code/log/gc.log 2>&1 &',
    # 'scrapy crawl minhang >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_nfdw >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_szyg >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_szzf >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_tl >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_yc >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_ztx >/home/gzcez/w_code/log/gc.log 2>&1 &',
#    'scrapy crawl gc_zfcg >/home/gzcez/w_code/log/gc.log 2>&1 &',
]

while True:
    for command in command_list:
        start_stamp = time.time()
        start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_stamp))
        os.system(command)
        end_stamp = time.time()
        end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_stamp))
        duration_stamp = end_stamp - start_stamp
        duration = datetime.timedelta(seconds=duration_stamp)
        print(
            'The {} had running\n   starTime is {}\n    endTime is {}\n   duration is {}'.format(command, start, end,
                                                                                                 duration))
        print('----------------------------------')
    time.sleep(1800)