# -*- coding: utf-8 -*-
import scrapy
import json
import pprint, os
import time, datetime
from jzsc_mohurd2016.decrypt import AESDecrypt
from jzsc_mohurd2016.settings import hubSavePath, articleSavePath, urlAllPath, root
from jzsc_mohurd2016.parser import *
import pandas as pd
from scrapy.exceptions import CloseSpider
import logging

def debugFile(LOG_LEVEL, name):
	if not LOG_LEVEL or LOG_LEVEL not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
		return None
	dtime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	debugfileName = dtime + '_{}_{}.log'.format(name, LOG_LEVEL)
	debugfolder = os.path.join(root, '{}_DEBUG-LOG'.format(name))
	if not os.path.exists(debugfolder):
		os.makedirs(debugfolder)
	clearDebugLog(debugfolder)
	return os.path.join(debugfolder, debugfileName)


class HubCrawlSpider(scrapy.Spider):
	name = 'hubCrawl_ZJB'
	allowed_domains = ['jzsc.mohurd.gov.cn']
	LOG_LEVEL = 'DEBUG'
	LOG_FILE = debugFile(LOG_LEVEL, name)
	if not LOG_FILE:
		raise CloseSpider('debugLOG_error, input (CRITICAL,ERROR,WARNING,INFO,DEBUG)')

	custom_settings = {
		'SPIDER_MIDDLEWARES': {
			'jzsc_mohurd2016.middlewares.Close_spider': 20,
		},
		'DOWNLOAD_TIMEOUT': 20,
		'LOG_FILE': LOG_FILE,
		'LOG_LEVEL': LOG_LEVEL
	}

	def start_requests(self):
		meta = {}
		for i in path_walk_urlall(urlAllPath):
			meta['jsonInfo'] = i
			yield scrapy.Request(url=meta['jsonInfo']['url'].format(str(meta['jsonInfo']['crawled_pageNum'])),
			                     callback=self.parse_temp,
			                     meta=meta,
			                     dont_filter=True)

	def parse_temp(self, response):
		meta = response.meta

		datalight = AESDecrypt.decrypt(response.text)
		jsonT = json.loads(datalight)
		meta['jsonInfo']['total'] = jsonT['data']['total']

		# meta['jsonInfo']['status']  0 未处理 1处理中  2 处理完毕
		if meta['jsonInfo']['total'] == 0:
			meta['jsonInfo']['status'] = 2
			with open(meta['jsonInfo']['filePath'], 'w', encoding='utf-8') as ff:
				json.dump(meta['jsonInfo'], ff, ensure_ascii=False)
			msg = messageCreat(meta=meta, message='零文章，结束',filePath=None)
			logging.debug(msg)
			return None

		hub_folder_father = os.path.join(hubSavePath, meta['jsonInfo']['reg_id'])
		mkdir(hub_folder_father)
		hub_folder_son = os.path.join(hub_folder_father, meta['jsonInfo']['apt_id'])
		mkdir(hub_folder_son)
		hub_fileName = 'page_{}_{}.json'.format(str(timeT()), str(meta['jsonInfo']['crawled_pageNum']))
		hub_filePath = os.path.join(hub_folder_son, hub_fileName)
		llist = []
		for num, i in enumerate(jsonT['data']['list']):
			item = i
			item['hub_crawl_status'] = 0
			llist.append(item)
		with open(hub_filePath, 'w', encoding='utf-8') as ff:
			json.dump(llist, ff, ensure_ascii=False)
		msg = messageCreat(meta=meta, message='发现hub数据，写入hubSave文件',filePath=hub_filePath)
		logging.debug(msg)

		count = (int(meta['jsonInfo']['crawled_pageNum'] + 1)) * 15
		if count >= meta['jsonInfo']['total']:
			with open(meta['jsonInfo']['filePath'], 'w', encoding='utf-8') as ff:
				meta['jsonInfo']['status'] = 2
				json.dump(meta['jsonInfo'], ff, ensure_ascii=False)
			msg = messageCreat(meta=meta, message=' 完整结束 status = 2 ',filePath=None)
			logging.debug(msg)
			return None
		else:
			with open(meta['jsonInfo']['filePath'], 'w', encoding='utf-8') as ff:
				meta['jsonInfo']['status'] = 1
				json.dump(meta['jsonInfo'], ff, ensure_ascii=False)

			msg = messageCreat(meta=meta, message=' 文章没抓完，还要继续 status = 1 ',filePath=None)
			logging.debug(msg)

			meta['jsonInfo']['crawled_pageNum'] += 1
			yield scrapy.Request(url=meta['jsonInfo']['url'].format(str(meta['jsonInfo']['crawled_pageNum'])),
			                     callback=self.parse_temp,
			                     meta=meta,
			                     dont_filter=True)
