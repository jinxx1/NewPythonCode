# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuangxiartileItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site = scrapy.Field()
    domain = scrapy.Field()
    capturedTime = scrapy.Field()
    issueTime = scrapy.Field()
    subclass = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    attachments = scrapy.Field()
    _id = scrapy.Field()