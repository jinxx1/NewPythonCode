# -*- coding: utf-8 -*-
import sys,os,threading,json,subprocess,io,pprint
from time import ctime,sleep

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
    return idNum

if __name__ == '__main__':
    idNum = cancel_list()
    cancelWord = "curl http://localhost:6800/cancel.json -d project=NEW_GGZY -d job={}"
    for xx in idNum:
        proc = subprocess.Popen(cancelWord.format(xx), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
        proc.wait()
        stream_stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8')
        str_stdout = str(stream_stdout.read())
        print(str_stdout)
