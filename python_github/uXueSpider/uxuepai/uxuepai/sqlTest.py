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
cursors_wxspider,db_wxspider = wxspider_datebse()




wxspider_seachdate_todaynowANDcopyRisnull =\
    "SELECT * FROM wenzhang_info WHERE copyR is null "
cursors_wxspider.execute(wxspider_seachdate_todaynowANDcopyRisnull)
dateall111 = cursors_wxspider.fetchall()
for item in dateall111:
    print(item['mp_id'])
    read_mpid= "SELECT name FROM mp_info WHERE _id = {}".format(item['mp_id'])
    cursors_wxspider.execute(read_mpid)
    dateall = cursors_wxspider.fetchall()
    wxName = dateall[0]['name']
    print(wxName)
    print(dateall)

cursors_wxspider.close()
db_wxspider.close()