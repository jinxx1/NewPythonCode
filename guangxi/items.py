# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GuangxiItem(scrapy.Item):

    site = scrapy.Field()
    domain = scrapy.Field()
    issueTime = scrapy.Field()
    subclass = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    attachments = scrapy.Field()
    pass
