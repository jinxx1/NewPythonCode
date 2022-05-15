# -*- coding: utf-8 -*-
import requests,time,json,smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendEmail(dict):
    import requests, time, json, smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    mail_host = 'smtp.exmail.qq.com'
    mail_user = 'umservice@uxuepai.net'
    mail_pass = 'Um20170927'
    mail_port = 465
    sender = mail_user
    receivers = ['jinxx1@163.com','wtg2022@163.com']
    # receivers = ['jinxx1@163.com']
    message = MIMEText(dict['body'],'plain','utf-8')
    # message['From'] = Header(sender,'utf-8')
    message['To'] = Header(';'.join(receivers),'utf-8')
    message['Subject'] = Header(dict['title'],'utf-8')


    smtpObj = smtplib.SMTP_SSL(mail_host,mail_port)
    smtpObj.ehlo()
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender,receivers,message.as_string())
    smtpObj.quit()
    print('succes')

def getdate():
    today_time = time.strftime("%Y-%m-%d",time.localtime())
    url = 'http://ztb.uxuepai.net:8035/pc/api/info/source/getInfoPurchaseSourceNumByDate?day={}&isRawInfo=true'.format(today_time)
    brow = requests.get(url=url)
    timedate = json.loads(brow.text)['data']
    listAll = []
    riqiList = []
    nameList = []
    for i in timedate:
        dictTime = {}
        time_local = time.localtime(i['date']//1000)
        dictTime['time_tabledate'] = str(time_local.tm_year) + '-' + str(time_local.tm_mon) + '-' + str(time_local.tm_mday)




        dictTime['num'] = i['num']
        dictTime['name'] = i['name']
        dictTime['date'] = i['date']
        if time_local.tm_wday == 6 or time_local.tm_wday == 5:
            continue
        else:
            if time_local.tm_wday == 0:
                dictTime['datawday'] = '星期一'
            elif time_local.tm_wday == 1:
                dictTime['datawday'] = '星期二'
            elif time_local.tm_wday == 2:
                dictTime['datawday'] = '星期三'
            elif time_local.tm_wday == 3:
                dictTime['datawday'] = '星期四'
            elif time_local.tm_wday == 4:
                dictTime['datawday'] = '星期五'

        listAll.append(dictTime)
        if dictTime['time_tabledate'] not in riqiList:
            riqiList.append(dictTime['time_tabledate'])
        nameList.append(dictTime['name'])




    dict = {}
    for key in nameList:
        dict[key] = dict.get(key,0)+1

    chayi = []
    for n in dict.keys():
        Num = len(riqiList) - dict[n]
        if Num> 2:
            dict2={}
            dict2['name'] = n
            dict2['chayi'] = Num
            chayi.append(dict2)

    dictWord= {}
    llist = []
    if chayi:
        sub = '以下数据，截止到昨天23:59分\n\n'
        for num,i in enumerate(chayi):
            dword="网站：{}。{}天没有数据\n".format(i['name'],i['chayi'])
            llist.append(dword)

        dictWord['body'] = sub + ''.join(llist) + '\n以上数据不包括周六、周日'
        dictWord['title'] = 'uXuePai监控提示：截止昨天,有{}个网站数据为空'.format(len(chayi))
        sendEmail(dictWord)

if __name__ =="__main__":
    ddict ={}
    ddict['body'] = '测试邮件——正文。测试邮件——正文。测试邮件——正文。测试邮件——正文。测试邮件——正文。'
    ddict['title'] = '入库接口错误栈——测试邮件_标题'
    sendEmail(ddict)

    exit()
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(getdate,'cron',day_of_week = '1-5',hour = 6,minute=1)
    sched.start()














