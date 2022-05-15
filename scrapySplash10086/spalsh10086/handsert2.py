# coding=utf-8
import re
from bs4 import BeautifulSoup
import sqlalchemy
from pymysql.converters import escape_string
import pymysql, datetime
import pandas as pd
import numpy as np
from pandas import Series
import pprint,json,requests

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_colwidth', 500)


def urlIsExist(urllist):
    HEA = {
        "Connection": "close",
    }
    posturlapi = 'https://umxh.xue2you.cn/pc/api/caijiApi/urlIsExist'
    str_c = json.dumps(urllist)
    dataApi = {"urlListJson": str_c}
    try:
        a = requests.post(url=posturlapi, data=dataApi, headers=HEA)
        jsonT = json.loads(a.text)
        return jsonT['data']
    except:
        return None



def mysqlcon():
	MYSQLINFO = {
		"HOST": "183.6.136.67",
		"DBNAME": "jxtest",
		"USER": "jinxiao_67",
		"PASSWORD": "Abcd!1234.",
		"PORT": 3306
	}
	conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
	                                                                                           PASSWORD=MYSQLINFO[
		                                                                                           'PASSWORD'],
	                                                                                           HOST=MYSQLINFO['HOST'],
	                                                                                           PORT=MYSQLINFO['PORT'],
	                                                                                           DBNAME=MYSQLINFO[
		                                                                                           'DBNAME'])
	mysqlcon = sqlalchemy.create_engine(conStr)
	return mysqlcon

def mysqlconF():
	MYSQLINFO = {
		"HOST": "183.6.136.67",
		"DBNAME": "uxsq",
		"USER": "jinxiao_67",
		"PASSWORD": "Abcd!1234.",
		"PORT": 3306
	}
	conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
	                                                                                           PASSWORD=MYSQLINFO[
		                                                                                           'PASSWORD'],
	                                                                                           HOST=MYSQLINFO['HOST'],
	                                                                                           PORT=MYSQLINFO['PORT'],
	                                                                                           DBNAME=MYSQLINFO[
		                                                                                           'DBNAME'])
	mysqlcon = sqlalchemy.create_engine(conStr)
	return mysqlcon
if __name__ == '__main__':
	wword = '''https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748472
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748455
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748449
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748446
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748445
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748441
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748440
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748439
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748438
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748437
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748433
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748430
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748429
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748428
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748409
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748426
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748423
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748421
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748419
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748405
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748418
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748417
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748416
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748414
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748403
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748412
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748391
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748395
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748388
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748387
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748394
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748381
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748380
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748379
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748376
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748351
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748374
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748372
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748366
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748365
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748364
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748363
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748367
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748347
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748359
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748358
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748357
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748344
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748355
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748354
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748343
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748342
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748328
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748335
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748333
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748311
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748320
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748306
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748318
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748315
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748305
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748304
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748303
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748312
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748301
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748300
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748288
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748299
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748286
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748292
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748280
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748270
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748277
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748268
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748249
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748259
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748258
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748246
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748245
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748244
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748242
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748241
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748239
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748238
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748254
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748253
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748233
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748211
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748226
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748225
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748224
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748217
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748199
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748198
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748214
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748196
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748171
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748168
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748167
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748183
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748164
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748182
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748179
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748177
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748163
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748175
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748148
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748155
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748144
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748143
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748152
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748111
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748108
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748134
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748102
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748100
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748120
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748118
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748115
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748097
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748096
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748113
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748095
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748112
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748071
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748443
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748457
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748473
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748456
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748454
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748453
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748450
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748442
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748407
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748401
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748399
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748389
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748393
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748392
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748375
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748350
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748373
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748370
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748369
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748348
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748360
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748346
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748345
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748339
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748330
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748327
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748332
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748308
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748302
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748296
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748284
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748294
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748282
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748281
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748276
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748247
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748255
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748237
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748230
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748209
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748227
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748208
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748223
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748222
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748206
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748221
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748205
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748204
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748203
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748197
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748195
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748192
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748185
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748166
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748178
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748158
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748157
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748151
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748150
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748149
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748154
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748145
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748139
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748105
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748132
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748130
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748126
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748124
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748123
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748098
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748070
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748092
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748452
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748451
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748448
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748444
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748435
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748434
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748432
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748408
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748424
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748422
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748420
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748406
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748404
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748415
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748413
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748390
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748398
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748397
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748396
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748382
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748349
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748362
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748361
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748336
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748329
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748326
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748323
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748309
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748321
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748307
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748319
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748317
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748316
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748314
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748313
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748291
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748290
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748289
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748298
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748285
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748295
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748293
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748278
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748267
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748266
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748275
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748265
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748273
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748264
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748250
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748261
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748260
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748257
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748256
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748231
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748232
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748210
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748229
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748228
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748207
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748219
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748200
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748216
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748215
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748212
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748194
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748176
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748162
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748159
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748174
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748173
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748156
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748142
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748153
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748141
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748140
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748109
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748128
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748104
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748103
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748101
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748121
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748447
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748436
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748431
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748411
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748410
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748427
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748425
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748402
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748400
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748386
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748385
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748384
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748383
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748378
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748377
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748371
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748368
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748356
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748341
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748340
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748353
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748352
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748331
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748338
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748337
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748334
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748325
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748324
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748310
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748322
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748287
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748297
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748283
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748271
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748279
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748269
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748274
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748272
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748251
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748263
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748262
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748248
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748243
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748240
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748236
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748252
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748235
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748234
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748220
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748218
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748202
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748201
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748213
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748193
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748191
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748190
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748170
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748189
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748169
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748188
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748187
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748186
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748165
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748184
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748181
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748180
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748161
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748160
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748172
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748147
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748146
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748110
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748138
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748137
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748136
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748107
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748135
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748106
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748133
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748131
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748129
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748127
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748125
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748099
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748122
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748119
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748117
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748116
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748114
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748094
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=748093'''.split('\n')

	exc = '''SELECT id FROM ztbRawInfo WHERE site="b2b.10086.cn" and page_url IN ({})'''

	urlword = ['"' +x+ '"' for x in wword]
	urlword = ','.join(urlword)


	mysqlcon=mysqlconF()
	a = mysqlcon.execute(exc.format(urlword))

	for num,i in enumerate(a):
		print(i[0])
	print(num)

