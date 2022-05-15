# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
import time,datetime
from NEW_GGZY.Breakpoint import *


TEMPPATH = TMEPTEST()


class CcgpGansuSpider(scrapy.Spider):
    name = 'ccgp_gansu'
    allowed_domains = ['www.ccgp-gansu.gov.cn']
    base_url = 'http://www.ccgp-gansu.gov.cn/web/doSearchmxarticle.action?limit=20&start={}'
    urlDict = [{'catName': '甘肃省_省级_公开招标', 'dtype': 'd62', 'classname': 'c1280501'}, {'catName': '甘肃省_省级_邀请招标', 'dtype': 'd62', 'classname': 'c1280502'}, {'catName': '甘肃省_省级_询价公告', 'dtype': 'd62', 'classname': 'c1280101'}, {'catName': '甘肃省_省级_竞争性谈判', 'dtype': 'd62', 'classname': 'c1280103'}, {'catName': '甘肃省_省级_竞争性磋商', 'dtype': 'd62', 'classname': 'c1280104'}, {'catName': '甘肃省_省级_单一来源', 'dtype': 'd62', 'classname': 'c1280102'}, {'catName': '甘肃省_省级_单一来源公示', 'dtype': 'd62', 'classname': 'c1280105'}, {'catName': '甘肃省_省级_资格预审公告', 'dtype': 'd62', 'classname': 'c12806'}, {'catName': '甘肃省_省级_中标公告', 'dtype': 'd62', 'classname': 'c12802'}, {'catName': '甘肃省_省级_成交公告', 'dtype': 'd62', 'classname': 'c12804'}, {'catName': '甘肃省_省级_更正公告', 'dtype': 'd62', 'classname': 'c12803'}, {'catName': '甘肃省_省级_废标/终止公告', 'dtype': 'd62', 'classname': 'c12807'}, {'catName': '甘肃省_省级_其他公告', 'dtype': 'd62', 'classname': 'c12820'}, {'catName': '甘肃省_兰州市_公开招标', 'dtype': 'd6201', 'classname': 'c1280501'}, {'catName': '甘肃省_兰州市_邀请招标', 'dtype': 'd6201', 'classname': 'c1280502'}, {'catName': '甘肃省_兰州市_询价公告', 'dtype': 'd6201', 'classname': 'c1280101'}, {'catName': '甘肃省_兰州市_竞争性谈判', 'dtype': 'd6201', 'classname': 'c1280103'}, {'catName': '甘肃省_兰州市_竞争性磋商', 'dtype': 'd6201', 'classname': 'c1280104'}, {'catName': '甘肃省_兰州市_单一来源', 'dtype': 'd6201', 'classname': 'c1280102'}, {'catName': '甘肃省_兰州市_单一来源公示', 'dtype': 'd6201', 'classname': 'c1280105'}, {'catName': '甘肃省_兰州市_资格预审公告', 'dtype': 'd6201', 'classname': 'c12806'}, {'catName': '甘肃省_兰州市_中标公告', 'dtype': 'd6201', 'classname': 'c12802'}, {'catName': '甘肃省_兰州市_成交公告', 'dtype': 'd6201', 'classname': 'c12804'}, {'catName': '甘肃省_兰州市_更正公告', 'dtype': 'd6201', 'classname': 'c12803'}, {'catName': '甘肃省_兰州市_废标/终止公告', 'dtype': 'd6201', 'classname': 'c12807'}, {'catName': '甘肃省_兰州市_其他公告', 'dtype': 'd6201', 'classname': 'c12820'}, {'catName': '甘肃省_白银市_公开招标', 'dtype': 'd6204', 'classname': 'c1280501'}, {'catName': '甘肃省_白银市_邀请招标', 'dtype': 'd6204', 'classname': 'c1280502'}, {'catName': '甘肃省_白银市_询价公告', 'dtype': 'd6204', 'classname': 'c1280101'}, {'catName': '甘肃省_白银市_竞争性谈判', 'dtype': 'd6204', 'classname': 'c1280103'}, {'catName': '甘肃省_白银市_竞争性磋商', 'dtype': 'd6204', 'classname': 'c1280104'}, {'catName': '甘肃省_白银市_单一来源', 'dtype': 'd6204', 'classname': 'c1280102'}, {'catName': '甘肃省_白银市_单一来源公示', 'dtype': 'd6204', 'classname': 'c1280105'}, {'catName': '甘肃省_白银市_资格预审公告', 'dtype': 'd6204', 'classname': 'c12806'}, {'catName': '甘肃省_白银市_中标公告', 'dtype': 'd6204', 'classname': 'c12802'}, {'catName': '甘肃省_白银市_成交公告', 'dtype': 'd6204', 'classname': 'c12804'}, {'catName': '甘肃省_白银市_更正公告', 'dtype': 'd6204', 'classname': 'c12803'}, {'catName': '甘肃省_白银市_废标/终止公告', 'dtype': 'd6204', 'classname': 'c12807'}, {'catName': '甘肃省_白银市_其他公告', 'dtype': 'd6204', 'classname': 'c12820'}, {'catName': '甘肃省_临夏州_公开招标', 'dtype': 'd6229', 'classname': 'c1280501'}, {'catName': '甘肃省_临夏州_邀请招标', 'dtype': 'd6229', 'classname': 'c1280502'}, {'catName': '甘肃省_临夏州_询价公告', 'dtype': 'd6229', 'classname': 'c1280101'}, {'catName': '甘肃省_临夏州_竞争性谈判', 'dtype': 'd6229', 'classname': 'c1280103'}, {'catName': '甘肃省_临夏州_竞争性磋商', 'dtype': 'd6229', 'classname': 'c1280104'}, {'catName': '甘肃省_临夏州_单一来源', 'dtype': 'd6229', 'classname': 'c1280102'}, {'catName': '甘肃省_临夏州_单一来源公示', 'dtype': 'd6229', 'classname': 'c1280105'}, {'catName': '甘肃省_临夏州_资格预审公告', 'dtype': 'd6229', 'classname': 'c12806'}, {'catName': '甘肃省_临夏州_中标公告', 'dtype': 'd6229', 'classname': 'c12802'}, {'catName': '甘肃省_临夏州_成交公告', 'dtype': 'd6229', 'classname': 'c12804'}, {'catName': '甘肃省_临夏州_更正公告', 'dtype': 'd6229', 'classname': 'c12803'}, {'catName': '甘肃省_临夏州_废标/终止公告', 'dtype': 'd6229', 'classname': 'c12807'}, {'catName': '甘肃省_临夏州_其他公告', 'dtype': 'd6229', 'classname': 'c12820'}, {'catName': '甘肃省_武威市_公开招标', 'dtype': 'd6206', 'classname': 'c1280501'}, {'catName': '甘肃省_武威市_邀请招标', 'dtype': 'd6206', 'classname': 'c1280502'}, {'catName': '甘肃省_武威市_询价公告', 'dtype': 'd6206', 'classname': 'c1280101'}, {'catName': '甘肃省_武威市_竞争性谈判', 'dtype': 'd6206', 'classname': 'c1280103'}, {'catName': '甘肃省_武威市_竞争性磋商', 'dtype': 'd6206', 'classname': 'c1280104'}, {'catName': '甘肃省_武威市_单一来源', 'dtype': 'd6206', 'classname': 'c1280102'}, {'catName': '甘肃省_武威市_单一来源公示', 'dtype': 'd6206', 'classname': 'c1280105'}, {'catName': '甘肃省_武威市_资格预审公告', 'dtype': 'd6206', 'classname': 'c12806'}, {'catName': '甘肃省_武威市_中标公告', 'dtype': 'd6206', 'classname': 'c12802'}, {'catName': '甘肃省_武威市_成交公告', 'dtype': 'd6206', 'classname': 'c12804'}, {'catName': '甘肃省_武威市_更正公告', 'dtype': 'd6206', 'classname': 'c12803'}, {'catName': '甘肃省_武威市_废标/终止公告', 'dtype': 'd6206', 'classname': 'c12807'}, {'catName': '甘肃省_武威市_其他公告', 'dtype': 'd6206', 'classname': 'c12820'}, {'catName': '甘肃省_张掖市_公开招标', 'dtype': 'd6207', 'classname': 'c1280501'}, {'catName': '甘肃省_张掖市_邀请招标', 'dtype': 'd6207', 'classname': 'c1280502'}, {'catName': '甘肃省_张掖市_询价公告', 'dtype': 'd6207', 'classname': 'c1280101'}, {'catName': '甘肃省_张掖市_竞争性谈判', 'dtype': 'd6207', 'classname': 'c1280103'}, {'catName': '甘肃省_张掖市_竞争性磋商', 'dtype': 'd6207', 'classname': 'c1280104'}, {'catName': '甘肃省_张掖市_单一来源', 'dtype': 'd6207', 'classname': 'c1280102'}, {'catName': '甘肃省_张掖市_单一来源公示', 'dtype': 'd6207', 'classname': 'c1280105'}, {'catName': '甘肃省_张掖市_资格预审公告', 'dtype': 'd6207', 'classname': 'c12806'}, {'catName': '甘肃省_张掖市_中标公告', 'dtype': 'd6207', 'classname': 'c12802'}, {'catName': '甘肃省_张掖市_成交公告', 'dtype': 'd6207', 'classname': 'c12804'}, {'catName': '甘肃省_张掖市_更正公告', 'dtype': 'd6207', 'classname': 'c12803'}, {'catName': '甘肃省_张掖市_废标/终止公告', 'dtype': 'd6207', 'classname': 'c12807'}, {'catName': '甘肃省_张掖市_其他公告', 'dtype': 'd6207', 'classname': 'c12820'}, {'catName': '甘肃省_酒泉市_公开招标', 'dtype': 'd6209', 'classname': 'c1280501'}, {'catName': '甘肃省_酒泉市_邀请招标', 'dtype': 'd6209', 'classname': 'c1280502'}, {'catName': '甘肃省_酒泉市_询价公告', 'dtype': 'd6209', 'classname': 'c1280101'}, {'catName': '甘肃省_酒泉市_竞争性谈判', 'dtype': 'd6209', 'classname': 'c1280103'}, {'catName': '甘肃省_酒泉市_竞争性磋商', 'dtype': 'd6209', 'classname': 'c1280104'}, {'catName': '甘肃省_酒泉市_单一来源', 'dtype': 'd6209', 'classname': 'c1280102'}, {'catName': '甘肃省_酒泉市_单一来源公示', 'dtype': 'd6209', 'classname': 'c1280105'}, {'catName': '甘肃省_酒泉市_资格预审公告', 'dtype': 'd6209', 'classname': 'c12806'}, {'catName': '甘肃省_酒泉市_中标公告', 'dtype': 'd6209', 'classname': 'c12802'}, {'catName': '甘肃省_酒泉市_成交公告', 'dtype': 'd6209', 'classname': 'c12804'}, {'catName': '甘肃省_酒泉市_更正公告', 'dtype': 'd6209', 'classname': 'c12803'}, {'catName': '甘肃省_酒泉市_废标/终止公告', 'dtype': 'd6209', 'classname': 'c12807'}, {'catName': '甘肃省_酒泉市_其他公告', 'dtype': 'd6209', 'classname': 'c12820'}, {'catName': '甘肃省_嘉峪关市_公开招标', 'dtype': 'd6202', 'classname': 'c1280501'}, {'catName': '甘肃省_嘉峪关市_邀请招标', 'dtype': 'd6202', 'classname': 'c1280502'}, {'catName': '甘肃省_嘉峪关市_询价公告', 'dtype': 'd6202', 'classname': 'c1280101'}, {'catName': '甘肃省_嘉峪关市_竞争性谈判', 'dtype': 'd6202', 'classname': 'c1280103'}, {'catName': '甘肃省_嘉峪关市_竞争性磋商', 'dtype': 'd6202', 'classname': 'c1280104'}, {'catName': '甘肃省_嘉峪关市_单一来源', 'dtype': 'd6202', 'classname': 'c1280102'}, {'catName': '甘肃省_嘉峪关市_单一来源公示', 'dtype': 'd6202', 'classname': 'c1280105'}, {'catName': '甘肃省_嘉峪关市_资格预审公告', 'dtype': 'd6202', 'classname': 'c12806'}, {'catName': '甘肃省_嘉峪关市_中标公告', 'dtype': 'd6202', 'classname': 'c12802'}, {'catName': '甘肃省_嘉峪关市_成交公告', 'dtype': 'd6202', 'classname': 'c12804'}, {'catName': '甘肃省_嘉峪关市_更正公告', 'dtype': 'd6202', 'classname': 'c12803'}, {'catName': '甘肃省_嘉峪关市_废标/终止公告', 'dtype': 'd6202', 'classname': 'c12807'}, {'catName': '甘肃省_嘉峪关市_其他公告', 'dtype': 'd6202', 'classname': 'c12820'}, {'catName': '甘肃省_金昌市_公开招标', 'dtype': 'd6203', 'classname': 'c1280501'}, {'catName': '甘肃省_金昌市_邀请招标', 'dtype': 'd6203', 'classname': 'c1280502'}, {'catName': '甘肃省_金昌市_询价公告', 'dtype': 'd6203', 'classname': 'c1280101'}, {'catName': '甘肃省_金昌市_竞争性谈判', 'dtype': 'd6203', 'classname': 'c1280103'}, {'catName': '甘肃省_金昌市_竞争性磋商', 'dtype': 'd6203', 'classname': 'c1280104'}, {'catName': '甘肃省_金昌市_单一来源', 'dtype': 'd6203', 'classname': 'c1280102'}, {'catName': '甘肃省_金昌市_单一来源公示', 'dtype': 'd6203', 'classname': 'c1280105'}, {'catName': '甘肃省_金昌市_资格预审公告', 'dtype': 'd6203', 'classname': 'c12806'}, {'catName': '甘肃省_金昌市_中标公告', 'dtype': 'd6203', 'classname': 'c12802'}, {'catName': '甘肃省_金昌市_成交公告', 'dtype': 'd6203', 'classname': 'c12804'}, {'catName': '甘肃省_金昌市_更正公告', 'dtype': 'd6203', 'classname': 'c12803'}, {'catName': '甘肃省_金昌市_废标/终止公告', 'dtype': 'd6203', 'classname': 'c12807'}, {'catName': '甘肃省_金昌市_其他公告', 'dtype': 'd6203', 'classname': 'c12820'}, {'catName': '甘肃省_天水市_公开招标', 'dtype': 'd6205', 'classname': 'c1280501'}, {'catName': '甘肃省_天水市_邀请招标', 'dtype': 'd6205', 'classname': 'c1280502'}, {'catName': '甘肃省_天水市_询价公告', 'dtype': 'd6205', 'classname': 'c1280101'}, {'catName': '甘肃省_天水市_竞争性谈判', 'dtype': 'd6205', 'classname': 'c1280103'}, {'catName': '甘肃省_天水市_竞争性磋商', 'dtype': 'd6205', 'classname': 'c1280104'}, {'catName': '甘肃省_天水市_单一来源', 'dtype': 'd6205', 'classname': 'c1280102'}, {'catName': '甘肃省_天水市_单一来源公示', 'dtype': 'd6205', 'classname': 'c1280105'}, {'catName': '甘肃省_天水市_资格预审公告', 'dtype': 'd6205', 'classname': 'c12806'}, {'catName': '甘肃省_天水市_中标公告', 'dtype': 'd6205', 'classname': 'c12802'}, {'catName': '甘肃省_天水市_成交公告', 'dtype': 'd6205', 'classname': 'c12804'}, {'catName': '甘肃省_天水市_更正公告', 'dtype': 'd6205', 'classname': 'c12803'}, {'catName': '甘肃省_天水市_废标/终止公告', 'dtype': 'd6205', 'classname': 'c12807'}, {'catName': '甘肃省_天水市_其他公告', 'dtype': 'd6205', 'classname': 'c12820'}, {'catName': '甘肃省_定西市_公开招标', 'dtype': 'd6211', 'classname': 'c1280501'}, {'catName': '甘肃省_定西市_邀请招标', 'dtype': 'd6211', 'classname': 'c1280502'}, {'catName': '甘肃省_定西市_询价公告', 'dtype': 'd6211', 'classname': 'c1280101'}, {'catName': '甘肃省_定西市_竞争性谈判', 'dtype': 'd6211', 'classname': 'c1280103'}, {'catName': '甘肃省_定西市_竞争性磋商', 'dtype': 'd6211', 'classname': 'c1280104'}, {'catName': '甘肃省_定西市_单一来源', 'dtype': 'd6211', 'classname': 'c1280102'}, {'catName': '甘肃省_定西市_单一来源公示', 'dtype': 'd6211', 'classname': 'c1280105'}, {'catName': '甘肃省_定西市_资格预审公告', 'dtype': 'd6211', 'classname': 'c12806'}, {'catName': '甘肃省_定西市_中标公告', 'dtype': 'd6211', 'classname': 'c12802'}, {'catName': '甘肃省_定西市_成交公告', 'dtype': 'd6211', 'classname': 'c12804'}, {'catName': '甘肃省_定西市_更正公告', 'dtype': 'd6211', 'classname': 'c12803'}, {'catName': '甘肃省_定西市_废标/终止公告', 'dtype': 'd6211', 'classname': 'c12807'}, {'catName': '甘肃省_定西市_其他公告', 'dtype': 'd6211', 'classname': 'c12820'}, {'catName': '甘肃省_平凉市_公开招标', 'dtype': 'd6208', 'classname': 'c1280501'}, {'catName': '甘肃省_平凉市_邀请招标', 'dtype': 'd6208', 'classname': 'c1280502'}, {'catName': '甘肃省_平凉市_询价公告', 'dtype': 'd6208', 'classname': 'c1280101'}, {'catName': '甘肃省_平凉市_竞争性谈判', 'dtype': 'd6208', 'classname': 'c1280103'}, {'catName': '甘肃省_平凉市_竞争性磋商', 'dtype': 'd6208', 'classname': 'c1280104'}, {'catName': '甘肃省_平凉市_单一来源', 'dtype': 'd6208', 'classname': 'c1280102'}, {'catName': '甘肃省_平凉市_单一来源公示', 'dtype': 'd6208', 'classname': 'c1280105'}, {'catName': '甘肃省_平凉市_资格预审公告', 'dtype': 'd6208', 'classname': 'c12806'}, {'catName': '甘肃省_平凉市_中标公告', 'dtype': 'd6208', 'classname': 'c12802'}, {'catName': '甘肃省_平凉市_成交公告', 'dtype': 'd6208', 'classname': 'c12804'}, {'catName': '甘肃省_平凉市_更正公告', 'dtype': 'd6208', 'classname': 'c12803'}, {'catName': '甘肃省_平凉市_废标/终止公告', 'dtype': 'd6208', 'classname': 'c12807'}, {'catName': '甘肃省_平凉市_其他公告', 'dtype': 'd6208', 'classname': 'c12820'}, {'catName': '甘肃省_庆阳市_公开招标', 'dtype': 'd6210', 'classname': 'c1280501'}, {'catName': '甘肃省_庆阳市_邀请招标', 'dtype': 'd6210', 'classname': 'c1280502'}, {'catName': '甘肃省_庆阳市_询价公告', 'dtype': 'd6210', 'classname': 'c1280101'}, {'catName': '甘肃省_庆阳市_竞争性谈判', 'dtype': 'd6210', 'classname': 'c1280103'}, {'catName': '甘肃省_庆阳市_竞争性磋商', 'dtype': 'd6210', 'classname': 'c1280104'}, {'catName': '甘肃省_庆阳市_单一来源', 'dtype': 'd6210', 'classname': 'c1280102'}, {'catName': '甘肃省_庆阳市_单一来源公示', 'dtype': 'd6210', 'classname': 'c1280105'}, {'catName': '甘肃省_庆阳市_资格预审公告', 'dtype': 'd6210', 'classname': 'c12806'}, {'catName': '甘肃省_庆阳市_中标公告', 'dtype': 'd6210', 'classname': 'c12802'}, {'catName': '甘肃省_庆阳市_成交公告', 'dtype': 'd6210', 'classname': 'c12804'}, {'catName': '甘肃省_庆阳市_更正公告', 'dtype': 'd6210', 'classname': 'c12803'}, {'catName': '甘肃省_庆阳市_废标/终止公告', 'dtype': 'd6210', 'classname': 'c12807'}, {'catName': '甘肃省_庆阳市_其他公告', 'dtype': 'd6210', 'classname': 'c12820'}, {'catName': '甘肃省_陇南市_公开招标', 'dtype': 'd6212', 'classname': 'c1280501'}, {'catName': '甘肃省_陇南市_邀请招标', 'dtype': 'd6212', 'classname': 'c1280502'}, {'catName': '甘肃省_陇南市_询价公告', 'dtype': 'd6212', 'classname': 'c1280101'}, {'catName': '甘肃省_陇南市_竞争性谈判', 'dtype': 'd6212', 'classname': 'c1280103'}, {'catName': '甘肃省_陇南市_竞争性磋商', 'dtype': 'd6212', 'classname': 'c1280104'}, {'catName': '甘肃省_陇南市_单一来源', 'dtype': 'd6212', 'classname': 'c1280102'}, {'catName': '甘肃省_陇南市_单一来源公示', 'dtype': 'd6212', 'classname': 'c1280105'}, {'catName': '甘肃省_陇南市_资格预审公告', 'dtype': 'd6212', 'classname': 'c12806'}, {'catName': '甘肃省_陇南市_中标公告', 'dtype': 'd6212', 'classname': 'c12802'}, {'catName': '甘肃省_陇南市_成交公告', 'dtype': 'd6212', 'classname': 'c12804'}, {'catName': '甘肃省_陇南市_更正公告', 'dtype': 'd6212', 'classname': 'c12803'}, {'catName': '甘肃省_陇南市_废标/终止公告', 'dtype': 'd6212', 'classname': 'c12807'}, {'catName': '甘肃省_陇南市_其他公告', 'dtype': 'd6212', 'classname': 'c12820'}, {'catName': '甘肃省_甘南州_公开招标', 'dtype': 'd6230', 'classname': 'c1280501'}, {'catName': '甘肃省_甘南州_邀请招标', 'dtype': 'd6230', 'classname': 'c1280502'}, {'catName': '甘肃省_甘南州_询价公告', 'dtype': 'd6230', 'classname': 'c1280101'}, {'catName': '甘肃省_甘南州_竞争性谈判', 'dtype': 'd6230', 'classname': 'c1280103'}, {'catName': '甘肃省_甘南州_竞争性磋商', 'dtype': 'd6230', 'classname': 'c1280104'}, {'catName': '甘肃省_甘南州_单一来源', 'dtype': 'd6230', 'classname': 'c1280102'}, {'catName': '甘肃省_甘南州_单一来源公示', 'dtype': 'd6230', 'classname': 'c1280105'}, {'catName': '甘肃省_甘南州_资格预审公告', 'dtype': 'd6230', 'classname': 'c12806'}, {'catName': '甘肃省_甘南州_中标公告', 'dtype': 'd6230', 'classname': 'c12802'}, {'catName': '甘肃省_甘南州_成交公告', 'dtype': 'd6230', 'classname': 'c12804'}, {'catName': '甘肃省_甘南州_更正公告', 'dtype': 'd6230', 'classname': 'c12803'}, {'catName': '甘肃省_甘南州_废标/终止公告', 'dtype': 'd6230', 'classname': 'c12807'}, {'catName': '甘肃省_甘南州_其他公告', 'dtype': 'd6230', 'classname': 'c12820'}, {'catName': '甘肃省_兰州新区_公开招标', 'dtype': 'd620124', 'classname': 'c1280501'}, {'catName': '甘肃省_兰州新区_邀请招标', 'dtype': 'd620124', 'classname': 'c1280502'}, {'catName': '甘肃省_兰州新区_询价公告', 'dtype': 'd620124', 'classname': 'c1280101'}, {'catName': '甘肃省_兰州新区_竞争性谈判', 'dtype': 'd620124', 'classname': 'c1280103'}, {'catName': '甘肃省_兰州新区_竞争性磋商', 'dtype': 'd620124', 'classname': 'c1280104'}, {'catName': '甘肃省_兰州新区_单一来源', 'dtype': 'd620124', 'classname': 'c1280102'}, {'catName': '甘肃省_兰州新区_单一来源公示', 'dtype': 'd620124', 'classname': 'c1280105'}, {'catName': '甘肃省_兰州新区_资格预审公告', 'dtype': 'd620124', 'classname': 'c12806'}, {'catName': '甘肃省_兰州新区_中标公告', 'dtype': 'd620124', 'classname': 'c12802'}, {'catName': '甘肃省_兰州新区_成交公告', 'dtype': 'd620124', 'classname': 'c12804'}, {'catName': '甘肃省_兰州新区_更正公告', 'dtype': 'd620124', 'classname': 'c12803'}, {'catName': '甘肃省_兰州新区_废标/终止公告', 'dtype': 'd620124', 'classname': 'c12807'}, {'catName': '甘肃省_兰州新区_其他公告', 'dtype': 'd620124', 'classname': 'c12820'}]
    # urlDict = [{'catName': '甘肃省_省级_公开招标', 'dtype': 'd62', 'classname': 'c1280501'}]


    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlDict)
        meta['Num'] = 0
        meta['releaseendtime'] = str(datetime.datetime.now()).split(' ')[0]
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['dtype'] = i['dtype']
            meta['classname'] = i['classname']
            datePost = {
                    "articleSearchInfoVo.releasestarttime": '2018-01-01',
                    "articleSearchInfoVo.releaseendtime": meta['releaseendtime'],
                    "articleSearchInfoVo.tflag": "1",
                    "articleSearchInfoVo.classname": meta['classname'],
                    "articleSearchInfoVo.dtype":meta['dtype'],
                    "articleSearchInfoVo.days":"",
                    "articleSearchInfoVo.releasestarttimeold":"",
                    "articleSearchInfoVo.releaseendtimeold":"",
                    "articleSearchInfoVo.title":"",
                    "articleSearchInfoVo.agentname":"",
                    "articleSearchInfoVo.bidcode":"",
                    "articleSearchInfoVo.proj_name":"",
                    "articleSearchInfoVo.buyername":"",
                    # "total": "181",
                    # "limit": "20",
                    # "current": "1",
                    "sjm": "7466",
            }
            yield scrapy.FormRequest(url=self.base_url.format(str(meta['Num'])),
                                     formdata=datePost,callback=self.parse,
                                     meta=meta,dont_filter=True,
                                     headers={'Referer': 'http://www.ccgp-gansu.gov.cn/web/doSearchmxarticle.action'})



    def parse(self, response):
        meta = response.meta
        link = response.xpath("//ul[@class='Expand_SearchSLisi']//a/@href").extract()

        GotArtcl = 0
        notGotArtcl = 0
        if len(link) > 0:
            for i in range(len(link) + 1):
                urlListTemp = []
                # print('进入List循环体了')
                if notGotArtcl == 0 and GotArtcl == len(link):
                    # print('-------------------------------没有新文章退出')
                    return None
                elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(link):
                    # print('--------------------翻页')
                    meta['Num'] += 20
                    datePost = {
                        "articleSearchInfoVo.releasestarttime": '2018-01-01',
                        "articleSearchInfoVo.releaseendtime": meta['releaseendtime'],
                        "articleSearchInfoVo.tflag": "1",
                        "articleSearchInfoVo.classname": meta['classname'],
                        "articleSearchInfoVo.dtype": meta['dtype'],
                        "articleSearchInfoVo.days": "",
                        "articleSearchInfoVo.releasestarttimeold": "",
                        "articleSearchInfoVo.releaseendtimeold": "",
                        "articleSearchInfoVo.title": "",
                        "articleSearchInfoVo.agentname": "",
                        "articleSearchInfoVo.bidcode": "",
                        "articleSearchInfoVo.proj_name": "",
                        "articleSearchInfoVo.buyername": "",
                        # "total": "181",
                        # "limit": "20",
                        # "current": "1",
                        "sjm": "7466",
                    }
                    yield scrapy.FormRequest(url=self.base_url.format(str(meta['Num'])),
                                             formdata=datePost, callback=self.parse,
                                             meta=meta, dont_filter=True,
                                             headers={
                                                 'Referer': 'http://www.ccgp-gansu.gov.cn/web/doSearchmxarticle.action'})
                else:
                    # print('--------------------最终进入文章')
                    urlTemp = parse.urljoin(response.url, link[i])
                    urlListTemp.append(urlTemp + TEMPPATH)
                    urllist = urlIsExist(urlListTemp)
                    if len(urllist) < 1:
                        GotArtcl += 1
                        continue
                    else:
                        notGotArtcl += 1
                        for url in urllist:
                            try:
                                meta['articleTitle'] = response.xpath("//a[@href = '{}']/text()".format(str(link[i]))).extract()[0]
                            except:
                                print('没找到标题****************')
                                continue
                            try:
                                articleTime = response.xpath("//a[@href = '{}']/../p/span/text()".format(str(link[i]))).extract()[0]
                                meta['articleTime'] = re.findall("发布时间：(.*?) \|",articleTime)[0]
                            except:
                                print('没找到时间****************')
                                continue
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,
                                                 dont_filter=True)
        else:

            return None

    def parseA(self, response):
        # print('进入文章了')

        meta = response.meta
        dict1 = {}

        attachmentListJsonList = []
        dict1['attachmentListJson'] = []
        try:
            html = response.xpath("//div[@id='fontzoom']").extract()[0]
            dict1['content'] = html
        except:
            return None

        fujianlink = response.xpath("//*[text()='附件下载']/../../../tr/td/a/@href").extract()
        if len(fujianlink) > 0:
            for fujianUrl in fujianlink:
                fujianName = response.xpath("//*[@href = '{}']/text()".format(fujianUrl)).extract()[0]
                attachmentDict = {}
                attachmentDict['downloadUrl'] = parse.urljoin(response.url, fujianUrl)
                attachmentDict['name'] = fujianName
                attachmentListJsonList.append(attachmentDict)
            dict1['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)



        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle'].strip()
        dict1['issueTime'] = timeReMark(meta['articleTime'])
        dict1['subclass'] = meta['catName']

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        # writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(dict1['subclass'])
        print(dict1['attachmentListJson'])
        print(len(dict1['content']))
        save_api(dict1)
        print('--------------------------------------------------------------------------------------------')


