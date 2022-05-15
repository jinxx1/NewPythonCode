# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GcProjectItem(scrapy.Item):
    ztb_type = scrapy.Field()
    subclass = scrapy.Field()
    site = scrapy.Field()
    page_url = scrapy.Field()
    title = scrapy.Field()
    issue_time = scrapy.Field()
    creation_time = scrapy.Field()
    city_name = scrapy.Field()
    business_type = scrapy.Field()
    purchase_type = scrapy.Field()


    raw_data_id = scrapy.Field()
    content = scrapy.Field()

    name = scrapy.Field()
    name_1 = scrapy.Field()
    status = scrapy.Field()
    download_url = scrapy.Field()
    download_url_1 = scrapy.Field()
