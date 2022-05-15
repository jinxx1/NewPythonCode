
import json
import pandas as pd
#import stanfordnlp
import pandas as pd
import MySQLdb
import datetime
import dateutil.parser
import time
import hashlib
import os

#显示所有列
# pd.set_option('display.max_columns', None)
#显示所有行
# pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth',100)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


import pprint
def string2timestamp(strValue):
    try:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        return timeStamp
    except ValueError as e:
        return 0
if __name__ == '__main__':


    start = time.time()
    conn = MySQLdb.connect(host="183.6.136.67",user="xey",passwd="xey123456",db="uxsq",charset="utf8")
    csv_data = pd.DataFrame()
    # exc = "select a.id as infoId, guild_id as guildId, page_title as title, project_amount as projectAmount, province, city, b.abbreviation as provinceName, c.name as cityName, business_type as businessType, minor_business_type as minorBusinessType, purchase_source as paramPurchaseSource, d.site_name as purchaseSource, purchase_date as purchaseDate, job_tag as jobTag from ztbInfo as a left join cfgProvince as b on a.province = b.id left join cfgCity as c on a.city = c.id left join ztbSource as d on a.purchase_source = d.id group by a.project_id"

    exc = "select a.id as infoId, guild_id as guildId, page_title as title, project_amount as projectAmount, province, city, b.abbreviation as provinceName, c.name as cityName, business_type as businessType, minor_business_type as minorBusinessType, purchase_source as paramPurchaseSource, d.site_name as purchaseSource, purchase_date as purchaseDate, job_tag as jobTag from ztbInfo as a left join cfgProvince as b on a.province = b.id left join cfgCity as c on a.city = c.id left join ztbSource as d on a.purchase_source = d.id group by a.project_id order by purchase_date desc"
    sql = exc# + " limit 2000"
    db_data = pd.read_sql(sql, conn, index_col='infoId')



    import os,sys

    print(sys.getsizeof(db_data))


    # db_data.to_excel('aa.xls')
    # jsonData = {}
    # csv_data = pd.read_excel('aa.xls',index_col='infoId')
    # print(csv_data)

    # byBussinessCount = csv_data.groupby(by=['jobTag'])['projectAmount'].sum()
    #
    # print(byBussinessCount)
    # print([i for i in amount.values])
    # # print(amount.values.tolist())
    # print([i for i in amount.values.tolist()])



    # print(printdate.info())



    end = time.time()
    print(end - start)
