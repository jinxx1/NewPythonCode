#! /usr/bin/python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UxuepaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Pageid = scrapy.Field()#文章入库时候唯一ID，8位int随机生成，已弃用
    NameTOTALItem = scrapy.Field()#被抓取网站的中文名称  str
    TimeItem = scrapy.Field()#被抓取文章在该网站的发布时间，同时做sql去重参考字段之一。int（8）
    TitleItem = scrapy.Field()#被抓取文章的标题。str
    LinkItem = scrapy.Field()#被抓取文章的链接。str，做sql去重判断条件
    OStime = scrapy.Field()#入sql库的系统时间，datatime。datatime
    WordItem = scrapy.Field()#正文内容。str
    WebNameWord = scrapy.Field()#被抓取网站的英文名称。用英文缩写或拼音标示。str


