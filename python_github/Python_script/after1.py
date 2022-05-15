# -*- coding: utf-8 -*-
import pandas as pd
import pprint
import sqlalchemy
from config import MYSQLINFO
conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO[
                                                                                               'DBNAME'])
mysqlcon = sqlalchemy.create_engine(conStr)

def getBase():
    wordd = r'''通信工程	其它工程	其它工程		
    通信工程	其它工程	其它工程		-
    通信工程	其它工程	其它工程		23
    ICT	集成服务	ICT与集成服务		ICT及其他网络服务
    通信工程	其它工程	其它工程		\
    通信工程	传输工程	通信设备安装	传输设备安装	一干传输设备安装
    通信工程	管线施工	传输管线工程		一干线路
    通信工程	其它工程	其它工程		三方项目
    通信工程	传输工程	通信设备安装	传输设备安装	二干传输设备安装
    通信工程	管线施工	传输管线工程		二干线路
    通信工程	管线施工	传输管线工程		二干线路/传输线路（除干线外）/线路维修整治（含迁改）
    通信工程	管线施工	传输管线工程		二干线路/线路维修整治（含迁改）/传输线路（除干线外）
    通信工程	有线宽带工程	宽带与专线接入		企业宽带与专线接入
    通信工程	有线宽带工程	宽带与专线接入		企业宽带与专线接入类
    通信工程	综合布线与施工	其它综合施工		企业宽带与专线接入类/传输线路（除干线外）
    通信工程	综合布线与施工	其它综合施工		企业宽带与专线接入类/传输线路（除干线外）/驻地网（家宽）工程
    通信工程	综合布线与施工	通信设备安装	综合设备安装	企业宽带与专线接入类/接入层传输设备安装/相关电源配套设备安装/骨干汇聚层传输设备安装/核心机房设备安装/宏蜂窝基站（含天馈线）设备安装
    通信工程	有线宽带工程	宽带与专线接入		企业宽带与专线接入类/线路维修整治（含迁改）/驻地网（家宽）工程
    通信工程	有线宽带工程	宽带与专线接入		企业宽带与专线接入类/驻地网（家宽）工程
    通信工程	综合布线与施工	其它综合施工		企业宽带与专线接入类/驻地网（家宽）工程/传输线路（除干线外）/传输管道/接入层传输设备
    通信工程	有线宽带工程	宽带与专线接入		企业宽带与专线接入类、驻地网（家宽）工程
    通信工程	管线施工	传输管线工程		传输管线
    通信工程	管线施工	传输管线工程		传输管道
    通信工程	管线施工	传输管线工程		传输管道/传输线路（除干线外）
    通信工程	管线施工	传输管线工程		传输管道、传输线路（除干线外）
    通信工程	综合布线与施工	其它综合施工		传输管道、传输线路（除干线外）、一干线路、二干线路、微蜂窝（室分）工程、驻地网（家宽）工程、企业宽带与专线接入类
    通信工程	管线施工	传输管线工程		传输管道、传输线路（除干线外）、管道维修整治（含迁改）
    通信工程	综合布线与施工	其它综合施工		传输管道、传输线路（除干线外）、驻地网（家宽）工程、企业宽带与专线接入类
    通信工程	管线施工	传输管线工程		传输管道工程
    通信工程	管线施工	传输管线工程		传输线路
    通信工程	管线施工	传输管线工程		传输线路(除干线外)
    通信工程	管线施工	传输管线工程		传输线路（除干线外）
    通信工程	有线宽带工程	宽带与专线接入		专线接入（企业宽带）类
    通信工程	管线施工	传输管线工程		传输管道
    通信工程	有线宽带工程	宽带与专线接入	驻地网	驻地网（家宽）工程
    通信工程	管线施工	传输管线工程		传输线路（除干线外）
    通信工程	有线宽带工程	宽带与专线接入		专线接入（企业宽带）类
    通信工程	管线施工	传输管线工程		传输线路（除干线外）
    通信工程	管线施工	传输管线工程		传输线路（除干线外）/二干线路/线路维修整治（含迁改）
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/企业宽带与专线接入类
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/企业宽带与专线接入类/二干线路/线路维修整治（含迁改）
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/企业宽带与专线接入类/传输管道/管道维修整治（含迁改）/二干线路/驻地网（家宽）工程
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/企业宽带与专线接入类/宏蜂窝基站（含天馈线）设备安装/接入层传输设备安装
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/企业宽带与专线接入类/驻地网（家宽）工程/线路维修整治（含迁改）
    通信工程	管线施工	传输管线工程		传输线路（除干线外）/传输管道
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/传输管道/二干线路/企业宽带与专线接入类/驻地网（家宽）工程
    通信工程	管线施工	传输管线工程		传输线路（除干线外）/传输管道/管道维修整治（含迁改）
    通信工程	管线施工	传输管线工程		传输线路（除干线外）/传输管道/线路维修整治（含迁改）
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/接入层传输设备安装/驻地网（家宽）工程
    通信工程	管线施工	传输管线工程		传输线路（除干线外）/线路维修整治（含迁改）
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/线路维修整治（含迁改）/驻地网（家宽）工程/企业宽带与专线接入类
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/驻地网（家宽）工程
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/驻地网（家宽）工程/企业宽带与专线接入类
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/驻地网（家宽）工程/企业宽带与专线接入类/传输管道
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/驻地网（家宽）工程/接入层传输设备安装
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/驻地网（家宽）工程/线路维修整治（含迁改）/企业宽带与专线接入类
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）/骨干汇聚层传输设备安装/宏蜂窝基站（含天馈线）设备安装/接入层传输设备安装
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）、企业宽带与专线接入类、驻地网（家宽）工程
    通信工程	管线施工	传输管线工程		传输线路（除干线外）、传输管道
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）、宏蜂窝基站（含天馈线）设备安装
    通信工程	综合布线与施工	其它综合施工		传输线路（除干线外）、接入层传输设备安装、驻地网（家宽）工程
    通信工程	管线施工	传输管线工程		传输线路（除干线外）、线路维修整治（含迁改）
    通信工程	传输工程	通信设备安装	传输设备安装	传输设备
    通信工程	传输工程	通信设备安装	传输设备安装	传输设备安装工程
    通信工程	传输工程	通信设备安装	传输设备安装	传输设备设备安装工程
    通信工程	综合布线与施工	全业务工程		全业务工程
    通信工程	其它工程	其它工程		其他
    通信工程	其它工程	其它工程		其它
    通信工程	其它工程	配套系统工程		土建及配套系统工程
    通信工程	无线工程	通信设备安装	无线基站安装	宏蜂窝基站（含天馈线）设备安装
    通信工程	无线工程	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装/室分工程(含微蜂窝基站)
    通信工程	无线工程	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装/室分工程(含微蜂窝基站)/相关电源配套设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装/接入层传输设备安装/核心机房设备安装/相关电源配套设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装/接入层传输设备安装/核心机房设备安装/相关电源配套设备安装/室分工程(含微蜂窝基站)/骨干汇聚层传输设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装/接入层传输设备安装/骨干汇聚层传输设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装/接入层传输设备安装/骨干汇聚层传输设备安装/室分工程(含微蜂窝基站)
    通信工程	综合布线与施工	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装/核心机房设备安装/接入层传输设备安装/相关电源配套设备安装/骨干汇聚层传输设备安装
    通信工程	无线工程	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装、室分工程(含微蜂窝基站)
    通信工程	综合布线与施工	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装、接入层传输设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装、接入层传输设备安装、骨干汇聚层传输设备安装、宏蜂窝基站（含天馈线）设备安装
    通信工程	无线工程	通信设备安装	无线基站安装	宏蜂窝基站（含天馈线）设备安装、相关电源配套设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	宏蜂窝基站（含天馈线）设备安装、相关电源配套设备安装、接入层传输设备安装
    通信工程	无线工程	通信设备安装	无线基站安装	宏蜂窝基站（含天馈线）设备安装工程
    通信工程	无线工程	通信设备安装	无线基站安装	宏蜂窝基站（含天馈）设备安装
    通信工程	室分直放站工程	室分与深度覆盖		室分工程(含微蜂窝基站)
    通信工程	无线工程	通信设备安装	综合设备安装	室分工程(含微蜂窝基站)/宏蜂窝基站（含天馈线）设备安装
    通信工程	室分直放站工程	通信设备安装	综合设备安装	室分工程(含微蜂窝基站)/宏蜂窝基站（含天馈线）设备安装/驻地网（家宽）工程
    通信工程	无线工程	通信设备安装	综合设备安装	室分工程(含微蜂窝基站)、宏蜂窝基站（含天馈线）设备安装
    通信工程	室分直放站工程	室分与深度覆盖		室分工程（含微蜂窝基站）
    通信工程	室分直放站工程	室分与深度覆盖		室分工程（含微蜂窝基站）/相关电源配套设备安装
    通信工程	室分直放站工程	室分与深度覆盖		室分施工
    通信工程	有线宽带工程	宽带与专线接入		家集客工程
    通信工程	通信电源与动力工程	配套系统工程		市电引入
    通信工程	室分直放站工程	室分与深度覆盖		微蜂窝室分
    通信工程	室分直放站工程	室分与深度覆盖		微蜂窝（室分）工程
    通信工程	传输工程	通信设备安装	传输设备安装	接入层传输设备安装
    通信工程	传输工程	传输管线工程		接入层传输设备安装/传输线路（除干线外）
    通信工程	综合布线与施工	通信设备安装	综合设备安装	接入层传输设备安装/宏蜂窝基站（含天馈线）设备安装/核心机房设备安装/骨干汇聚层传输设备安装/传输线路（除干线外）/传输管道/相关电源配套设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	接入层传输设备安装/宏蜂窝基站（含天馈线）设备安装/骨干汇聚层传输设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	接入层传输设备安装/宏蜂窝基站（含天馈线）设备安装/骨干汇聚层传输设备安装/相关电源配套设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	接入层传输设备安装/室分工程(含微蜂窝基站)/宏蜂窝基站（含天馈线）设备安装/骨干汇聚层传输设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	接入层传输设备安装/核心机房设备安装/二干传输设备安装/宏蜂窝基站（含天馈线）设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	接入层传输设备安装、宏蜂窝基站（含天馈线）设备安装、骨干汇聚层传输设备安装
    通信工程	综合布线与施工	其它综合施工		接入层传输设备安装、驻地网（家宽）工程
    通信工程	传输工程	通信设备安装	传输设备安装	接入层传输设备安装、骨干汇聚层传输设备安装、二干传输设备安装
    通信工程	管线施工	传输管线工程		本地网与接入网光缆
    通信工程	交换与数据通信工程	通信设备安装	核心设备安装	核心机房设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	核心机房设备安装/相关电源配套设备安装/二干传输设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	核心机房设备安装/骨干汇聚层传输设备安装/接入层传输设备安装/宏蜂窝基站（含天馈线）设备安装/相关电源配套设备安装/二干传输设备安装/一干传输设备安装
    通信工程	交换与数据通信工程	通信设备安装	核心设备安装	核心机房设备设备安装工程
    通信工程	其它工程	其它工程		框架协议
    通信工程	其它工程	其它工程		框架合同
    通信工程	通信电源与动力工程	通信设备安装	配套设备安装	电源配套设备安装工程
    通信工程	通信电源与动力工程	配套系统工程		相关电源配套
    通信工程	通信电源与动力工程	通信设备安装	配套设备安装	相关电源配套设备安装
    通信工程	室分直放站工程	室分与深度覆盖		相关电源配套设备安装、室分工程(含微蜂窝基站)
    通信工程	有线宽带工程	宽带与专线接入		相关电源配套设备安装、驻地网（家宽）工程
    网络维护	管线维护	传输管线工程		管道维修、线路维修整治（含迁改）
    网络维护	管线维护	传输管线工程		管道维修整治（含迁改）
    网络维护	管线维护	传输管线工程		管道维修整治（含迁改）、线路维修整治（含迁改）
    ICT	集成服务	ICT与集成服务		系统集成
    通信工程	无线工程	通信设备安装	无线基站安装	线路宏蜂窝基站（含天馈线）设备安装
    网络维护	管线维护	传输管线工程		线路维修改造（含迁改）
    网络维护	管线维护	传输管线工程		线路维修整改（含迁改）
    网络维护	管线维护	传输管线工程		线路维修整治（含迁改）
    通信工程	综合布线与施工	其它综合施工		线路维修整治（含迁改）/企业宽带与专线接入类
    通信工程	管线施工	传输管线工程		线路维修整治（含迁改）/传输线路（除干线外）
    通信工程	综合布线与施工	其它综合施工		线路维修整治（含迁改）/传输线路（除干线外）/驻地网（家宽）工程
    通信工程	综合布线与施工	其它综合施工		线路维修整治（含迁改）/传输线路（除干线外）/驻地网（家宽）工程/接入层传输设备安装
    通信工程	综合布线与施工	其它综合施工		线路维修整治（含迁改）、驻地网（家宽）工程
    通信工程	综合布线与施工	其它综合施工		线路（除干线外）、驻地网（家宽）工程、专线接入（企业宽带）类、接入层传输设备安装
    通信工程	无线工程	通信设备安装	无线基站安装	蜂窝宏基站含天馈线设备安装
    ICT	集成服务	ICT与集成服务		视频监控
    通信工程	综合布线与施工	通信设备安装	综合设备安装	设备安装
    通信工程	无线工程	其它工程		铁塔改造
    通信工程	有线宽带工程	宽带与专线接入		集团专线及家宽
    通信工程	有线宽带工程	宽带与专线接入	驻地网	驻地网家宽工程
    通信工程	有线宽带工程	宽带与专线接入	驻地网	驻地网（家宽）
    通信工程	有线宽带工程	宽带与专线接入	驻地网	驻地网（家宽）工程
    通信工程	有线宽带工程	宽带与专线接入		驻地网（家宽）工程/企业宽带与专线接入类
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/企业宽带与专线接入类/传输管道/传输线路（除干线外）
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/企业宽带与专线接入类/传输线路（除干线外）
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/企业宽带与专线接入类/传输线路（除干线外）/传输管道
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/企业宽带与专线接入类/线路维修整治（含迁改）
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/企业宽带与专线接入类/线路维修整治（含迁改）/传输线路（除干线外）
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/传输线路（除干线外）
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/传输线路（除干线外）/企业宽带与专线接入类
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/传输线路（除干线外）/企业宽带与专线接入类/接入层传输设备安装
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/传输线路（除干线外）/企业宽带与专线接入类/线路维修整治（含迁改）
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/传输线路（除干线外）/线路维修整治（含迁改）
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/室分工程(含微蜂窝基站)/传输线路（除干线外）
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/线路维修整治（含迁改）
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/线路维修整治（含迁改）/企业宽带与专线接入类
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程/线路维修整治（含迁改）/传输线路（除干线外）/接入层传输设备安装
    通信工程	有线宽带工程	宽带与专线接入		驻地网（家宽）工程、企业宽带与专线接入类
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程、传输管道
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程、传输管道、传输线路（除干线外）
    通信工程	综合布线与施工	其它综合施工		驻地网（家宽）工程、宏蜂窝基站（含天馈线）设备安装
    通信工程	传输工程	通信设备安装	传输设备安装	骨干汇聚层传输设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	骨干汇聚层传输设备安装/接入层传输设备安装/宏蜂窝基站（含天馈线）设备安装
    通信工程	综合布线与施工	通信设备安装	综合设备安装	骨干汇聚层传输设备安装/接入层传输设备安装/核心机房设备安装/宏蜂窝基站（含天馈线）设备安装/二干传输设备安装/相关电源配套设备安装
    通信工程	综合布线与施工	其它综合施工		骨干汇聚层传输设备安装、传输管道、传输线路（除干线外）、企业宽带与专线接入类
    通信工程	综合布线与施工	通信设备安装	综合设备安装	骨干汇聚层传输设备安装、接入层传输设备安装、宏蜂窝基站（含天馈线）设备安装、相关电源配套设备安装'''.split('\n')
    llist = []
    for i in wordd:
        ddict = {}
        a = i.split('\t')
        ddict['business_type'] = a[0]
        ddict['minor_business_type'] = a[1]
        ddict['analyze_primary'] = a[2]
        ddict['analyze_subtypes'] = a[3]
        ddict['category'] = a[4]
        llist.append(ddict)

    df = pd.DataFrame(llist)  # .set_index('category')
    return df


from rexTime import *

import pprint



import numpy as np
from pandas import Series
import cpca


def main_catmark():
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqldb = MYSQLDB()

    # tablesList = ['supervisor_tb7', 'design_tb6', 'construction_tb6']
    tablesList = ['construction_tb6']
    keysList = ['id', 'category']
    llist = []
    for i in tablesList:
        datemysql = mysqldb.get_mysqlinfo(tbName=i, keysList=keysList)
        for ii in datemysql:
            ddict = {}
            ddict['from_id'] = ii[0]
            ddict['category'] = ii[1]
            ddict['from_table'] = i
            llist.append(ddict)
    mysqlDF = pd.DataFrame(llist)
    baseDF = getBase()
    resultTEMP = pd.merge(mysqlDF, baseDF, on=['category'])
    result = resultTEMP.drop_duplicates(['from_id'])

    mysqlcon = sqlalchemy.create_engine(conStr)
    result.to_sql(name='catmark', con=mysqlcon, if_exists='append', index=False, chunksize=1000)


def main_location():
    mysqldb = MYSQLDB()

    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])

    mysqlcon = sqlalchemy.create_engine(conStr)

    # tablesList = ['supervisor_tb7', 'design_tb6', 'construction_tb6']

    tablesList = ['construction_tb6']

    keysList = ['id', 'location_original_str', 'contractor', 'contractor_address']

    for i in tablesList:
        llist = []
        datemysql = mysqldb.get_mysqlinfo(tbName=i, keysList=keysList)
        for ii in datemysql:
            ddict = {}
            ddict['from_id'] = ii[0]
            ddict['location_original_str'] = ii[1]
            ddict['contractor'] = ii[2]
            ddict['contractor_address'] = ii[3]
            ddict['from_table'] = i

            if ddict['location_original_str']:
                item_location = get_location(ddict['location_original_str'])
            else:
                item_location = get_location('无')

            if ddict['contractor']:
                item_contractor = get_location(
                    ddict['contractor'].replace('北京', '').replace('上海', '').replace('天津', '').replace('重庆', ''))
            else:
                item_contractor = get_location('无')

            ddict['Project_province'] = item_location['Project_province']
            ddict['Project_country'] = item_location['Project_country']
            ddict['Project_district'] = item_location['Project_district']
            ddict['remark'] = 'country by location_original_str'

            if item_contractor['Project_district'] != '':
                ddict['Project_district'] = item_contractor['Project_district']

            if ddict['Project_country'] == '' and ddict['Project_province'] == '':

                ddict['Project_province'] = item_contractor['Project_province']
                ddict['Project_country'] = item_contractor['Project_country']
                ddict['Project_district'] = item_contractor['Project_district']
                ddict['remark'] = 'all by contractor'

            elif ddict['Project_country'] == '' and item_contractor['Project_country'] != '':
                ddict['Project_country'] = item_contractor['Project_country']
                ddict['Project_district'] = item_contractor['Project_district']
                ddict['remark'] = 'country by contractor'

            if ddict['Project_country'] == '' and ddict['Project_province'] != '':
                llist.append(ddict)
                continue

            if ddict['contractor_address'] != '':
                supervisorItem = get_location(ddict['Project_country'])
                if ddict['Project_province'] != supervisorItem['Project_province']:
                    addrItem = get_location(ddict['contractor_address'])
                    ddict['Project_country'] = addrItem['Project_country']
                    ddict['Project_district'] = addrItem['Project_district']
                    ddict['remark'] = 'Country by contractor_address'
                    llist.append(ddict)
                    continue
                else:
                    llist.append(ddict)
                    continue
            else:
                llist.append(ddict)
                continue

        DF = pd.DataFrame(llist)
        DF.to_sql(name='locationinfo', con=mysqlcon, if_exists='append', index=False, chunksize=1000)


def main_location_tb3():
    mysqldb = MYSQLDB()
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    tablesList = ['supervisor_tb3', 'construction_tb3']
    keysList = ['id', 'province', 'county', 'address']
    for i in tablesList:
        llist = []
        datemysql = mysqldb.get_mysqlinfo(tbName=i, keysList=keysList)
        for ii in datemysql:
            ddict = {}
            ddict['from_table'] = i
            ddict['from_id'] = ii[0]
            ddict['province'] = ii[1]
            ddict['county'] = ii[2]
            ddict['address'] = ii[3]
            ddict['remark'] = ''
            if not ddict['address'] or ddict['address'] is None or ddict['address'] == '':
                ddict['address'] = '原表无值'

            if not ddict['county'] or ddict['county'] is None or ddict['county'] == '':
                ddict['county'] = '原表无值'

            if not ['province'] or ddict['province'] is None or ddict['province'] == '':
                ddict['province'] = '原表无值'

            item_ADDRESS = get_location(ddict['address'])
            ddict['Project_district'] = item_ADDRESS['Project_district']

            item_Province = get_location(ddict['province'])
            ddict['Project_province'] = item_Province['Project_province']
            if ddict['Project_province']:
                ddict['remark'] += 'by province,'
            else:
                ddict['Project_province'] = item_ADDRESS['Project_province']
                ddict['remark'] += 'by address_province,'

            item_County = get_location(ddict['county'])
            ddict['Project_country'] = item_County['Project_country']

            if ddict['Project_country']:
                ddict['remark'] += 'by county,'
            else:
                ddict['Project_country'] = item_Province['Project_country']
                if ddict['Project_country']:
                    ddict['remark'] += 'by province,'
                else:
                    ddict['Project_country'] = item_ADDRESS['Project_country']
                    ddict['remark'] += 'by address_country,'

            llist.append(ddict)
        DF = pd.DataFrame(llist)
        DF.to_sql(name='locationinfo', con=mysqlcon, if_exists='append', index=False, chunksize=1000)






def main_nagvi_tb7():



    sqlCode = ["SELECT Name,excel_rownum,contract_amount,from_excel_path FROM maintain_tb7_negative WHERE contract_amount < 0;",
               "SELECT Name,excel_rownum,invoice_amount,from_excel_path FROM maintain_tb7_negative WHERE invoice_amount < 0;",
               ]
    for num,sql in enumerate(sqlCode):
        sqlinfoall = mysqlcon.execute(sql)
        for ii in sqlinfoall:
            ddict = {}
            ddict['contract'] = 0
            ddict['invoice'] = 0
            if num == 0:
                ddict['contract'] = 1
                ddict['Name'] = ii[0]
                ddict['excel_rownum'] = ii[1]
                ddict['contract_amount'] = int(ii[2])
                ddict['from_excel_path'] = ii[3]

            if num ==1:
                ddict['invoice'] = 1
                ddict['Name'] = ii[0]
                ddict['excel_rownum'] = ii[1]
                ddict['invoice_amount'] = int(ii[2])
                ddict['from_excel_path'] = ii[3]
            yield ddict



def update_main_nagvi_tb7(item):


    if item['invoice'] == 1:
        sql = '''UPDATE maintain_tb7 SET invoice_amount = {invoice_amount} WHERE Name = '{Name}' AND excel_rownum = '{excel_rownum}' AND from_excel_path = '{from_excel_path}';'''.format(
            invoice_amount = item['invoice_amount'],
            Name = item['Name'],
            excel_rownum = item['excel_rownum'],
            from_excel_path = item['from_excel_path']
        )
        mysqlcon.execute(sql)

    else:
        sql = '''UPDATE maintain_tb7 SET contract_amount = {contract_amount} WHERE Name = '{Name}' AND excel_rownum = '{excel_rownum}' AND from_excel_path = '{from_excel_path}';'''.format(
            contract_amount = item['contract_amount'],
            Name = item['Name'],
            excel_rownum = item['excel_rownum'],
            from_excel_path = item['from_excel_path']
        )

    mysqlcon.execute(sql)






if __name__ == '__main__':
    ddf = main_nagvi_tb7()
    for i in ddf:
        update_main_nagvi_tb7(i)


