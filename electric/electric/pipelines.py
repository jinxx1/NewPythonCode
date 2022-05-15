import json
import requests,re,pprint
from bs4 import BeautifulSoup
from crawltools import save_api

class ElectricPipeline:
    def process_item(self, item, spider):
        print('未走save api前的url',item['url'])
        a = save_api(item)# 将数据录入save api
        item['content'] = len(item['content'])# 已经跑完 save api 把正文转换成字符串长度
        print('以下是进入save api的完整数据格式。')
        pprint.pprint(item)
        print('以下是save api的返回信息')
        print(a)
        print('------------------------分隔符---------------------------------')
        return item