# -*- coding: utf-8 -*-
# author = wph
# date = 2020/10/28
import pymysql

'''本地'''
# mysql_host = '127.0.0.1'
# mysql_port = 3306
# mysql_user = 'root'
# mysql_password = 'root'
# mysql_db = 'pp788'
'''测试'''
# mysql_host = '172.16.10.99'
# mysql_port = 3306
# mysql_user = 'xey'
# mysql_password = 'Xey123456!@#$%^'
# mysql_db = 'shangqing'
'''线上'''
mysql_host = '172.16.10.94'
mysql_port = 3306
mysql_user = 'gzcez'
mysql_password = '1234@Qwer'
mysql_db = 'shangqing'


def insert_mysql(sql):
    res = None
    conn = pymysql.Connect(host=mysql_host,
                           port=mysql_port,
                           user=mysql_user,
                           password=mysql_password,
                           db=mysql_db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        res = conn.insert_id()
        conn.commit()
    except Exception as e:
        print('error  ',e,'**%s**'%sql)
        conn.rollback()
    cur.close()
    conn.close()
    return res

def select_mysql(sql):
    conn = pymysql.Connect(host=mysql_host,
                           port=mysql_port,
                           user=mysql_user,
                           password=mysql_password,
                           db=mysql_db)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    data_list = cur.fetchall()
    conn.close()
    return data_list

# sql = 'https://cgpt.sotcbb.com/detail?cggg&qczbcg_szcg_4ef6f55b-e214-4d85-ae5a-d4368a1ec630.html'
# num = select_mysql("SELECT COUNT(*) FROM `ztbrawinfo` WHERE page_url = '%s'"%sql)
# print(num,type(num))
# a = num[0]['COUNT(*)']
# print(a,type(a))

import pymysql
from DBUtils.PooledDB import PooledDB, SharedDBConnection
'''
连接池
'''
class MysqlPool(object):

    def __init__(self):
        self.POOL = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=10,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=mysql_host,
            port=mysql_port,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db,
            charset='utf8'
        )
    def __new__(cls, *args, **kw):
        '''
        启用单例模式
        :param args:
        :param kw:
        :return:
        '''
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def connect(self):
        '''
        启动连接
        :return:
        '''
        conn = self.POOL.connection()
        cur = conn.cursor()
        return conn, cur

    def connect_close(self,conn, cursor):
        '''
        关闭连接
        :param conn:
        :param cursor:
        :return:
        '''
        cursor.close()
        conn.close()

    def fetch_all(self,sql, args):
        '''
        批量查询
        :param sql:
        :param args:
        :return:
        '''
        conn, cursor = self.connect()

        cursor.execute(sql, args)
        record_list = cursor.fetchall()
        self.connect_close(conn, cursor)

        return record_list

    def fetch_one(self,sql, args):
        '''
        查询单条数据
        :param sql:
        :param args:
        :return:
        '''
        conn, cursor = self.connect()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        self.connect_close(conn, cursor)

        return result

    def insert(self, sql):
        '''
        插入数据
        :param sql:
        :param args:
        :return:
        '''
        conn, cur = self.connect()
        try:
            cur.execute(sql)
            res = cur._cursor._result.insert_id
            conn.commit()
            self.connect_close(conn, cur)
        except pymysql.err.IntegrityError as e:
            return '该数据已经存在，重复插入'
        except Exception as e1:
            return e1
        return res



