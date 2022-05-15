import time,os,datetime
# a = datetime.datetime.now()
# print(a)
# b = datetime.datetime.fromtimestamp(time.time())
# print(b)
# exit()

while True:

    print('\n\n开始抓取。开始时间为：{}'.format(datetime.datetime.now()))

    print('开始抓取 采购公告')
    os.system('scrapy crawl 10086')
    print('采购公告 抓取完成')
    print('********************************************************************')
    print('开始抓取 资格预审公告')
    os.system('scrapy crawl 10086_2')
    print('资格预审公告 抓取完成')
    print('********************************************************************')
    print('开始抓取 候选人公示')
    os.system('scrapy crawl 10086_3')
    print('候选人公示 抓取完成')
    print('********************************************************************')
    print('开始抓取 中选结果公示')
    os.system('scrapy crawl 10086_4')
    print('中选结果公示 抓取完成')
    print('********************************************************************')
    print('开始抓取 单一来源公告')
    os.system('scrapy crawl 10086_5')
    print('单一来源公告 抓取完成')

    print('\n\n抓取结束。结束时间为：{}'.format(datetime.datetime.now()))


    # os.system('scrapy crawl artcraw --nolog')
    time.sleep(1200*2.5)