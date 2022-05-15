# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CiccrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()#文章来源 如新华网 人民日报
    programa_dictionaries = scrapy.Field()
    subtopic_dictionaries = scrapy.Field()
    summary = scrapy.Field()
    body = scrapy.Field()
    cover = scrapy.Field()
    person = scrapy.Field()
    publishTime = scrapy.Field()
    created = scrapy.Field()
    updated = scrapy.Field()
    url = scrapy.Field()
    online = scrapy.Field()


    staticPath = scrapy.Field()
    timeYmd = scrapy.Field()
    slug = scrapy.Field()



    pass
