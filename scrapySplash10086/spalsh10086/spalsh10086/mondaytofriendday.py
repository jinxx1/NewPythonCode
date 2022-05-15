from apscheduler.schedulers.blocking import BlockingScheduler
import os,sys,datetime

def main():

	os.system("nohup scrapy crawl t10086 &")


if __name__ == '__main__':
	hour = sys.argv[1]
	sched = BlockingScheduler()
	sched.add_job(main, 'interval',id='6_hour_job',seconds=3600 * int(hour))
	sched.start()