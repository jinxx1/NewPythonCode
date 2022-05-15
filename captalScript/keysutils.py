import re
import logging
import nerutils

#strs = ['限定','中标候选人数量|中选候选人数量','(中标数量|中标人数量|候选人数量|中选人数量|中选数量|(中选|中标).*家数)','区域|地域|地市|本地网|地点','建设规模|标包名称|采购包名称|选包名称|标段名称|产品名称|标包介绍|标段介绍|标包内容|标段内容','(费用|金额|规模|投资|工程费|上限|估算|概算|预算|总价|报价|施工费|(小计.{0,}元)|（元）|万元)','包序|服务包|标包号|标段号|标段|标包|^包$|采购包|比选包|选包|子项|分项','份额序号|((中选人|候选人)(排名|名次))|^份额$','折扣','申请单位|申请人|应答人|候选人|单位名称|服务商名称|公司名称|中选人|供应商|投标人|入围(服务商|单位|厂家|公司)','成交份额|比例|占比|分配比例|份额分配|预估份额|中标份额|中选份额|份额划分','序号|排名|名次','负责人','证书编号','工期','估算数量|需求数量|数量','标段数量|标包数量']
#keymaps = ['limit','can_counts','bid_counts','location','product','budget','package','sequence','discount','candidate','share','order','projectmanager','pm_license','period','pt_counts','pkg_counts']
strs = ['(费用|金额|规模|投资|工程费|上限|估算|概算|预算|总价|报价|施工费|(小计.{0,}元)|（元）|万元)','份额序号|((中选人|候选人)(排名|名次))|^份额$','折扣','^份额|成交份额|比例|占比|分配比例|份额分配|预估份额|中标.{0,10}?份额|中选.{0,10}?份额|份额划分','标段数量|标包数量','限定','中标候选人数量|中选候选人数量','(中标数量|中标人数量|候选人数量|中选人数量|中选数量|(中选|中标).*家数)','推荐单位|申请单位|申请人|应答人|候选人|单位名称|服务商名称|公司名称|中选人|供应商|投标人|入围(服务商|单位|厂家|公司)','包序|服务包|标包号|标段号|标段|标包|^包$|采购包|比选包|选包|子项|分项','建设规模|标包名称|采购包名称|选包名称|标段名称|产品名称|标包介绍|标段介绍|标包内容|标段内容','序号|排名|名次','负责人','证书编号','工期','估算数量|需求数量|数量','区域|地域|地市|本地网|地点']
keymaps = ['budget','sequence','discount','share','pkg_counts','limit','can_counts','bid_counts','candidate','package','product','order','projectmanager','pm_license','period','pt_counts','location']

p9 = "(\d{1,12}\.?\d{0,4}?)"
p9_1 = "((\d{1,3},\d{3},\d{3},\d{3}.?\d{0,6}?)|(\d{1,3},\d{3},\d{3}.?\d{0,6}?)|(\d{1,3},\d{3}.?\d{0,6}?))"
p9_2 = "(\d{1,12}\.?\d{0,6}?[元万亿])"
p9_3 = "((\d{1,3},\d{3},\d{3},\d{3}.?\d{0,6}?[元万亿])|(\d{1,3},\d{3},\d{3}.?\d{0,6}?[元万亿])|(\d{1,3},\d{3}.?\d{0,6}?[元万亿]))"

p7 = "(\d{1,3}(\.\d{1,2})\D?)%"

#p8 = "(折扣|上浮|下浮)"
p8 = "(\d{1,3}\.?\d{0,2})\D?%"
p8_2 = "(0\.\d{1,4})"
p8_3 = "(\d{1,3}\.?\d{0,2})"

CANDIDATE_LIST = "((([一二三四五六七八九]?[十一二三四五六七八九]{1,})([服采比]?[务购选]?[标包][段包]*))|([A-Z123456789一二三四五六七八九]{1,}[服采比]?[务购选]?[标包][段包]*)|(([服采比]?[务购选]?[标包][段包]*)([一二三四五六七八九]?十[一二三四五六七八九]?))|(([服采比]?[务购选]?[标包][段包]*)([A-Z123456789][0123456789])))"
def verifycandidate(candidate):
    ret = candidate
    v = False
    if len(candidate) >= 24:
        v = True
    elif candidate.find("公司") < 0:
        v = True
    else:
        m1 = re.findall(CANDIDATE_LIST,candidate)
        if len(m1) >= 0:
            v = True
    if v:
        objs = nerutils.getner(candidate)
        if len(objs) > 1:
            pass
            #ret = objs[0]['org'] + objs[1]['org']
        elif len(objs) == 1:
            ret = objs[0]['org']
        else:
            ret = ''
    else:
        pass
    return not v, ret

number_keys = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10}
number_str = "第([一二三四五六七八九十123456789])"

def cleanchar(text):
    while len(text) > 0 and text[len(text)-1] not in ['0','1','2','3','4','5','6','7','8','9']:
       text = text[0:len(text)-1]
    return text

def process_number(text):
    m1 = re.findall(number_str, text)
    if m1:
        if m1[0] in number_keys.keys():
            return number_keys[m1[0]]
    return 0

def process_discount(text):
    m1 = re.findall(p8, text)
    if m1:
        return float(m1[0]) / 100
    m1 = re.findall(p8_2, text)
    if m1:
        return float(m1[0])
    m1 = re.findall(p8_3, text)
    if m1:
        return float(m1[0]) / 100
    return None

def unit_convert(text):
    #print(text)
    try:
        t = text
        if t.endswith(')'):
            t = t[0:len(t)-1]
        if t.endswith('）'):
            t = t[0:len(t)-1]
        if t.endswith('元'):
            t = t[0:len(t)-1]
        t = t.replace(',','')
        value = 0
        if t.endswith('万'):
            value = float(cleanchar(t[:len(t)-1]))
            return value * 10000
        elif t.endswith('亿'):
            value = float(cleanchar(t[:len(t)-1]))
            return value * 100000000
        else:
            value = float(cleanchar(t))
        return value
    except Exception as e:
        logging.error(e)
        logging.error("failed to convert:%s" % text)
    return 0

def process_rmb(text):
    m1 = re.findall(p9_3, text)
    if len(m1) > 0:
        if len(m1[0]) > 0:
            return unit_convert(m1[0][0])
    m1 = re.findall(p9_2, text)
    if len(m1) > 0:
        #print(m1)
        return unit_convert(m1[0])
    m1 = re.findall(p9_1, text)
    if len(m1) > 0:
        if len(m1[0]) > 0:
            return float(m1[0][0].replace(',',''))
    m1 = re.findall(p9, text)
    if len(m1) > 0:
        return float(m1[0])
    return None

def findmax(keys, key):
    print("keys:%s key:%s" % (keys,key))
    maxvalue = 2
    for item in keys:
        if len(item) == '':
            continue
        if item.find(key) >= 0:
            if len(item) == len(key):
                if maxvalue < 2:
                    maxvalue = 2
            else:
                pos = len(key)
                value = int(item[pos:]) + 1
                if maxvalue < value:
                    maxvalue = value 
    return str(maxvalue)

def getmerge(keys):
    ret = []
    merge = ''
    for key in keys:
        j = 0
        found = False
        for str1 in strs:
            m1 = re.findall(str1, key)
            if m1:
              if keymaps[j] in ret:
                newkey = keymaps[j] + findmax(ret, keymaps[j])
                ret.append(newkey)
                if key.startswith('S--'):
                    merge += newkey + '.'
              else:
                ret.append(keymaps[j])
              found = True
              break
            j+=1
        if not found:
            ret.append(key)
    return merge

def keymap(keys):
    ret = []
    merge = ''
    for key in keys:
        j = 0
        found = False
        for str1 in strs:
            m1 = re.findall(str1, key)
            if m1:
              if keymaps[j] in ret:
                newkey = keymaps[j] + findmax(ret, keymaps[j])
                ret.append(newkey)
              else:
                ret.append(keymaps[j])
              found = True
              break
            j+=1
        if not found:
            ret.append(key)
    return ret

def process_candidate(text):
    value_type = True
    value = text
    pos = text.find("（候选）")
    if pos < 0:
        pos =  text.find("（备选）")
    if pos >=0:
        value = text[0:pos]
        value_type = False
    v, value = verifycandidate(text)
    return value,value_type

def getkey(key):
        ret = key
        j = 0
        found = False
        for str1 in strs:
            m1 = re.findall(str1, key)
            if m1:
              ret = keymaps[j]
              break
            j+=1
        return ret

def getkeys(key):
        ret = []
        j = 0
        found = False
        for str1 in strs:
            m1 = re.findall(str1, key)
            if m1:
              ret.append(keymaps[j])
            j+=1
        return ret

def getsecondkey(key,firstkey):
        ret = None
        j = 0
        found = False
        for str1 in strs:
            m1 = re.findall(str1, key)
            if m1:
              if firstkey != keymaps[j]:
                ret = keymaps[j]
            j+=1
        return ret

def getthirdkey(key,firstkey,secondkey):
        ret = None
        j = 0
        found = False
        for str1 in strs:
            m1 = re.findall(str1, key)
            if m1:
              if firstkey != keymaps[j] and secondkey != keymaps[j]:
                ret = keymaps[j]
            j+=1
        return ret
