# -*- coding: utf-8 -*-
import os, time, datetime

from scrapy import cmdline
from multiprocessing import Process
import multiprocessing
import logging

class run():

	def task(self):
		excWord = '''scrapy crawl hubCrawl_ZJB'''.split()
		cmdline.execute(excWord)

	def main_run(self):
		while True:
			pp = multiprocessing.Process(target=self.task)
			logging.info('pp run')
			pp.start()
			pp.join()
			time.sleep(60 * 30)
if __name__ == '__main__':
	obj = run()
	obj.main_run()
