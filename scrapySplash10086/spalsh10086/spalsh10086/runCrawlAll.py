import os

# 启动10086监控程序
os.system("cd /home/terry/j108/spalsh10086 && nohup python mondaytofriendday.py 4 >/dev/null 2>&1 &")
# 启动scrapyd服务
os.system("cd /home/terry/i139/newscrap/scrap/NEW_GGZY/NEW_GGZY && nohup scrapyd >/dev/null 2>&1 &")
# 启动ggzy服务
os.system("cd /home/terry/i139/jxpython/ggzy/ggzy && nohup python main_ggzy.py >/dev/null 2>&1 &")
# 启动ggzy-requests服务
os.system("cd /home/terry/i139/jxpython/ggzy/ggzy/requestsAPI && nohup python main_ggzy_requests.py >/dev/null 2>&1 &")

# 启动mcf服务1
os.system("cd /home/terry/i139/mcf && nohup python hub_article.py >/dev/null 2>&1 &")
# 启动mcf服务2
os.system("cd /home/terry/i139/mcf && nohup python hub_run.py >/dev/null 2>&1 &")
# 启动elc服务
os.system("cd /home/terry/i139/jxpython/electric && nohup python main_electric.py >/dev/null 2>&1 &")