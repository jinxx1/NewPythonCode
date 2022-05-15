#! /usr/bin/python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import pymysql
class UxuepaiPipeline(object):
    def process_item(self, item, spider):
        item['OStime'] = datetime.datetime.now()
        db = pymysql.connect(
            host="120.79.192.168",
            db="umxh",
            user="xey",
            passwd="85f0a9e2e63b47c0b56202824195fb70#AAA",
            charset="utf8",
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = db.cursor()
        search_todaydate = "SELECT * FROM ztbInfo WHERE spiderKey = %d and site = '%s' "%(item['TimeItem'],item['WebNameWord'])
        cursor.execute(search_todaydate)
        resultes = cursor.fetchall()
        quchongList = []
        for row in resultes:
            quchongList.append(row['page_url'])
        if item['LinkItem'] not in quchongList:
            insert_code_nocontent = '''
                                    INSERT INTO ztbInfo(site_name,page_title,page_url,created,spiderKey,site)
                                    VALUES (
                                    '{site_name}',
                                    '{page_title}',
                                    '{page_url}',
                                    '{created}',
                                    '{spiderKey}',
                                    '{site}'
                                    )'''
            q1 = insert_code_nocontent.format(
                site_name=item['NameTOTALItem'],
                page_title=item['TitleItem'],
                page_url=item['LinkItem'],
                created=item['OStime'],
                spiderKey=item['TimeItem'],
                site = item['WebNameWord']
            )
            cursor.execute(q1)
            sql_id = db.insert_id()
            db.commit()
            insert_code_content = '''
                                    INSERT INTO ztbInfoContent(info_id,content)
                                    VALUES (
                                    '{info_id}',
                                    '{content}'
                                    )'''
            q2 = insert_code_content.format(
                info_id=sql_id,
                content=item['WordItem']
            )
            cursor.execute(q2)
            db.commit()
            # print(item['NameTOTALItem'])
            print(item['TitleItem'])
            print(item['TimeItem'])
            # print(item['WordItem'])
            print(item['LinkItem'])
            # print(item['OStime'])
            # print("*********************************************")
            cursor.close()
            db.close()
            return item
        else:
            cursor.close()
            db.close()
            return item