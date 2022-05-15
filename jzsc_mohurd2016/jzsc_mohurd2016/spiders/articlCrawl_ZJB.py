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


class ArticlcrawlZjbSpider(scrapy.Spider):
	name = 'articlCrawl_ZJB'
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

	def paseArticle(self, response):
		pass
