# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilucrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    cat = scrapy.Field()
    url = scrapy.Field()
    pageNum = scrapy.Field()
    formLink = scrapy.Field()
    videoInfo = scrapy.Field()
    imgUrl = scrapy.Field()
