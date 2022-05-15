# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GgzyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    title = scrapy.Field()
    issueTime = scrapy.Field()
    content = scrapy.Field()
    subclass = scrapy.Field()
    attachmentListJson = scrapy.Field()



    pass
