# -*- coding: utf-8 -*-
import pprint,pymysql
from .SechMySql import mysql_inser


class MidcrawlPipeline(object):
    def process_item(self, item, spider):

        inserInfo = mysql_inser(item)

        print('网站名称：  ',item['SiteNameCha'])
        print('网站域名：  ',item['SiteUrl'])
        print('入口链接：  ',item['StartUrl'])
        print('文章标题：  ',item['artTitle'])
        print('文章发布时间：  ',item['artContentTime'])
        print('文章正文长度：  ',len(item['artContent']))
        print('文章链接：  ',item['artUrl'])
        print('爬取规则id：  ',item['Xpath_id'])
        print('****************************   {}   *****************************'.format(inserInfo))
        return item


