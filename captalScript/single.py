import os
import json
import sys
import ztbutils
import os
import time
import datetime

DT_N = datetime.datetime(2019,11,11)

def getdatetime(ModifiedTime):
    y=time.strftime('%Y', ModifiedTime) 
    m=time.strftime('%m', ModifiedTime) 
    d=time.strftime('%d', ModifiedTime) 
    H=time.strftime('%H', ModifiedTime) 
    M=time.strftime('%M', ModifiedTime) 
    d2 = datetime.datetime(int(y),int(m),int(d),int(H),int(M))
    return d2

def loaddir(dir,ndir):
    print("corelate:%s %s" % (dir,ndir))
    vv = []
    objs = []
    acounts = 0
    mcounts = 0
    fp = open(ndir, 'w') 
    for root, dirs, files in os.walk(dir, True):
        for name in files:
            if not name.endswith('.txt'):
                continue
            acounts += 1
            fpath = os.path.join(root, name)
            mt = getdatetime(time.localtime(os.stat(fpath).st_mtime))
            if mt >= DT_N:
                print(fpath)
                print(mt)
                mcounts += 1
                fp.write(name[0:len(name) - 4] + '\n')
            """
            obj = ztbutils.readjson(fpath)
            if obj['last_bid_time'] is None:
                print(obj['project_name'])
            fp.write(obj['project_name'] + '\n')
            """
    fp.close()
    print(acounts, mcounts)

if __name__ == "__main__":
    dir = sys.argv[1]
    ndir = sys.argv[2]
    loaddir(dir,ndir)
