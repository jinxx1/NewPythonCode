# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JzscMohurd2016Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    credit_id = scrapy.Field()
    person_name = scrapy.Field()
    company_location = scrapy.Field()
    art_code = scrapy.Field()
    company_name = scrapy.Field()
    compDetail_info = scrapy.Field()
    regStaffList_info = scrapy.Field()
    caDetailList_info = scrapy.Field()
    compPerformanceListSys_info = scrapy.Field()
    compCreditRecordList_good = scrapy.Field()
    compCreditRecordList_bad = scrapy.Field()
    compCreditBlackList_info = scrapy.Field()
    compPunishList_info = scrapy.Field()
    traceList_info = scrapy.Field()
    remark = scrapy.Field()
    mainID = scrapy.Field()







