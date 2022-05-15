# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Spalsh10086Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    issueTime = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    subclass = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    get_pageNum = scrapy.Field()
    pass
