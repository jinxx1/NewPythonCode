# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy




class NewscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pageNum = scrapy.Field()
    contentNum = scrapy.Field()


    site = scrapy.Field()
    title = scrapy.Field()
    issueTime = scrapy.Field()
    subclass = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    attachmentListJson = scrapy.Field()

    msg = scrapy.Field()
    errortime = scrapy.Field()

    # attachmentListJson说明
    # ddict = {}
    # ddict['downloadUrl'] = 'xxx'
    # ddict['name'] = 'name'
    # llist = [ddict,ddict,ddict,ddict]
    # item['attachmentListJson'] = json.dumps(llist, ensure_ascii=False)








    pass
