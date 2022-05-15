# -*- coding: utf-8 -*-
from NEW_GGZY.Exist import *
import pprint
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from uxue_orm import *
import json
mysql_db_orm = mysql_orm()

class GgzyPipeline(object):
    def process_item(self, item, spider):


        ztbHubInfo_obj = ZtbHubInfo()
        item['creation_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['end_time'] = item['creation_time']
        item['craw_status'] = 1

        item['page_url'] = item['url']
        item['issue_time'] = item['issueTime']

        ztbHubInfo_obj.issue_time = item['issue_time']
        ztbHubInfo_obj.subclass = item['subclass']
        ztbHubInfo_obj.site = item['site']


        ztbRawInfo_insert_id = mysql_db_orm.ztbRawInfo_add_single(hubInfo=ztbHubInfo_obj, articleInfo=item)
        if not ztbRawInfo_insert_id:
            return None
        mysql_db_orm.ztbRawInfoContent_add_single(content=item['content'], rawid=ztbRawInfo_insert_id)
        if 'attachmentListJson' in item.keys():
            attchment = []

            attch = json.loads(item['attachmentListJson'])

            for i in attch:
                ddict = {}
                ddict['download_url'] = i['downloadUrl']
                ddict['download_filename'] = i['name']
                attchment.append(ddict)
            mysql_db_orm.ztbInfoAttaChment_add_single(info=attchment, rawid=ztbRawInfo_insert_id)


        item['content'] = len(item['content'])
        import pprint
        pprint.pprint(item)
        print('-------------------------------已经录入成功')
        bl.insert(item['page_url'])
        return item
