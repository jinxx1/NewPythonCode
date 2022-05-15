import os,time,pprint,pymysql,sys

HOST = "localhost"
DBNAME = "HOME"
LAB = 'homepic'
USER = "root"
PASSWORD = "aa040304"
CHARSET = "utf8"
USE_UNICON = True


def inserMYSQL(item):
    # try:
    insert_code = '''
    INSERT INTO homepic(picCat,picName,picPath,pic_day,pic_month,pic_size,pic_splitext,pic_year)
    VALUES (
    '{picCat}',
    '{picName}',
    '{picPath}',
    '{pic_day}',
    '{pic_month}',
    '{pic_size}',
    '{pic_splitext}',
    '{pic_year}'
    )'''
    inser_excut = insert_code.format(
        picCat = pymysql.escape_string(item['picCat']),
        picName = pymysql.escape_string(item['picName']),
        picPath = pymysql.escape_string(item['picPath'].replace('\\','/')),
        pic_day = pymysql.escape_string(item['pic_day']),
        pic_month = pymysql.escape_string(item['pic_month']),
        pic_size = pymysql.escape_string(str(item['pic_size'])),
        pic_splitext = pymysql.escape_string(item['pic_splitext']),
        pic_year = pymysql.escape_string(item['pic_year']))
    cursor.execute(inser_excut)
    db.commit()
    # except:
    #     return None



def picSortOut(picPath,picName,pathluan):
    picDict = {}
    picDict['pic_size'] = os.stat(path=picPath).st_size
    picDict['pic_splitext'] = os.path.splitext(picPath)[-1].replace('.','')
    if picDict['pic_splitext'] == 'db' or picDict['pic_splitext'] == 'tmp' or picDict['pic_size'] == 0:
        os.remove(picPath)
        return None
    ModifiedTime = time.localtime(os.stat(path=picPath).st_mtime)
    picDict['pic_year']=time.strftime('%Y',ModifiedTime)
    picDict['pic_month']=time.strftime('%m',ModifiedTime)
    picDict['pic_day']=time.strftime('%d',ModifiedTime)

    picDict['picPath'] = picPath
    picDict['picName'] = picName
    picDict['picCat'] = picPath.replace(pathluan,'').replace(picName,'').replace('\\','')
    return picDict


def file_name_walk(file_dir):

    listpath = []
    for root, dirs, files in os.walk(file_dir):
        dictTemp = {}
        dictTemp['root'] = root# 当前目录路径
        dictTemp['dirs'] = dirs# 当前路径下所有子目录
        dictTemp['files'] = files# 当前路径下所有非目录子文件
        listpath.append(dictTemp)
    return listpath


if __name__ == "__main__":

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

    pathluan = 'D:\homePic_luan'

    # pathluan = r'\\192.168.1.1\XiaoMi\[备份]samsung-SM-G9250\相册\2015年11月'
    # pathluan = r'\\192.168.1.1\XiaoMi'

    fileAll = file_name_walk(pathluan)

    for tis in fileAll:
        for picName in tis['files']:
            picPath = tis['root'] + '\\' + picName
            picCat = tis['dirs']
            picDict = picSortOut(picPath,picName,pathluan)
            inser_sql = inserMYSQL(picDict)
            pprint.pprint(picDict)
            print('*********************************')
    cursor.close()
    db.close()