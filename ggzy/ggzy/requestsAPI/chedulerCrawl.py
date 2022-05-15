from apscheduler.schedulers.blocking import BlockingScheduler
import os

def getdate():
        try:
                os.system("ps -ef|grep ccgp_cq.py|grep -v grep|cut -c 9-15|xargs kill -9")
                os.system("ps -ef|grep home/terry/jxpython/wd/chromedriver|grep -v grep|cut -c 9-15|xargs kill -9")
                os.system("ps -ef|grep ccgp_hubei.py|grep -v grep|cut -c 9-15|xargs kill -9")
                os.system("ps -ef|grep ccgp_yunnan.py|grep -v grep|cut -c 9-15|xargs kill -9")
                os.system("ps -ef|grep /home/terry/jxpython/ggzy/ggzy/requestsAPI/wd/chromedriver|grep -v grep|cut -c 9-15|xargs kill -9")
        except:
                pass


if __name__ == '__main__':
        sched = BlockingScheduler()
        sched.add_job(getdate, 'cron', day_of_week='1-6', hour=1, minute=1)
        sched.start()
