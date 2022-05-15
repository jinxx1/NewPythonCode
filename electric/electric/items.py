# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ElectricItem(scrapy.Item):
    issueTime = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    subclass = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    attachmentListJson = scrapy.Field()
    pass
