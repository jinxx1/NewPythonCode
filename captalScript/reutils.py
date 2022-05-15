import re
import nerutils
import keysutils
from keysutils import cleanchar

pa = ".*(采\S?购\S?人|招\S?标\S?人|招\S?募\S?人|发布单位|比\S?选\S?人).{0,12}"
p1 = re.compile(pa)
pb = ".*(代理).{0,12}"
p2 = re.compile(pb)
pc = ".*((第[一二三四五六七八九123456789])?(候选|中标|中选|成交|签约|入围)).{0,12}"
p3 = re.compile(pc)
#pd = ".*(采购人|招标人|招募人|发布单位|比选人/.{0,2}代理.{0,2}：).*"
pd = ".*(采购人|招标人|招募人|发布单位|比选人).{0,6}/.{0,6}代理.{0,6}.*"
p4 = re.compile(pd)
#pe = ".*[采购人|招标人|招募人|发布单位|比选人].{0,6}/(.{0,6}代理.{0,6}).* ：.*/.*"
pe = ".*[采购人|招标人|招募人|发布单位|比选人].{0,6}/.{0,6}(代理).{0,6}：.*/.*"
p5 = re.compile(pe)

p3_2 = "项目负责人"

pf = "(.*)受(.*)委托.*"

p6 = re.compile(pf)

p7 = "(份额)\D{0,10}(\d{1,3}(\.\d{1,2})\D?)%"

pg = re.compile(p7)

p8 = "(折扣|上浮|下浮)\D{0,10}(\d{1,3}\.?\d{0,2}\D?)%"

p8_2 = "(折扣|上浮|下浮)\D{0,10}(0\.\d{1,4})"

p8_3 = "(折扣|上浮|下浮)\D{0,10}(\d{1,3}\.?\d{0,2})"

p8_4 = "(报价|价格)[：:]?\s*?.{0,12}?(\d{1,3}\.?\d{0,2}\D?)%"

p9 = "(金额|规模|投资|工程费|上限|估算|概算|预算|总价|报价|限价|预估|费用)\D{0,10}(\d{4,12}\.?\d{0,6}?)\s*?$"
p9_2 = "(金额|规模|投资|工程费|上限|估算|概算|预算|总价|报价|限价|预估|费用)\D{0,10}(\d{1,12}\.?\d{0,6}?[】]?\s*?[(（]?[元万亿][)）]?)"
p9_3 = "(金额|规模|投资|工程费|上限|估算|概算|预算|总价|报价|限价|预估|费用)\D{0,10}((\d{1,3},\d{3},\d{3},\d{3}.?\d{0,6}?[】]?\s*?[(（]?[元万亿][)）]?)|(\d{1,3},\d{3},\d{3}.?\d{0,6}?[】]?\s*?[(（]?[元万亿][)）]?)|(\d{1,3},\d{3}.?\d{0,6}?[】]?\s*?[(（]?[元万亿])[)）]?)"
p9_0 = "(金额|投资|工程费|上限|预算|总价|报价|限价|费用)\D{0,10}(\d{1,12}\.?\d{0,6}?)[，。\n]"

pr = ".*(金额|规模|投资|工程费|上限|估算|概算|预算|总价|报价|限价|费用)?.{0,10}((\d{4,12}\.?\d{0,2}?$)|(\d{1,12}\.?\d{0,6}?[元万亿])|((\d{1,3},)?(\d{1,3},)?(\d{1,3},)?(\d{1,3})[.]?\d{0,6}?[元万亿])).*"

p10 = "(工程费|施工费)\D{0,10}(\d{4,12}\.?\d{0,2}?)\s*?$"
p10_2 = "(工程费|施工费)\D{0,10}(\d{1,12}\.?\d{0,6}?[】]?\s*?[元万亿])"
p10_3 = "(工程费|施工费)\D{0,10}((\d{1,3},\d{3},\d{3},\d{3}.?\d{0,6}?[】]?\s*?[元万亿])|(\d{1,3},\d{3},\d{3}.?\d{0,6}?[】]?\s*?[元万亿])|(\d{1,3},\d{3}.?\d{0,6}?[】]?\s*?[元万亿]))"

p19 = "(金额|规模|投资|工程费|上限|估算|概算|预算|总价|限价|预估|费用)\D{0,10}(\d{4,12}\.?\d{0,6}?)\s*?$"
p19_2 = "(金额|规模|投资|工程费|上限|估算|概算|预算|总价|限价|预估|费用|项目概况：)\D{0,10}(\d{1,12}\.?\d{0,6}?[】]?\s*?[(（]?[元万亿][)）]?)"
p19_3 = "(金额|规模|投资|工程费|上限|估算|概算|预算|总价|限价|预估|费用|项目概况：)\D{0,10}((\d{1,3},\d{3},\d{3},\d{3}.?\d{0,6}?[】]?\s*?[(（]?[元万亿][)）]?)|(\d{1,3},\d{3},\d{3}.?\d{0,6}?[】]?\s*?[(（]?[元万亿][)）]?)|(\d{1,3},\d{3}.?\d{0,6}?[】]?\s*?[(（]?[元万亿])[)）]?)"
p19_0 = "(金额|投资|工程费|上限|预算|总价|限价|费用)\D{0,10}(\d{1,12}\.?\d{0,6}?)[，。\n]"

#NO.1选包第一中选候选人：
str_p0 = "(([一二三四五六七八九]?[十一二三四五六七八九]{1,})([采比]?[购选]?[标包][段包件]*))((第[1234567890一二三四五六七八九十])[名中][标选]?候?选?人?)[\s.:：是为]|(([A-Z0123456789][0123456789]?)([采比]?[购选]?[标包][段包件]*))((第[1234567890一二三四五六七八九十])[名中][标选]?候?选?人?)[\s.:：是为]|(([采比]?[购选]?[标包][段包件]*)([一二三四五六七八九]?[十一二三四五六七八九]{1,2}))((第[1234567890一二三四五六七八九十])[名中][标选]?候?选?人?)[\s.:：是为]|(([采比]?[购选]?[标包][段包件]*)\[?([A-Z0123456789][0123456789]?))((第[1234567890一二三四五六七八九十])[名中][标选]?候?选?人?)[\s.:：是为]|(([采比]?[购选]?[标包][段包件]*)\[?([A-Z0123456789][0123456789]?))((第[1234567890一二三四五六七八九十])[名中][标选]?候?选?人?)\n"
str_p1 = "(([一二三四五六七八九]?[十一二三四五六七八九]{1,})([采比]?[购选]?[标包][段包件]*)).{0,20}?[\s.:：是为]|(([A-Z0123456789][0123456789]?)([采比]?[购选]?[标包][段包件]*)).{0,20}?[\s.:：是为]|(([采比]?[购选]?[标包][段包件]*)([一二三四五六七八九]?[十一二三四五六七八九]{1,2})).{0,20}?[\s.:：是为]|(([采比]?[购选]?[标包][段包件]*)\[?([A-Z0123456789][0123456789]?)).{0,20}?[\s.:：是为]|(([采比]?[购选]?[标包][段包件]*)\[?([A-Z0123456789][0123456789]?))\D{0,20}?\n|((标段[(（]包[)）])[（(\[]?([A-Z0123456789][0123456789]*)).{0,20}?[\s.:：是为]"
#润建股份有限公司为第一中选候选人
str_b0 = "(.*?)为(第[1234567890一二三四五六七八九十])[名中][标选]?候?选?人?"
str_b1 = "(第[1234567890一二三四五六七八九十])[名中][标选]?候?选?人?"

BLACK_LIST = ['比选','机构','中国','省公司','诚E招','比选人公司','招标代理公司','联合体','新禾联']
REX_LIST = '(.高职$|.*建安$|.{2,4}部$|.*委员会$|.*评委会$|.*组委会$|.*代理机构$|.*办公室$|.*小组$|.*监察室$|.*招标网$|.*采购网$|.*纪委$)'
OTHER_LIST = "([\w]+(\.[\w]+)*@[\w]+(\.[\w]+)+)"

def printobjs(objs):
    if len(objs) > 0:
        print(objs)

def nerfilter(text,ner_type):
    if text is None or len(text) == 1:
        return False
    if text in BLACK_LIST:
        return False
    if ner_type == 'LOC':
        return False
    m1 = re.findall(REX_LIST, text)
    if len(m1) > 0:
        return False
    m1 = re.findall(OTHER_LIST, text)
    if len(m1) > 0:
        return False
    return True

KEYWORDS_YJ=['业绩','注册资金','注册资本','供货金额','同类','单价','条件','具有','满足','合作','招标文件费用','采购文件','每套售价','招标文件','比选文件']
ZT_NUMBER = ['500元','400元','300元','200元','100元']

def getline2(text, pos):
    text1 = text[0:pos]
    pos1 = text1.rfind('\n')
    pos1_b = text1.rfind(' ')
    if pos1_b > pos1:
       pos1 = pos1_b
    if pos1 < 0:
       pos1 = 0
    newtext = text1[pos1:]
    return newtext,pos1

def budgetfilter(plaintext,m):
    print("budgetfilter for :%s" % m)
    if m in ZT_NUMBER:
        return False, plaintext
    pos = plaintext.find(m)
    if pos >= 0:
        #text,tpos = getline(plaintext, pos)
        text,tpos = getline2(plaintext, pos)
        print(tpos)
        print(text)
        for c in KEYWORDS_YJ:
            cpos = text.find(c)
            if cpos >= 0:
                print("************%d" % cpos)
                #return False,plaintext[tpos+len(text):]
                return False,plaintext[pos + len(m):]
        return True,plaintext[pos + len(m):]
    return True,plaintext

def getbiaometa(text):
    ret = []
    m1 = re.findall(str_p1, text)
    if len(m1) > 0:
      print(m1)
      for mm in m1:
        if mm[0] != '':
          ret.append(mm[0])
        if mm[3] != '':
          ret.append(mm[3])
        if mm[6] != '':
          ret.append(mm[6])
        if mm[9] != '':
          ret.append(mm[9])
        if mm[12] != '':
          ret.append(mm[12])
        if mm[15] != '':
          ret.append(mm[15])
    return ret

number_str = "(\d*)"
def getnumber(text):
    m1 = re.findall(number_str, text)
    if len(m1) > 0:
        try:
            ret = int(m1[0])
            return ret
        except Exception as e:
            print(e)
        return None
    else:
        return None

float_str = "(\d{1,}\.?\d{0,6})"
def getfloatstr(text):
    m1 = re.findall(float_str, text)
    if len(m1) > 0:
        try:
            ret = m1[0]
            print("ret:%s" % ret)
            return ret
        except Exception as e:
            print(e)
        return None
    else:
        return None

def process_biaoinfo2(text):
    # print("process_biaoinfo2:%s" % text)
    print("process_biaoinfo2:reutlis.py ----160" )
    tpos = text.find('否决')
    if tpos >= 0:
        text = text[:tpos]
    ret = []
    r1 = re.compile(str_b1)
    m1 = re.finditer(r1,text)
    objs = []
    labels = []
    while True:
        try:
            label = None
            obj = m1.__next__()
            groups = obj.groups()
            for group in groups:
                if group:
                    label = group
                    break
            if label and label not in labels:
                labels.append(label)
                objs.append(obj)
            print(obj)
        except Exception as e:
            print(e)
            break
    printobjs(labels)
    objs_size = len(objs)
    if objs_size == 0:
        zz = nerutils.getner(text)
        printobjs(zz)
        for z in zz:
          if z['ner_type'] == 'ORG' and z['type'] not in ['招标','代理']:
            if z['org'] in ret:
              #skip the duplicate company
              continue
            if z['type'] == '':
              z['type'] = '中选'
            if nerfilter(z['org'],z['ner_type']):
              ret.append(z)
        return ret

    newtext = ""
    for i in range(objs_size):
        if i == objs_size - 1:
            newtext = text[objs[i].start():]
        else:
            obj1 = objs[i]
            obj2 = objs[i+1]
            newtext = text[obj1.start():obj2.start()]
        #print(newtext)
        zz = nerutils.getner(newtext)
        printobjs(zz)
        for z in zz:
          if 'sbudget' in z.keys():
              oflag, otext = budgetfilter(newtext, str(z['sbudget']))
              if not oflag:
                  z.pop('budget')
          if z['type'] not in ['招标','代理'] and z['ner_type'] == 'ORG':
            if z['org'] in ret:
              #skip the duplicate company
              continue
            if z['type'] == '':
              z['type'] = '中选'
            if nerfilter(z['org'],z['ner_type']):
              ret.append(z)
    return ret

def preprocess_biaoinfo2(objs,text):
    ret = []
    objs_size = len(objs)
    newtext = ""
    for i in range(objs_size):
        if i == objs_size - 1:
            newtext = text[objs[i].start():]
        else:
            obj1 = objs[i]
            obj2 = objs[i+1]
            newtext = text[obj1.start():obj2.start()]
        #print(newtext)
        zz = nerutils.getner(newtext)
        print(zz)
        for z in zz:
          if 'sbudget' in z.keys():
              oflag, otext = budgetfilter(newtext, str(z['sbudget']))
              if not oflag:
                  z.pop('budget')
          if z['type'] not in ['招标','代理'] and z['ner_type'] == 'ORG':
            if z['org'] in ret:
              #skip the duplicate company
              continue
            if z['type'] == '':
              z['type'] = '中选'
            if nerfilter(z['org'],z['ner_type']):
              ret.append(z)
    return ret

def preprocess_biaoinfo(text):
    print("preprocess_biaoinfo")
    #print(text)
    text = text.replace("\xa0", '')
    ret = []
    r1 = re.compile(str_p0)
    m1 = re.finditer(r1,text)
    objs = []
    labels = []
    while True:
        try:
            label = None
            obj = m1.__next__()
            #CHECK IF THE PACKAGE IS VALID, if it followed by some keywords as following, then could not be a correct package
            if len(text) >= obj.end() + 2:
                if text[obj.end():obj.end() + 2] == '划分' or text[obj.start():obj.end()].find('划分') >= 0:
                    print("WRONG PACKAGE:%s" % obj)
                    continue
            groups = obj.groups()
            #print(groups)
            for group in groups:
                if group:
                    label = group
                    break
            if label and label not in labels:
                labels.append(label)
                package = {}
                package['package'] = label
                ret.append(package)
                objs = []
                package['mshares'] = objs
            objs.append(obj)
            print(obj)
        except Exception as e:
            print(e)
            break
    print(labels)
    print(objs)
    for obj in ret:
        objs = obj['mshares']
        obj['mshares'] = preprocess_biaoinfo2(objs,text)
    return ret
 
def process_biaoinfo(text):
    ret = preprocess_biaoinfo(text)
    if len(ret) > 0:
        print(ret)
        return ret
    print("process_biaoinfo")
    #print(text)
    text = text.replace("\xa0", '')
    ret = []
    r1 = re.compile(str_p1)
    m1 = re.finditer(r1,text)
    objs = []
    labels = []
    while True:
        try:
            label = None
            obj = m1.__next__()
            #CHECK IF THE PACKAGE IS VALID, if it followed by some keywords as following, then could not be a correct package
            if len(text) >= obj.end() + 2:
                if text[obj.end():obj.end() + 2] == '划分' or text[obj.start():obj.end()].find('划分') >= 0:
                    print("WRONG PACKAGE:%s" % obj)
                    continue
            if obj.start() > 0:
                if text[obj.start() - 1:obj.start()] in ['个','国']:
                    print("WRONG PACKAGE:%s" % obj)
                    continue
            groups = obj.groups()
            #print(groups)
            for group in groups:
                if group:
                    label = group
                    break
            if label and label not in labels:
                labels.append(label)
                objs.append(obj)
            print(obj)
        except Exception as e:
            print(e)
            break
    print(labels)

    objs_size = len(objs)
    newtext = ""
    for i in range(objs_size):
        if i == objs_size - 1:
            newtext = text[objs[i].end():]
        else:
            obj1 = objs[i]
            obj2 = objs[i+1]
            newtext = text[obj1.end():obj2.start()]
        #print(newtext)
        biao = {}
        biao['package'] = labels[i]
        biao['mshares'] = process_biaoinfo2(newtext)
        ret.append(biao)
    return ret

def process_rmb2(text):
    m1 = re.findall(p10_3, text)
    if m1:
        return m1
    m1 = re.findall(p10_2, text)
    if m1:
        return m1
    m1 = re.findall(p10, text)
    if m1:
        return m1
    return None

def process_share(text):
    m1 = re.findall(p7, text)
    if m1:
        return m1[0][0], float(cleanchar(m1[0][1])) / 100
    return None

def process_discount(text):
    m1 = re.findall(p8, text)
    if m1:
        return m1[0][0], float(cleanchar(m1[0][1])) / 100
    m1 = re.findall(p8_2, text)
    if m1:
        return m1[0][0], float(cleanchar(m1[0][1]))
    m1 = re.findall(p8_3, text)
    if m1:
        return m1[0][0], float(cleanchar(m1[0][1])) / 100
    m1 = re.findall(p8_4, text)
    if m1:
        return m1[0][0], float(cleanchar(m1[0][1])) / 100
    return None

def process_rmb(text):
    m1 = re.findall(p9_3, text)
    if m1:
        return m1
    m1 = re.findall(p9_2, text)
    if m1:
        return m1
    m1 = re.findall(p9, text)
    if m1:
        return m1
    m1 = re.findall(p9_0, text)
    if m1:
        return m1
    return None

def process_rmb0(text):
    m1 = re.findall(p19_3, text)
    if m1:
        return m1
    m1 = re.findall(p19_2, text)
    if m1:
        return m1
    m1 = re.findall(p19, text)
    if m1:
        return m1
    m1 = re.findall(p19_0, text)
    if m1:
        return m1
    return None

