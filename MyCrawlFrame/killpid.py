# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
import os



def getdate():
	llist = [
		"ccgp_cq.py",
		"ccgp_hubei.py",
		"ccgp_yunnan.py",
		"chrome",
		"crpsz",
		"sdicc",
	]
	for shell in llist:
		try:
			os.system("ps -ef|grep {}|grep -v grep|cut -c 9-15|xargs kill -9".format(shell))
		except:
			pass


# ps -ef|grep ccgp_cq.py|grep -v grep|cut -c 9-15|xargs kill -9
# ps -ef|grep chrome|grep -v grep|cut -c 9-15|xargs kill -9
# ps -ef|grep {}|grep -v grep|cut -c 9-15|xargs kill -9
if __name__ == '__main__':
	sched = BlockingScheduler()
	sched.add_job(getdate, 'cron', day_of_week='1-6', hour=1, minute=1)
	sched.start()