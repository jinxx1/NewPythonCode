# -*- coding: utf-8 -*-
import sys,os,threading,json,subprocess,io,pprint
from time import ctime,sleep


def get_pengding_and_runing_spiderName_func():
    cmdscrapylist = os.popen('curl http://localhost:6800/listjobs.json?project=NEW_GGZY | python -m json.tool')
    dictjson = json.loads(cmdscrapylist.read())
    pending_and_runing_List = dictjson['pending'] + dictjson['running']
    pendAndrun_spiderName_List = []
    for pendAndrun_spiderDict in pending_and_runing_List:
        pendAndrun_spiderName_List.append(pendAndrun_spiderDict['spider'])
    return pendAndrun_spiderName_List

def scrapy_D_list_func():
    CMDword = "curl http://localhost:6800/listspiders.json?project=NEW_GGZY"

    proc = subprocess.Popen(CMDword,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=-1)
    proc.wait()
    stream_stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8')
    str_stdout = str(stream_stdout.read())
    scrapy_D_List = json.loads(str_stdout)
    return scrapy_D_List['spiders']

def re_runSpiders(spiderNameList):
    for name in spiderNameList:
        CmdWord = "curl http://localhost:6800/schedule.json -d project=NEW_GGZY -d spider={}"
        os.system(CmdWord.format(name))
        print('爬虫{}，已经重新开启'.format(name))


def cancel_list():
    cmdscrapylist = os.popen('curl http://localhost:6800/listjobs.json?project=NEW_GGZY | python -m json.tool')
    dictjson = json.loads(cmdscrapylist.read())
    pendlist = dictjson['pending']
    runinglist = dictjson['running']
    idNum = []
    for i in pendlist:
        idNum.append(i['id'])
    for n in runinglist:
        idNum.append(n['id'])

    cancelWord = "curl http://localhost:6800/cancel.json -d project=NEW_GGZY -d job={}"
    for xx in idNum:
        proc = subprocess.Popen(cancelWord.format(xx), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
        proc.wait()
        stream_stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8')
        str_stdout = str(stream_stdout.read())
        print(str_stdout)

if __name__ == '__main__':
    sleepSec = 3600
    while True:
        sleep(sleepSec*2)
        pendAndrun_spiderName_List = get_pengding_and_runing_spiderName_func()
        scrapy_D_list = scrapy_D_list_func()
        if len(pendAndrun_spiderName_List) != len(scrapy_D_list):
            finished_SpiderNames = [y for y in scrapy_D_list if y not in pendAndrun_spiderName_List]
            re_runSpiders(finished_SpiderNames)
        sleep(sleepSec*2)
        for i in range(6):
            cancel_list()
            sleep(10)


