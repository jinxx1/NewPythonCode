# -*- coding: utf-8 -*-

# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from spalsh10086.scrapyParse import *
import pprint,json
from spalsh10086.mysql_processing import *


def attchment_get(HTMLcontent):
    soup = BeautifulSoup(HTMLcontent, 'lxml')
    hrefall = soup.find_all(href=re.compile("commonDownload\.html\?attId"))
    attchment = []
    for nn in hrefall:
        ddict = {}
        download_url = nn.get('href')
        ddict['download_url'] = "https://b2b.10086.cn" + download_url
        ddict['name'] = nn.get_text()
        attchment.append(ddict)
    return attchment

class Spalsh10086Pipeline(object):
    def process_item(self, item, spider):
        try:
            get_pageNum = item['get_pageNum']
            del item['get_pageNum']
        except Exception as e:
            get_pageNum = e

        attachmentListJsonList = []
        attachmentListJsonList = attchment_get(item['content'])
        if attachmentListJsonList:
            item['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)

        a = save_api(item)
        item['content'] = len(item['content'])
        item['get_pageNum'] = get_pageNum
        pprint.pprint(item)

        print(a)
        print('------------------------')
        update_stats(item['itemID'])
        return item
