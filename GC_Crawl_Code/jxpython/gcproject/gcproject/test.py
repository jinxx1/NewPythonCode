# -*- coding: utf-8 -*-
import datetime
from datetime import datetime

def catid_2_purchaseTypeAndClass(catid):
    dictList = [{'typeName': '不限分类', 'catid': '0'},
                {'typeName': '招标采购信息公告', 'catid': '74166'},
                {
                    'typeName': '预中标公告',
                    'catid': '74167'
                },
                {
                    'typeName': '结果公告',
                    'catid': '74168'
                },
                {
                    'typeName': '更正答疑公告',
                    'catid': '74169'
                },
                {
                    'typeName': '招标文件购买流程',
                    'catid': '74181'}]
    numList_int = [int(i['catid']) for i in dictList]
    numList_str = ','.join([i['catid'] for i in dictList])

    try:
        int(catid)
    except:
        print('catid输入错误，必须全部都是数字：',numList_str)
        return None


    if int(catid) not in numList_int:
        print('catid输入错误，必须是{}这些数字中的一项'.format(numList_str))
        return None


    for info in dictList:
        if int(catid) == int(info['catid']):
            return info['typeName']

if __name__ == '__main__':

    ddict ={'city_name': '深圳市',
 'creation_time': '2020-10-19 20:12:54',
 'end_time': '2020-10-19 20:12:54',
 'issue_time': '2020-10-19 19:24:17',
 'page_url': 'http://www.chinapsp.cn/notice_content.html?itemid=0d1affbf-3a06-4f6b-d702-08d873d23d97',
 'province_name': '广东省',
 'purchase_type': '公开招标',
 'site': 'www.gdebidding.com',
 'subclass': '招标采购信息公告',
 'title': '网球场地面翻新工程招标公告（招标编号：CLF0120SZ12QY77）'}

    comparisonKeys = ('subclass', 'site', 'page_url', 'title', 'issue_time', 'creation_time', 'end_time',
                      'province_name', 'city_name','purchase_type',
                      'business_type','minor_business_type','money','data')


    keysList = [i for i in ddict.keys() if i in comparisonKeys]
    print(keysList)