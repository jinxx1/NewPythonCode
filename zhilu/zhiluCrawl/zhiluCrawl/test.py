
import requests,json,pprint,re
from zhiluCrawl.config import MYSQLINFO
import sqlalchemy

conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(
    USER=MYSQLINFO['USER'], PASSWORD=MYSQLINFO['PASSWORD'], HOST=MYSQLINFO['HOST'], PORT=MYSQLINFO['PORT'],
    DBNAME=MYSQLINFO['DBNAME'])

mysqlcon = sqlalchemy.create_engine(conStr)

a = mysqlcon.execute("select id,url from zhilu where title is null and artCode is null")
blist = [{'id':i[0],'url':i[1]} for i in a]

pprint.pprint(blist)


# pUrl = 'https://videodelivery.net/9c64aaf67aa83f11e3c83e77ac6885dc/manifest/stream_1.m3u8'
# acd = requests.get(url=pUrl)
#
# listA = re.findall("seg_(\d{1,4})\.ts",acd.text)
# print(listA)
# print(len(listA))
# listB = ['stream_0', 'stream_1', 'stream_2', 'stream_3', 'stream_4', 'stream_5']
#
# ddict = {
#     'p128':'stream_0',
#     'p240':'stream_1',
#     'p360':'stream_2',
#     'p480':'stream_3',
#     'p720': 'stream_4',
#     'p1080': 'stream_5',
#          }
# videoInfo = {
#     'p128': 'stream_0',
#     'p240': 'stream_1',
#     'p360': 'stream_2',
#     'p480': 'stream_3',
#     'p720': 'stream_4',
#     'p1080': 'stream_5',
#
# }
# for i in videoInfo.keys():
#     del videoInfo[i]
#     print(videoInfo.keys())
# a1 = list(set(listB).difference(set(listA)))
# if a1:
#     for nn in a1:
#         keys = list (ddict.keys()) [list (ddict.values()).index (nn)]
#         del ddict[keys]
# pprint.pprint(ddict)

