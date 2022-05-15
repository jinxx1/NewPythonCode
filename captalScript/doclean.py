import sys
import os

def cleanfile(filename, dirpath = ''):
    fp = open(filename,"r")
    fpw = open("pp.txt", 'w')
    lines = fp.readlines()
    for line in lines:
        pos = line.find(".txt")
        if pos >= 0:
            filepath = line[0:pos + 4]
            title = filepath[2:pos]
            #os.system("rm %s/%s*" % (dirpath,title))
            fpw.write(title)
            fpw.write("\n")
    fpw.close()
    fp.close()

if __name__ == "__main__":
    filename = sys.argv[1]
    dirpath = sys.argv[2]
    cleanfile(filename, dirpath)
