import pymysql
import datetime
ToDayDate = int(datetime.datetime.now().strftime('%Y%m%d'))
def wxspider_datebse():
    db = pymysql.connect(
        host="120.79.192.168",
        db="wxspider",
        user="xey",
        passwd="85f0a9e2e63b47c0b56202824195fb70#AAA",
        charset="utf8",
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor)

    cursor = db.cursor()
    return cursor,db
def umxh_datebase():
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
    return cursor,db
cursors_wxspider,db_wxspider = wxspider_datebse()
cursors_umxh,db_umxh = umxh_datebase()
# wxspider_seachdate_todaynowANDcopyRisnull =\
#     "SELECT * FROM wenzhang_info WHERE to_days(date_time) = TO_DAYS(NOW()) AND copyR is null "
wxspider_seachdate_todaynowANDcopyRisnull ="SELECT * FROM wenzhang_info WHERE copyR is null "
read_mpid= "SELECT _id,name,company FROM mp_info WHERE _id = {_id}"



insert_ztbInfo = '''
                                    INSERT INTO ztbInfo(site_name,page_title,page_url,created,spiderKey)
                                    VALUES (
                                    '{site_name}',
                                    '{page_title}',
                                    '{page_url}',
                                    '{created}',
                                    '{spiderKey}'
                                    )'''
insert_ztbInfo_content = '''
                                    INSERT INTO ztbInfoContent(info_id,content)
                                    VALUES (
                                    '{info_id}',
                                    '{content}'
                                    )'''
insert_1_to_wxspider_wenzhanginfo_copyR = "update wenzhang_info set copyR = 1 where _id = {_id}"

# 读取wxspider库的wenzhang_info表所有数据
cursors_wxspider.execute(wxspider_seachdate_todaynowANDcopyRisnull)

for item in cursors_wxspider.fetchall():
    idname = "SELECT name FROM mp_info WHERE _id = {}".format(item['mp_id'])
    cursors_wxspider.execute(idname)
    nameWord = cursors_wxspider.fetchall()
    try:
        wxName = nameWord[0]['name']
    except:
        continue
    try:
        # 往umxh库的ztbinfo和ztbinfo_content两张表里写数据
        ztbInfo_inserFormat = insert_ztbInfo.format(
            site_name= '公众号：' + wxName,
            page_title=item['title'],
            page_url=item['content_url'],
            created = item['date_time'],
            spiderKey=ToDayDate,
        )
        cursors_umxh.execute(ztbInfo_inserFormat)
        sql_id = db_umxh.insert_id()
        print(sql_id)
        ztbInfoContent_inserFormat = insert_ztbInfo_content.format(
                        info_id=sql_id,
                        content=item['content'].replace('\n','')
                    )
        cursors_umxh.execute(ztbInfoContent_inserFormat)
    except:
        continue
    db_umxh.commit()
    # 修改wxspider库wenzhang_info表中的copyR键值。为1，表示已经写完
    copyR_insert = insert_1_to_wxspider_wenzhanginfo_copyR.format(_id = item['_id'])
    cursors_wxspider.execute(copyR_insert)
    db_wxspider.commit()
    # 从wenzhang_info表读取mp_id数据，并与mp—id数据相对应
    nameAndcompany = read_mpid.format(_id = item['mp_id'])
    cursors_wxspider.execute(nameAndcompany)
    dateall = cursors_wxspider.fetchall()
    for mpinfo in dateall:
        # ins1 = '''INSERT INTO ztbTag(info_id,key,value) VALUES ('{info_id}','{key}','{value}')'''
        ins1 = '''INSERT INTO ztbTag(info_id,keyW,valueW) VALUES ('{info_id}','{key}','{value}')'''
        # ins_name = ins1.format(info_id=123123,key = 'kkk',value = 'vvvv')
        ins_name = ins1.format(info_id = sql_id,key = '公众号名称',value = mpinfo['name'])
        ins_company = ins1.format(info_id = sql_id,key = '公众号主体',value = mpinfo['company'])
        cursors_umxh.execute(ins_name)
        cursors_umxh.execute(ins_company)
        db_umxh.commit()

cursors_wxspider.close()
db_wxspider.close()
cursors_umxh.close()
db_umxh.close()
