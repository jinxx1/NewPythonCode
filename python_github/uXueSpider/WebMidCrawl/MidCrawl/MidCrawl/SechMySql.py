import pymysql,re
import pprint

HOST = "120.79.192.168"
DBNAME = "dev_umxh"
USER = "xey"
PASSWORD = "85f0a9e2e63b47c0b56202824195fb70#AAA"
CHARSET = "utf8"
USE_UNICON = True


def mysql_seach():
    db = pymysql.connect(
        host=HOST,
        db=DBNAME,
        user=USER,
        passwd=PASSWORD,
        charset=CHARSET,
        use_unicode=USE_UNICON,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    search_date = "SELECT * FROM MiddlewareXPATH WHERE yes=1"
    cursor.execute(search_date)
    resultes = cursor.fetchall()
    cursor.close()
    db.close()
    return resultes

def mysql_inser(item):
    db = pymysql.connect(
        host=HOST,
        db=DBNAME,
        user=USER,
        passwd=PASSWORD,
        charset=CHARSET,
        use_unicode=USE_UNICON,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    insert_code = '''
    INSERT INTO MiddlewareArticleInfo(SiteNameCha,SiteUrl,StartUrl,artTitle,artContent,artUrl,Xpath_id,artContentTime)
    VALUES (
    '{SiteNameCha}',
    '{SiteUrl}',
    '{StartUrl}',
    '{artTitle}',
    '{artContent}',
    '{artUrl}',
    '{Xpath_id}',
    '{artContentTime}'
    )'''
    inser_excut = insert_code.format(
        SiteNameCha = pymysql.escape_string(item['SiteNameCha']),
        SiteUrl = pymysql.escape_string(item['SiteUrl']),
        StartUrl = pymysql.escape_string(item['StartUrl']),
        artTitle = pymysql.escape_string(item['artTitle']),
        artContent = pymysql.escape_string(item['artContent']),
        artUrl = pymysql.escape_string(item['artUrl']),
        Xpath_id = item['Xpath_id'],
        artContentTime = item['artContentTime'])
    cursor.execute(inser_excut)
    db.commit()
    cursor.close()
    db.close()
    return '入库成功'

def mysql_Deduplication(dictList):
    db = pymysql.connect(
        host=HOST,
        db=DBNAME,
        user=USER,
        passwd=PASSWORD,
        charset=CHARSET,
        use_unicode=USE_UNICON,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    listTrueUrl = []
    for link in dictList:
        search_date = "SELECT * FROM MiddlewareArticleInfo WHERE artUrl='{}'".format(link['url'])
        cursor.execute(search_date)
        resultes = cursor.fetchall()

        if isinstance(resultes,list) and len(resultes)>0:
            continue
        else:
            newDict={}
            newDict['url'] = link['url']
            newDict['Num'] = link['Num']
            listTrueUrl.append(link)

    return listTrueUrl
    cursor.close()
    db.close()


if __name__=="__main__":
    pass
