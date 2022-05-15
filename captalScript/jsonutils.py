import json
import sys
import re
import reutils
import keysutils

text = "[{'序号': '1', '标段': '标段A', '标包': '标包1', '归属区域': '海口东:世纪大桥-龙昆南-迎宾路-绕城高速-东线高速以东（含海甸岛）', '单位': '站', '投资估算（不含税）（万元）': '404.64'}, {'序号': '2', '标段': '标段A', '标包': '标包2', '归属区域': '海口西:世纪大桥-龙昆南-迎宾路-绕城高速-东线高速以西（不含海甸岛）', '单位': '站', '投资估算（不含税）（万元）': '352.27'}, {'序号': '3', '标段': '标段B', '标包': '标包1', '归属区域': '三亚东:G224国道-吉阳大道-迎宾路-及延长至海边以东、以及其他市县（陵水县、三沙市）', '单位': '站', '投资估算（不含税）（万元）': '292.76'}, {'序号': '4', '标段': '标段B', '标包': '标包2', '归属区域': '三亚西:G224国道-吉阳大道-迎宾路-及延长至海边 以西、以及其他市县（乐东、五指山、保亭）', '单位': '站', '投资估算（不含税）（万元）': '275.18'}, {'序号': '5', '标段': '标段C', '标包': '标包1', '归属区域': '东线高速沿途其他市县（文昌、定安、琼海、万宁）', '单位': '站', '投资估算（不含 税）（万元）': '231.20'}, {'序号': '6', '标段': '标段C', '标包': '标包2', '归属区域': '儋州等其他市县（澄迈、临高、屯昌、琼中、儋州、昌江、白沙、东方）', '单位': '站', '投资估算（不含税）（万元）': '210.24'}, {'序号': '合计', '投资估算（ 不含税）（万元）': '1766.29'}]"

from keysutils import keymap,process_rmb,process_discount,process_number,process_candidate

str_f2a = "(份额([1234567890一二三四五六七八九十]{1,}))\D{1,30}?(\d{1,12}\.?\d{0,2}?%)"
str_f2 = "(份额([1234567890一二三四五六七八九十]{1,}))\D{1,30}?(\d{1,12}\.?\d{0,6}?[元万亿])"
str_f3a = "(([1234567890一二三四五六七八九十]{1,})份额).{0,30}?(\d{1,12}\.?\d{0,2}?%)"
str_f3 = "(([1234567890一二三四五六七八九十]{1,})份额).{0,30}?(\d{1,12}\.?\d{0,6}?[元万亿])"
str_f8 = "份额[:： 为是]?(\d{1,3}%)"
#Terry modify from .{0，50} to .{0,20}
str_f1 = "(第([1234567890一二三四五六七八九十])).{0,30}?(\d{1,12}\.?\d{0,2}%)"
str_f4 = "(([1234567890一二三四五六七八九十]{1,})份额).*?(\d{1,12}\.?\d{0,2}?%)"
str_f5 = "份额分别为((\d{1,12}\.?\d{0,2} *?%[、。]){1,})"
str_f6 = "(\d{1,12}\.?\d{0,2}?%)"
str_f7 = "(第([1234567890一二三四五六七八九十])名).{0,30}?(\d{1,12}\.?\d{0,6})"
str_f6a = "([10]\.\d{1,4})"

KEYWORDS_B = "(标包|标段|采购包|包段|^包$)"

def cleanchar(text):
    while len(text) > 0 and text[len(text)-1] not in ['0','1','2','3','4','5','6','7','8','9','.']:
       text = text[0:len(text)-1]
    while len(text) > 0 and text[0] not in ['0','1','2','3','4','5','6','7','8','9','.']:
       text = text[1:]
    ret = reutils.getfloatstr(text)
    if ret is not None:
        return ret
    else:
        return 0

def seq_order_en(text):
    str1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seq = 0
    if len(text) == 1:
        pos = str1.find(text)
        if pos >= 0:
            seq = pos + 1
    return seq

def seq_order_cn(text):
    str1 = "一二三四五六七八九十"
    seq = 0
    if len(text) == 1:
        pos = str1.find(text)
        if pos >= 0:
            seq = pos + 1
    elif len(text) == 2:
        pos1 = str1.find(text[0]) + 1
        pos2 = str1.find(text[1]) + 1
        seq = pos1 + pos2
    elif len(text) == 3:
        pos1 = str1.find(text[0]) + 1
        pos2 = str1.find(text[1]) + 1
        pos3 = str1.find(text[2]) + 1
        seq = pos1 * pos2 + pos3
    return seq

def seq_order(text):
    seq = 0
    try:
        seq = int(text)
    except Exception as e:
        print(e)
        seq = seq_order_en(text)
        if seq == 0:
            seq = seq_order_cn(text)
    return seq

KEYWORDS_FENER = ['0','1','2','3','4','5','6','7','8','9','.','一','二','三','四','五','六','七','八','九','十','份','额','第','名','、','%']
def fenervalidate(text):
    if len(text) == 0:
        return False
    cc = 0
    for t in text:
        if t in KEYWORDS_FENER:
            cc += 1 
    return (cc >= 3)

def process_fener2(text):
          objs = []
          m3 = re.findall(str_f6, text)
          print("f6:%s" % m3)
          if len(m3) == 0:
            m3 = re.findall(str_f6a, text)
            print("f6a:%s" % m3)
          i = 1
          for m in m3:
            obj = {}
            obj['order'] = i
            obj['share'] = process_discount(m)
            objs.append(obj)
            i += 1
          return objs

def process_fener(text):
    #print(text)
    objs = []
    numtype='f'
    m1 = re.findall(str_f1, text)
    if len(m1) == 0:
        m1 = re.findall(str_f2a, text)
        if len(m1) > 0:
            #print("f2a:%s" % m1)
            if m1[0][1].endswith('10') and m1[0][2].startswith('0'):
                m1 = []
    if len(m1) == 0:
        m1 = re.findall(str_f3a, text)
        #print("f3a:%s" % m1)
    if len(m1) == 0:
      m1 = re.findall(str_f2, text)
      #print("f2:%s" % m1)
      if len(m1) == 0:
        m1 = re.findall(str_f3, text)
        #print("f3:%s" % m1)
      if len(m1) > 0:
        numtype = 'm'
    if len(m1) == 0:
        m1 = re.findall(str_f4, text)
        #print("f4:%s" % m1)
    if len(m1) == 0:
        m1 = re.findall(str_f7, text)
        #print("f7:%s" % m1)
        if len(m1) > 0:
          numtype = 'm'
    if len(m1) == 0:
        m1 = re.findall(str_f8, text)
        #print("f8:%s" % m1)
        if len(m1) > 0:
            m1 = [('1','1',m1[0])]

    if len(m1) == 0:
        m2 = re.findall(str_f5, text)
        #print("f5:%s" % m2)
        if len(m2):
          m3 = re.findall(str_f6, text)
          #print("f6:%s" % m3)
          i = 1
          for m in m3:
            obj = {}
            obj['order'] = i
            obj['share'] = process_discount(m)#m
            objs.append(obj)
            i += 1
          return objs

    if len(m1) > 0:
        print(m1)
        for biao, fene, qian in m1:
            obj = {}
            obj['name'] = biao
            obj['order'] = seq_order(fene)
            vv = None
            if numtype == 'f':
              vv = process_discount(qian)
              if vv:
                obj['share'] = vv
              else:
                #vv = process_number(qian)
                obj['share'] = qian
            else:
              #skip the wrong format
              if qian.endswith('.'):
                  continue
              obj['budget'] = process_rmb(qian)
            objs.append(obj)
    return objs

def removekey(objs, key):
    for obj in objs:
        obj.pop(key,None)

def ssobj(obj,pkg_name):
            objp = {}
            objp[pkg_name] = obj[pkg_name]
            objp['kshares'] = []
            objp['kshares'].append(obj)
            return objp

def llobj(obj,pkg_name):
            objp = {}
            objp[pkg_name] = obj[pkg_name]
            objp['mshares'] = []
            objp['mshares'].append(obj)
            """
            if 'budget' in obj.keys():
              objp['budget'] = obj['budget']
            else:
              objp['budget'] = 0
            """
            objp['budget'] = 0
            return objp

def removeduplicate(obj):
    toremove = []
    if 'duplicate' not in obj.keys():
        return []
    for key in obj.keys():
        if not key.startswith('budget'):
            continue
        if obj['duplicate'].find(key + ".") >= 0:
            toremove.append(key)
    for item in toremove:
        obj.pop(item)
    return toremove

def checkshares(obj):
    cc = 0
    keys = obj.keys()
    for key in keys:
        if key.startswith('share'):
            cc += 1 
    return (cc > 1)

str_vn = '^\d{1,}家?$'
def validatenum(text):
    text = text.strip()
    m1 = re.findall(str_vn, text)
    if len(m1) > 0:
        return True
    return False

def postprocess_seq(objs):
    print("postprocess_seq")
    ret = []
    for obj in objs:
        if 'backup' in obj.keys() and len(obj['backup']) >= 2 and obj['backup'][0:2] in ['总计','合计','小计']:
            continue 
        if 'sequence' in obj.keys() and len(obj['sequence']) >= 2 and obj['sequence'][0:2] in ['总计','合计','小计']:
            continue
        if 'order' in obj.keys() and len(obj['order']) >= 2 and obj['order'][0:2] in ['总计','合计','小计']:
            continue
        ret.append(obj)
        cc = removeduplicate(obj)
        if len(cc) == 0:
            continue
        c = cc[len(cc)-1] 
        if 'budget' == c:
          if 'budget2' in obj.keys():
            obj['budget'] = obj.pop('budget2')
        elif 'budget2' == c:
            pass
    return ret

def postprocess_obj(obj):
    if 'budget' in obj.keys():
        return
    if 'budget2' in obj.keys():
        obj['budget'] = obj.pop('budget2')
    if 'budget3' in obj.keys():
        obj['budget2'] = obj.pop('budget3')
    return

def checkduplicate(objp, obj, key, newkey):
        if key not in obj.keys():
            print("no key:%s" % key)
            return False
        if 'duplicate' not in obj.keys():
            print("no duplicate:%s" % (key))
            return False
        if obj['duplicate'].find(key + '.') < 0:
            print("no duplicate:%s %s" % (key,obj['duplicate']))
            return False
        keys = obj['duplicate'].split('.')
        counts = obj['duplicate_counts'].split('.')
        index = 0
        for ikey in keys:
            if ikey == key:
                break
            index += 1
        if index == len(keys) or counts[index] == '':
            print("no duplicate:%s" % key)
            return False
        icount = int(counts[index])
        if 'mergecount' not in objp.keys() and icount > 0:
            objp['mergecount'] = icount
        if icount > 0 and icount == objp['mergecount']:
            objp[newkey] = obj.pop(key)
            return True
        else:
            return False

def postprocess_seq_json(objs,pkg_name='sequence',merge = None):
    objp = None
    newobjs = []
    lastobj = None
    for obj in objs:
        if pkg_name not in obj.keys():
            return objs
        if pkg_name in obj.keys() and len(obj[pkg_name]) >= 2 and obj[pkg_name][0:2] in ['总计','合计','小计']:
            continue
        if 'duplicate' not in obj.keys():
            print("no need to postprocess seq:%s" % (pkg_name))
            newobjs.append(obj)
        elif obj['duplicate'].find(pkg_name + '.') < 0:
            print("no need to postprocess seq:%s %s" % (pkg_name,obj['duplicate']))
            newobjs.append(obj)
            continue
        package = obj[pkg_name]
        if objp is None:
            objp = ssobj(obj, pkg_name)
            newobjs.append(objp)
        elif package == lastobj:
            objp['kshares'].append(obj)
        else:
            objp = ssobj(obj, pkg_name)
            newobjs.append(objp)

        checkduplicate(objp, obj, 'budget','budget')
        checkduplicate(objp, obj, 'budget2','budget')
        checkduplicate(objp, obj, 'budget3','budget')
        checkduplicate(objp, obj, 'share','share')
        checkduplicate(objp, obj, 'share2','share')
        checkduplicate(objp, obj, 'share3','share')
        #postprocess_obj(obj)
        lastobj = package
    return newobjs
 
def postprocess_json(objs,pkg_name='package',merge = None):
    objp = None
    newobjs = []
    lastobj = None
    index = 0
    sumobj = None
    for obj in objs:
        index += 1
        if pkg_name not in obj.keys():
            print(obj, index)
            if 'package' == pkg_name:
                if index == 1:
                    return postprocess_seq_json(objs)
                elif index > 1:
                    continue
            else:
                return objs 
        if len(obj[pkg_name]) >= 2:
          if obj[pkg_name][0:2] in ['总计','合计','小计']:
            print("skip the summary:%s" % obj)
            #newobjs.append(obj)
            sumobj = obj
            continue
          elif len(obj[pkg_name]) >= 10 and len(objs) >= 2 and index == len(objs):
            print("skip the wrong package:%s" % obj[pkg_name])
            continue
          elif obj[pkg_name] in ['标段','标包','子项','采购包','包段']:
            print("skip wrong package:%s l2" % obj[pkg_name])
            continue
        """
        if 'duplicate' not in obj.keys():
            print("no need to postprocess:%s %s" % (pkg_name,obj))
            newobjs.append(obj)
            continue
        elif obj['duplicate'].find(pkg_name + '.') < 0:
            print("no need to postprocess:%s %s" % (pkg_name,obj['duplicate']))
            newobjs.append(obj)
            continue
        """
        package = obj[pkg_name]
        if objp is None:
            objp = llobj(obj, pkg_name)
        elif package == lastobj:
            objp['mshares'].append(obj)
        else:
            if len(objp['mshares']) > 1:
                newobjs.append(objp)
            elif len(objp['mshares']) == 1:
                kobj = objp['mshares'][0]
                kobj[pkg_name] = objp[pkg_name]
                newobjs.append(kobj)
            objp = llobj(obj, pkg_name)

        oshare = []
        if 'share' in obj.keys() and isinstance(obj['share'], str):
            oshare = process_fener(obj['share'])
        if len(oshare) > 1:
            obj['mshares'] = oshare
        elif checkshares(obj):
            shares = []
            for key,val in obj.items():
                if key.startswith('share'):
                    nobj = {}
                    nobj['share'] = val
                    shares.append(nobj)
            obj['mshares'] = shares
            print("has multi shares:%s" % shares)
            if merge:
                obj['merge'] = True
                dkeys = merge.split('.')
                budgets = []
                for dkey in dkeys:
                  if dkey.startswith('budget') and dkey in obj.keys():
                    budgets.append(obj[dkey])
                i = 0
                for share in shares:
                    if len(budgets) == i:
                        print("no enough budgets:%s, for shares:%s" % (budgets,shares))
                        break
                    share['budget'] = budgets[i]
                    i += 1
        elif 'duplicate_counts' in obj.keys():
          checkduplicate(objp, obj, 'budget','budget')
          checkduplicate(objp, obj, 'budget2','budget')
          checkduplicate(objp, obj, 'budget3','budget')
        else:
            #removeduplicate(obj)
            """
            if 'budget' in obj.keys() and 'budget2' in obj.keys():
                vv = obj['budget'] if obj['budget2'] > obj['budget'] else obj['budget2']
                #objp['budget'] += vv
                if 'duplicate' not in obj.keys():
                    objp['budget'] += vv
                elif obj['duplicate'].find('budget.') >= 0:
                    objp['budget'] = vv

                if vv == obj['budget']:
                    obj.pop('budget2')
                else:
                    obj.pop('budget')
            elif 'budget' in obj.keys():
                if 'duplicate' not in obj.keys():
                    objp['budget'] += float(obj['budget'])
                elif obj['duplicate'].find('budget') >= 0:
                    objp['budget'] = float(obj['budget'])
                    obj.pop('budget')
            """
        obj.pop(pkg_name)
        lastobj = package
    if objp is not None:
        if len(objp['mshares']) > 1:
            newobjs.append(objp)
        elif len(objp['mshares']) == 1:
            kobj = objp['mshares'][0]
            kobj[pkg_name] = objp[pkg_name]
            newobjs.append(kobj)
    if sumobj is not  None:
        newobjs.append(sumobj)

    if pkg_name != 'package2' and 'package2' in obj.keys():
      for obj in newobjs:
        if 'mshares' in obj.keys():
          obj['mshares'] = postprocess_json(obj['mshares'],'package2',merge)
    if pkg_name != 'sequence':
      for obj in newobjs:
        if 'mshares' in obj.keys() and 'merge' not in obj.keys():
          obj['mshares'] = postprocess_seq_json(obj['mshares'],'sequence',merge)
    #中国移动四川公司2019-2021年全省管理用房配套中央空调维保维修服务项目
    for obj in newobjs:
        if 'mshares' not in obj.keys():
            continue
        subobjs = obj['mshares']
        jj = {}
        hasshares = False
        haspackage2 = False
        hasbudget = False
        hascandidate = False
        for sobj in subobjs:
            postprocess_obj(sobj)
            print(sobj)
            for key,value in sobj.items():
                print(key,value)
                if key.startswith('candidate'):
                    hascandidate = True
                if key.startswith('package2'):
                    haspackage2 = True
                if key.startswith('share') and value is not None:
                     #only one bid
                     if value >= 1.0:
                         continue 
                     hasshares = True
                     if key in jj.keys():
                         jj[key] += value
                     else:
                         jj[key] = value
                #TODO
                if key.startswith('budget') and value is not None:
                    hasbudget = True
                if 'duplicate' in sobj.keys():
                    if sobj['duplicate'].find(key+'.') >= 0:
                        #TODO
                        pass
                        #obj[key] = value
                    else:
                        if key.startswith('budget'):
                            hasbudget = True
        for key in jj.keys():
            if jj[key] < 0.99:
                print(key)
                removekey(subobjs,key) 
        print(jj) 
        if not hasshares and not haspackage2 and not hasbudget and not hascandidate and len(obj['mshares']) > 1:
            print('no shares at all')
            obj['kshares'] = obj.pop('mshares')
    return newobjs

def checkvalue0(text):
    text = text.strip()
    if text == '' or text[0] in ['/','-','备','后','侯']:
        return True
    return False

def process_json(objs):
    newobjs = []
    for obj in objs:
        newobj = {}
        keys = []
        for key in obj.keys():
            keys.append(key)
        newkeys = keymap(keys)
        print(keys,newkeys)
        if 'duplicate' in obj.keys():
            i = 0
            for key in keys:
                obj['duplicate'] = obj['duplicate'].replace(key + '.',newkeys[i] + '.')
                i += 1
        j = 0
        #if a cn key could be mapped to two en keys, then copy it here.
        for key in keys:
            #newkey = keysutils.getsecondkey(key,newkeys[j-1])
            nkeys = keysutils.getkeys(key)
            for newkey in nkeys:
              if newkey is not None and newkey not in newkeys:
                if newkey in ['budget','discount','share']:
                    newkeys.append(newkey)
                    obj[key + str(j)] = obj[key]
                    print("adding new key:%s with value:%s" % (newkey,obj[key+str(j)])) 
            j += 1
        j = 0
        for key,value in obj.items():
            newkey = newkeys[j] 
            #print(key,value) 
            j += 1
            if not newkey.startswith('budget'):
                if newkey.startswith('product'):
                    if 'package' not in newkeys:
                        if len(re.findall(KEYWORDS_B,key)) > 0:
                            print("product is a package:%s" % value)
                            newkey = 'package'
                if newkey.startswith('sequence'):
                    if value.find("%") >= 0:
                        print("key from seq to share:%s" % value)
                        newkey = 'share'
                if newkey.startswith('discount'):
                    value = process_discount(value)
                    #例如4.5折被识别成0.045
                    if value is None:
                        value = 1
                    if value < 0.1:
                        value = value * 10
                elif newkey.startswith('share'):
                    #ignore the wrong share format, as 份额包含的工程
                    if not fenervalidate(value):
                        newobj[key] = value
                        continue
                    sobjs = process_fener(value)
                    if len(sobjs) == 0:
                        sobjs = process_fener2(value)
                    if len(sobjs) > 1:
                        newobj['mshares'] = sobjs
                        continue
                    elif len(sobjs) == 1:
                        print("BBINGGGGGGGGGGGGGGGGGGGGG")
                        #value = sobjs[0]['share']
                    elif checkvalue0(value):
                        value = '0' 
                    else:
                        print("no shares in share:%s" % value)
                        continue
                    value = process_discount(value)
                    #金额被误处理成份额
                    if value is not None and value > 1.0:
                        value = value * 100
                        if key.find('万元') >= 0:
                            value = float(value) * 10000
                        elif key.find('亿元') >= 0:
                            value = float(value) * 100000000
                        elif float(value) <= 10000:
                            value = float(value) * 10000
                elif newkey.startswith('number'):
                    value = process_number(value)
                elif newkey.startswith('candidate'):
                    ovalue = value
                    value,value_type = process_candidate(value)
                    newobj['bid'] = value_type
                    if value == '':
                        newobj['backup'] = ovalue
                elif newkey.startswith('package'):
                    value = value.replace(" ","").replace("\xa0","")
                newobj[newkey] = value
                continue
            if value == '':
                continue
            value = value.replace(",","").replace("\xa0",'').replace("/",'').replace(" ",'').replace("．",'.').replace("，",'').replace("；",'')
            print("budget:%s" % value)
            if value == '':
                value = 0
            elif value.find('万') >= 0 or value.find('亿') >=0 or value.find('元') >=0:
                #print(value)
                value = process_rmb(value)
            elif value[0] not in ['1','2','3','4','5','6','7','8','9','0','¥']:
                print(value)
                value = 0
            elif key.find('万元') >= 0:
                value = cleanchar(value)
                value = float(value) * 10000
            elif key.find('亿元') >= 0:
                value = cleanchar(value)
                value = float(value) * 100000000
            elif key.find('元') >= 0:
                value = cleanchar(value)
                value = float(value)
            else:
              try:
                print(value)
                value = cleanchar(value)
                value = float(value)
                if value < 10000:
                  value = float(value) * 10000
                print(value)
              except Exception as e:
                print(e)
                print(value)
                value = 0
            newobj[newkey] = value 
        newobjs.append(newobj)
    #cnewobjs = postprocess_json(newobjs)
    #print(cnewobjs)
    print(newobjs)
    return newobjs

def load_json(text):
    text = text.replace("\'","\"")
    objs = json.loads(text)
    return process_json(objs)

if __name__ == "__main__":
    fname = sys.argv[1]
    fp = open(fname,'r')
    text = fp.read()
    fp.close()
    objs = load_json(text)
    print(objs)
