import os,time
while True:
    os.system('scrapy crawl cm')
    os.system('scrapy crawl tower')
    os.system('scrapy crawl ct')
    os.system('python chinaUniconSql2Mongo.py')
    time.sleep(1800)
