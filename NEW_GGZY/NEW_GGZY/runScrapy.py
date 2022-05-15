# -*- coding: utf-8 -*-
import sys,os,threading,json,subprocess,io,pprint
from time import ctime,sleep

def scrapy_List_func():
    cmd_scrapy_list = os.popen('scrapy list')
    scrapy_List_temp = cmd_scrapy_list.read().split('\n')
    scrapy_List = [x for x in scrapy_List_temp if x]
    return scrapy_List

def scrapy_D_list_func():
    CMDword = r"curl http://localhost:6800/listspiders.json?project=NEW_GGZY"
    proc = subprocess.Popen(CMDword,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=-1)
    proc.wait()
    stream_stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8')
    str_stdout = str(stream_stdout.read())
    scrapy_D_List = json.loads(str_stdout)
    return scrapy_D_List['spiders']

def inputSpiderName(scrapy_D_list):
    spiderNameInput = input('请输入需要运行的某一个爬虫名称，all为所有爬虫，watch查看可以运行爬虫名称，quit退出程序：').strip()
    inputWord = str(spiderNameInput).lower()

    if inputWord == 'all':
        print('您输入的是all')
        return inputWord

    elif inputWord == 'watch':
        pprint.pprint(scrapy_D_list)
        return 0

    elif inputWord == 'quit':
        print('程序退出，再见。')
        return inputWord

    elif inputWord in scrapy_D_list:
        print('您输入的爬虫名称为：',inputWord)
        return inputWord

    else:
        print('您输入有误，请重新输入。您输入的信息为：',spiderNameInput)
        return 0

def find_newSpider(scrapy_List,scrapy_D_list):
    NewSpiderNameList = [y for y in scrapy_List if y not in scrapy_D_list]
    print('发现有{}个新爬虫文件，新爬虫名称为：{}'.format(len(NewSpiderNameList),NewSpiderNameList))
    # print('发现有{}个新爬虫文件，新爬虫名称为：{}'.format(len(NewSpiderNameList)),NewSpiderNameList)
    inputWord = input('若想所有新爬虫生效，请输入yes').strip().lower()
    if inputWord == 'yes':
        print('正在更新爬虫文件.....')
        updateSpiders = os.popen("scrapyd-deploy newggzy -p NEW_GGZY")
        print(updateSpiders.read())
        print('爬虫文件更新完毕，请重新启动本脚本')
        return None

    else:
        print('您没有输入yes，本脚本将以旧爬虫库为启动对象。')
        return 1

def runSpiders(scrapy_D_list):
    CmdWord = "curl http://localhost:6800/schedule.json -d project=NEW_GGZY -d spider={}"
    while True:
        spiderName = inputSpiderName(scrapy_D_list)
        if spiderName != 0:
            if spiderName == 'all':
                for i, name in enumerate(scrapy_D_list):
                    # if i > 2:
                    #     break
                    os.system(CmdWord.format(name))
            elif spiderName == 'quit':
                return None
            else:
                os.system(CmdWord.format(spiderName))
            break

    print('爬虫已经开启')
    print('本目录还有两个文件脚本，分别是cancel_spiders.py和supervisory.py。可直接运行，没有任何传参')
    print('cancel_spiders.py：是用来终止爬虫进程。运行后，终止全部正在运行中runing和排队中pending的所有爬虫')
    print('supervisory.py：是用来自动启动已经结束的爬虫。时间间隔为1小时。使用的while死循环，该进程会一直存在。')


if __name__ == '__main__':
    print('启动本脚本前，请确保localhost:6800服务已开启。若没有开启，请新开一个终端，输入命令scrapyd即可')
    print('项目名：NEW_GGZY，用以保证各标讯网站日常更新')
    scrapy_List = scrapy_List_func()
    scrapy_D_list = scrapy_D_list_func()
    if len(scrapy_List) == len(scrapy_D_list):
        print('没有发现有新爬虫文件，可以继续进行')
        runSpiders(scrapy_D_list)
    else:
        update_newSpdier_yes_or_other = find_newSpider(scrapy_List,scrapy_D_list)
        if update_newSpdier_yes_or_other == 1:
            runSpiders(scrapy_D_list)
