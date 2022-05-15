import time,os

while True:
    os.system('scrapy crawl gcable_guangdong -s LOG_FILE=/home/terry/jxpython/logALL/gcable_guangdong.log')
    time.sleep(7200)