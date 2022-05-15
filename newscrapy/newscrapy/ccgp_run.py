import time,os

while True:
    time.sleep(3600*2)
    os.system('scrapy crawl ccgp -s LOG_FILE=/home/terry/jxpython/logALL/ccgp_sort.log')