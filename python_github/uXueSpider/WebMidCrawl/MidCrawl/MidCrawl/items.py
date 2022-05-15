# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MidcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    SiteNameCha = scrapy.Field()
    SiteUrl = scrapy.Field()
    StartUrl = scrapy.Field()
    artTitle = scrapy.Field()
    artContent = scrapy.Field()
    artUrl = scrapy.Field()
    Xpath_id = scrapy.Field()
    artContentTime = scrapy.Field()
