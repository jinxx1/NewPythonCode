import sys
import db2mongo

def addlink(line,sp = ','):
    text = ''
    items = line.split(sp)
    #print(items)
    title = items[0]
    issueDate = items[3]
    if issueDate == "None":
        issueDate = "2019-07-01"
    items[len(items)-1] = db2mongo.geturl(title,issueDate)
    for item in items:
        text += item + sp
    return text + '\n'
    
def linkfile(filepath,sp):
    fp = open(filepath, "r")
    lines = fp.readlines()
    fp.close()
    fp = open(filepath, "w")
    i = 0
    for line in lines:
        if i == 0:
            fp.write(line)
        elif len(line) > 1:
            line = line[:len(line) - 1]
            line = addlink(line,sp)
            fp.write(line)
        i += 1
    fp.close()

if __name__ == "__main__":
    filepath = sys.argv[1]
    sp = sys.argv[2]
    linkfile(filepath,sp)
