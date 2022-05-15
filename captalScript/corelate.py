import os
import json
import sys
import ztbutils

def loaddir(dir,ndir):
    print("corelate:%s %s" % (dir,ndir))
    vv = []
    objs = []
    for root, dirs, files in os.walk(dir, True):
        for name in files:
            if not name.endswith('.txt'):
                continue
            fpath = os.path.join(root, name)
            obj = ztbutils.readjson(fpath)
            project_name = ztbutils.process_biao(obj['title'])
            if project_name != obj['project_name']:
                print(name)
                obj['project_name'] = project_name
                newfpath = os.path.join(ndir, name)
                ztbutils.dump2json(newfpath,obj)

if __name__ == "__main__":
    dir = sys.argv[1]
    ndir = sys.argv[2]
    loaddir(dir,ndir)
