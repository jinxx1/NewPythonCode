import sys
import os
import pymysql
from urllib.parse import urlparse

LANG = 'en'

conn = pymysql.connect(host='120.24.4.84', port=3306, user='rdev', password='87d54305a48046c8bb3a9c7ac472981d', db='umxh', charset='utf8')
cur = conn.cursor()
cur.execute("USE umxh")


def updatedb(rid, type0, type1, type2):
    print("%s %s %s %s" % (rid,type0,type1,type2))
    if True:
        cur.execute("update ztbProject set business_type = %s, minor_business_type=%s, minor_business_type_details = %s, business_type_source=2 where id = %s", (type0, type1, type2, rid))
        conn.commit()

cate1 = {}
cate_count = 0
cate_values = 0
label_names = []
def process_line(line):
    global cate1,cate_count,cate_values,label_names
    tabs = line.split('\t')
    if len(tabs) < 9:
        return
    cate0_name = tabs[7]
    cate1_name = tabs[8]
    cate2_name = tabs[9]
    rid = tabs[0]
    updatedb(rid, cate0_name, cate1_name, cate2_name)
    cate_count = cate_count + 1
    #print("cates:%d" % cate_count)

def txt2db(src):
    print("txt2db from %s" % (src))
    fp = open(src, 'r')
    line = fp.readline()
    while line !='':
        line = fp.readline()
        process_line(line)
    fp.close()
    print("cates:%d" % cate_count)
    return cate_count

if __name__ == "__main__":
    filepath = sys.argv[1]
    txt2db(filepath)
