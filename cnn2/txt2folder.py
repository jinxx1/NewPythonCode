import sys
import os

cate1 = {}
cate_count = 0
cate_values = 0
label_names = []
def process_line(line,rootpath):
    global cate1,cate_count,cate_values,label_names
    tabs = line.split('\t')
    if len(tabs) < 3:
        return
    cate1_name = tabs[2].replace('\n','')
    title = tabs[0]
    if cate1_name == '0' or cate1_name=='' or cate1_name is None:
        return
    if cate1_name not in cate1.keys():
        print('"' + cate1_name + '",')
        label_names.append(cate1_name)
        cate1[cate1_name] = cate_values
        catepath = os.path.join(rootpath, "%d" % cate_values)
        os.system("mkdir %s" % catepath)
        cate_values = cate_values + 1
    cate1_value = cate1[cate1_name]
    f2path = os.path.join(rootpath, "%d" % cate1_value)
    f2path = os.path.join(f2path, "%d.txt" % cate_count)
    f2 = open(f2path, 'w')
    f2.write(title)
    f2.close()
    cate_count = cate_count + 1
    #print("cates:%d" % cate_count)

def txt2folder(src,dst):
    print("txt2folder from %s to %s" % (src,dst))
    fp = open(src, 'r')
    line = fp.readline()
    while line !='':
        line = fp.readline()
        process_line(line,dst)
    fp.close()
    print("cates:%d" % cate_values)
    fp = open("labelnames.py", 'w')
    fp.write("label_names=" + str(label_names))
    fp.close()
    return cate_values

if __name__ == "__main__":
    filepath = sys.argv[1]
    rootpath = sys.argv[2]
    txt2folder(filepath, rootpath)
