# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GeturlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site = scrapy.Field()
    domain = scrapy.Field()
    capturedTime = scrapy.Field()
    issueTime = scrapy.Field()
    subclass = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    collName = scrapy.Field()
    from_Page = scrapy.Field()


    ArticleUrl = scrapy.Field()
    Num = scrapy.Field()
    insert_status = scrapy.Field()
    ArticleUrlList = scrapy.Field()
    RequestUrl = scrapy.Field()
    channelCode = scrapy.Field()
    _id = scrapy.Field()
    couchdb_id = scrapy.Field()
    mongoContent_id = scrapy.Field()
    sitewebId = scrapy.Field()
    zaoday = scrapy.Field()
    wanday = scrapy.Field()
    timeTuple = scrapy.Field()
    content = scrapy.Field()
    attachments = scrapy.Field()
    artID = scrapy.Field()









