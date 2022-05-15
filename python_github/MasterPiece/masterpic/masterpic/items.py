# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MasterpicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    PicTitle = scrapy.Field()
    PicFullTitle = scrapy.Field()
    PicFullUrl = scrapy.Field()
    description = scrapy.Field()
    iconImg = scrapy.Field()
    PicUrl = scrapy.Field()
    MasterName = scrapy.Field()
    MasterNameUrl = scrapy.Field()
    letterNameListPageUrl = scrapy.Field()
    letter = scrapy.Field()
    PicLocalPath = scrapy.Field()
    iconImgLocalPath = scrapy.Field()
    _id = scrapy.Field()
    collName = scrapy.Field()
    PicSize = scrapy.Field()
    referer = scrapy.Field()
