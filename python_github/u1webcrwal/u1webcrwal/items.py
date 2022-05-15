# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class U1WebcrwalItem(scrapy.Item):


    slug = scrapy.Field()
    type = scrapy.Field()
    media_id = scrapy.Field()
    ArtUrl = scrapy.Field()
    staticPath = scrapy.Field()

    weixinID = scrapy.Field()
    summary = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
    body = scrapy.Field()
    imgCoverYN = scrapy.Field()

    publish = scrapy.Field()
    created = scrapy.Field()
    updated = scrapy.Field()
    timeYmd = scrapy.Field()

    imgCoverYN = scrapy.Field()







    pass
