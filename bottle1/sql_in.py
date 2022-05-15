#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime,json,pprint
import pymysql


with open('MYSQL_INFO.json',encoding='utf-8') as f:
    line = f.read()
    MySql_INFO = json.loads(line)

HOST = MySql_INFO['HOST']
DB_NAME = MySql_INFO['DB_NAME']
USER_WORD = MySql_INFO['USER_WORD']
PASS_WORD = MySql_INFO['PASS_WORD']

def mysql_indata(item):
    db = pymysql.connect(
        host=HOST,
        db=DB_NAME,
        user=USER_WORD,
        passwd=PASS_WORD,
        charset="utf8",
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = db.cursor()
    insert_code_nocontent = '''
                                INSERT INTO MiddlewareXPATH(CharSet,pageUrl,Content_Text,Content_Title,LinkList,SiteName,SiteUrl,TimeList,TitleList,cutPoint,startUrl,get_List,get_Timew,get_contenturl,get_Title,get_Tag,get_Tag2,get_Tag3,Time_now,yes,uPR,catName,imgDownload,splash_Content,splash_list)
                                VALUES (
                                '{CharSet}',
                                '{pageUrl}',
                                '{Content_Text}',
                                '{Content_Title}',
                                '{LinkList}',
                                '{SiteName}',
                                '{SiteUrl}',
                                '{TimeList}',
                                '{TitleList}',
                                '{cutPoint}',
                                '{startUrl}',
                                '{get_List}',
                                '{get_Timew}',
                                '{get_contenturl}',
                                '{get_Title}',
                                '{get_Tag}',
                                '{get_Tag2}',
                                '{get_Tag3}',
                                '{Time_now}',
                                '{yes}',
                                '{uPR}',
                                '{catName}',
                                '{imgDownload}',
                                '{splash_Content}',
                                '{splash_list}'
                                )'''
    linkListstr = ','.join(item['get_contenturl'])
    q1 = insert_code_nocontent.format(
            CharSet =item['CharSet'],
            pageUrl = item['pageUrl'],
            Content_Text =pymysql.escape_string(item['Content_Text']),
            Content_Title =pymysql.escape_string(item['Content_Title']),
            LinkList =pymysql.escape_string(item['LinkList']),
            SiteName =pymysql.escape_string(item['SiteName']),
            SiteUrl =pymysql.escape_string(item['SiteUrl']),
            TimeList ='None',
            TitleList =pymysql.escape_string(item['TitleList']),
            cutPoint ='None',
            startUrl =item['startUrl'],
            get_List =item['get_url'],
            get_Timew ='None',
            get_contenturl =pymysql.escape_string(linkListstr),
            get_Title =pymysql.escape_string(item['get_TitleList']),
            get_Tag = pymysql.escape_string(item['get_Tag']),
            get_Tag2 = pymysql.escape_string(item['get_Tag2']),
            get_Tag3 = pymysql.escape_string(item['get_Tag3']),
            Time_now = datetime.datetime.now(),
            yes = 0,
            uPR = item['uPR'],
            catName = item['catName'],
            imgDownload = int(item['imgDownload']),
            splash_Content=item['splash_Content'],
            splash_list = item['splash_list'],
        )
    cursor.execute(q1)
    db.commit()
    sql_id = cursor.lastrowid
    cursor.close()
    db.close()
    return sql_id
def mysql_seach(id):
    db = pymysql.connect(
        host=HOST,
        db=DB_NAME,
        user=USER_WORD,
        passwd=PASS_WORD,
        charset="utf8",
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    search_date = "SELECT * FROM MiddlewareXPATH WHERE id='{}'".format(id)
    cursor.execute(search_date)
    resultes = cursor.fetchall()
    return resultes
def mysql_yes(id):
    db = pymysql.connect(
        host=HOST,
        db=DB_NAME,
        user=USER_WORD,
        passwd=PASS_WORD,
        charset="utf8",
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    search_date = "SELECT * FROM MiddlewareXPATH WHERE id='{}'".format(id)
    cursor.execute(search_date)
    resultes = cursor.fetchall()[0]
    if resultes['yes'] ==0:
        insert_yes = '''UPDATE MiddlewareXPATH SET yes=1 WHERE id='{}'
        '''.format(id)
        cursor.execute(insert_yes)
        db.commit()
        return '提交成功'
    else:
        return '该条目已经了，无需重复提交'
    cursor.close()
    db.close()


if __name__ == '__main__':
    item = {"get_List": "http://www.gov.cn/xinwen/gundong.htm",
            "get_Timew": "2019-01-20",
            "get_contenturl": "http://www.gov.cn/xinwen/2019-01/20/content_5359559.htm",
            "get_Title": "通讯：南极冰盖之巅天文观测探秘",
            "get_Tag": "日来，中国第35次南极科考队昆仑队队员在昆仑站天文区",
            "startUrl": "http://www.gov.cn/xinwen/gundong.htm",
            "TitleList": "//*[@class = 'list list_1 list_2']//a/text()",
            "LinkList": "//*[@class = 'list list_1 list_2']//a/@href",
            "TimeList": "//*[@class = 'list list_1 list_2']//span/text()",
            "CharSet": "utf-8",
            "cutPoint": "-",
            "SiteName": "无法获取网站名称，请手动添加",
            "SiteUrl": ["gov.cn"],
            "Content_Title": "//title//text()",
            "Content_Text": "//*[@class = 'pages_content']//p/text()"}
    # idNum = mysql_indata(item)
    # print(idNum)

    ddt =mysql_seach(654)
    pprint.pprint(ddt)