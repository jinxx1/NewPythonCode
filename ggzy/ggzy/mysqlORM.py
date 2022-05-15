# -*- coding: utf-8 -*-
# @Time : 2021/6/30  17:45
# @File : mysql_demo.py
# @程序说明 :
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# 建立与mysql数据库的链接，格式为：mysql+pymysql://数据库账号:密码@数据库IP/使用的库名
engine = create_engine('mysql+pymysql://数据库账号:数据库密码@数据库ip地址/数据库名', pool_size=20)
# 定义模型类继承父类及数据连接会话
DBsession = sessionmaker(bind=engine)  # 类似于游标
dbsession = scoped_session(DBsession)
Base = declarative_base()  # 定义一个给其他类继承的父类
md = MetaData(bind=engine)  # 元数据: 主要是指数据库表结构、关联等信息


# 定义模型类，类名默认使用驼峰
class OrderDetail(Base):  # 自动加载表结构
    __table__ = Table('数据库表名', md, autoload=True)


def up_analysis_data_for_mysql(table_obj, session, args, filter_cloum):
    """
    封装的通用插入，更新操作方法
    :param table_obj: SQLalchemy映射对象（OrderDetail）
    :param args: 需要插入（更新）的数据
    :param filter_cloum: 用于查询过滤的字段映射字典
    :return:
    """
    return_dict = {'status': '200', 'return_info': '处理成功', 'args': args}
    try:
        if args is None:
            return_dict['status'] = '5004'
            return_dict['return_info'] = '请求参数为空'
        result_detail = session.query(table_obj).filter_by(**dict(filter_cloum))  # 动态接收过滤条件
        # 此处调用数据库的操作方法（增删改）
        if not result_detail.first():
            save_date = table_obj(**dict(args))  # 动态传参
            session.add(save_date)
            session.commit()  # 修改类操作需要手动提交
        else:
            # 有则更新
            result_detail.update(args)  # 动态更新
            session.commit()
    except Exception as E:
        # 出错回滚
        session.rollback()
        return_dict['status'] = '500'
        return_dict['args'] = args
        return_dict['return_info'] = f'{E}'
    finally:
        session.close()
        return return_dict


if __name__ == '__main__':
    # 这个字典的键名对应数据库的字段名，值就是要插入（更新）的数据
    data_dict = {
        'id': 1,
        'mysql_column1': '1',
        'mysql_column2': '2',
    }
    filter_dict = {
        'id':data_dict.get('id')
    }
    up_analysis_data_for_mysql(OrderDetail, dbsession, data_dict, filter_dict)
