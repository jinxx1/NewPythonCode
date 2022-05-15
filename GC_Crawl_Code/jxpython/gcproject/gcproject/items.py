# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GcprojectItem(scrapy.Item):

    # ztbRawInfo 表名称（文章信息存储表）
    subclass = scrapy.Field()#子类型
    site = scrapy.Field()#来源站点,域名
    page_url = scrapy.Field()#链接地址
    title = scrapy.Field()#标题
    issue_time = scrapy.Field()#发布时间
    creation_time = scrapy.Field()#抓取开始时间
    end_time = scrapy.Field()#抓取结束时间
    province_name = scrapy.Field()#省
    city_name = scrapy.Field()#市

    purchase_type = scrapy.Field()#采购方式
    business_type = scrapy.Field()#业务大类
    minor_business_type = scrapy.Field()#业务细类
    money = scrapy.Field()#项目金额
# --------------------------------------------------------------------------
    # ztbRawInfoContent 表名称（内容存储表）
    content = scrapy.Field()#公告内容
    raw_data_id = scrapy.Field()#公告内容
# --------------------------------------------------------------------------
    # ztbInfoAttachment 表名称（附件存储表）
    attchment = scrapy.Field()
    info_id = scrapy.Field()
    raw_id = scrapy.Field()#公告内容
    download_url = scrapy.Field()#原始网站的附件下载地址
    name = scrapy.Field()#文件对应的名称,如文件名为123.xls,name为广州招标

