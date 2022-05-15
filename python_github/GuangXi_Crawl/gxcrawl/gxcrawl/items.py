# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GxcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ContentUrl = scrapy.Field()
    code = scrapy.Field()
    allpageNum = scrapy.Field()
    bei_10 = scrapy.Field()
    yu_10 = scrapy.Field()
    Num = scrapy.Field()
    arrange = scrapy.Field()
    insert = scrapy.Field()
    nowMaxNum = scrapy.Field()
    nowMinNum = scrapy.Field()
    ContentUrlList = scrapy.Field()

    site = scrapy.Field()
    domain = scrapy.Field()
    capturedTime = scrapy.Field()
    issueTime = scrapy.Field()
    subclass = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    attachments = scrapy.Field()



