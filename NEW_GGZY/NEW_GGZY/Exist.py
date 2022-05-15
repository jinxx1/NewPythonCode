import requests,json


import datetime,time,logging

# from ggzy.redis_dup import BloomFilter
# bl = BloomFilter('uxue:url')


def urlIsExist(urllist):
    posturlapi = 'http://183.6.136.70:8035/pc/api/caijiApi/urlIsExist'
    # posturlapi = 'https://umxh.xue22222222222222you.cn/pc/api/caijiApi/urlIsExist'

    str_c = json.dumps(urllist)
    dataApi = {"urlListJson": str_c}

    try:
        a = requests.post(url=posturlapi,data=dataApi)
        jsonT = json.loads(a.text)
        return jsonT['data']
    except:

        print('链接筛选api--有故障，等待3秒后，重新发送请求')
        time.sleep(3)
        urlIsExist(urllist)

def save_api(dict1):
    import requests
    try:
        a = requests.post(url='http://183.6.136.70:8035/pc/api/caijiApi/save', data=dict1)
        return a
    except Exception as f:
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header
        aa = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ddict = {}
        ddict['title'] = '旧爬虫入库API出现问题---' + aa
        ddict['body'] = '发生时间为：{datetime}\n错误栈信息为：、\n{f}\n'.format(datetime=aa,f=f)

        mail_host = 'smtp.exmail.qq.com'
        mail_user = 'umservice@uxuepai.net'
        mail_pass = 'Um20170927'
        mail_port = 465
        sender = mail_user
        receivers = ['jinxx1@163.com', 'wtg2022@163.com']
        message = MIMEText(ddict['body'], 'plain', 'utf-8')
        message['To'] = Header(';'.join(receivers), 'utf-8')
        message['Subject'] = Header(ddict['title'], 'utf-8')
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.ehlo()
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()

        # time.sleep(3)
        # save_api(dict1)




def timeReMark(timtext):
    if not timtext:
        timtext = "2000-01-01 00:00:00"
    timetext=timtext.strip()
    timeTrue = ''
    timeWord1 =timetext.split(' ')
    try:
        time1 = timeWord1[1].split(':')
    except IndexError:
        timeTrue = timeWord1[0] + " 00:00:00"
    if not timeTrue:
        if len(time1) == 1:
            timeTrue = timeWord1[0] + ' ' + time1[0] + ":00:00"
        elif len(time1) == 2:
            timeTrue = timeWord1[0] + ' ' + time1[0] + ':' + time1[1] + ":00"
        elif len(time1) == 3:
            timeTrue = timeWord1[0] + ' ' + time1[0] + ':' + time1[1] + ':' + time1[2][0:2]
        else:
            timeTrue = timeWord1[0] + ' ' + time1[0] + ':' + time1[1] + ':' + time1[2][0:2]
    return timeTrue



if __name__=="__main__":
    a = ['aaaaaa']

    # print(urlIsExist(a))
    # print('******************************')
