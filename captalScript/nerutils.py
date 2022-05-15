import sys
import requests
import json
import re
import keysutils
# URL = "183.6.136.67:8001/ner"
URL = "http://183.6.136.67:8075/infoContent/"
# URL = 'http://ztb.uxuepai.net:8001/ner'
# URL = "http://localhost:8001/ner"
#URL = "http://appincloud.cn:8001/ner"
WHITE_LIST = []
BLACK_LIST = ['比选','评标委员会','机构','评审委员会','比选代理机构','比选代理机构','采购评审委员会','评委会','评选委员会','竞争性谈判小组','采购评标委员会','中国','省公司']

def nerfilter(text,ner_type):
    if len(text) == 1:
        return False
    if text in WHITE_LIST:
        return False
    if ner_type == 'LOC':
        return False
    return True

pa = "(采购人|招标人|招募人|发布单位|比选人)[：:](.{0,20}?公司)"
KEYWORDS_Z = ['候选','中标','中选','成交','签约','入围','供应','申请']
def ztb(text):
    #p1 = re.compile(pa)
    m1 = re.findall(pa,text)
    print(m1)

def preprocess(allobjs):
    newobjs = []
    for objs in allobjs:
        if len(objs) == 0:
            continue
        i = 0
        for i in range(len(objs)):
            obj = objs[i]
            obj[2] = obj[2].replace('【','').replace('】','')
            if i < len(objs) - 1:
              nobj = objs[i+1]
              nobj[2] = nobj[2].replace('【','').replace('】','')
              bid_type, ner_type, name, pos, share, discount, budget = obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6]
              nbid_type, nner_type, nname, npos, nshare, ndiscount, nbudget = nobj[0], nobj[1], nobj[2], nobj[3], nobj[4], nobj[5], nobj[6]
              #fix the bid issue
              if share is not None and bid_type == '':
                  obj[0] = '中选'
              if nshare is not None and nbid_type == '':
                  nobj[0] = '中选'

              if ner_type == 'LOC' and nner_type == 'ORG' and (pos + len(name)) == npos:
                nobj[2] = name + nname
                nobj[3] = pos
                newobjs.append(nobj)
                i += 1
              else:
                newobjs.append(obj)
            else:
              #fix the bid issue
              if obj[4] is not None and obj[0] == '':
                  obj[0] = '中选'

              newobjs.append(obj)
            i += 1
    return [newobjs]

def getner(text):
    text = text.strip()
    #print(len(text),text)
    text = text.replace("\xa0", '')
    text = text.replace('\u3000', '')
    text = text.replace('\u2003', '')
    text = text.replace('\u2002', '')
    text = text.replace(",","\n")
    text = text.replace("，","\n")
    text = text.replace("。","\n")
    text = text.replace(" ","\n")
    text = text.replace("、","\n")
    dict1 = {}
    dict1['name'] = text
    ret = requests.post(URL,dict1)
    allobj = []
    try:
        allobj = json.loads(ret.content)
        allobj = preprocess(allobj)
    except Exception as e:
        print(e)
    newobjs = []
    companies = []
    for objs in allobj:
        if len(objs) == 0:
            continue
        print(objs)
        for obj in objs:
            bid_type, ner_type, name, pos, share, discount, budget = obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6]
            if name in  WHITE_LIST:
                continue
            if name in companies:
                continue

            newobj = {}
            newobj['ner_type'] = ner_type
            if True:
                if discount:
                    if discount[0] == '下浮':
                        newobj['discount'] = 1 - discount[1]
                    else:
                        newobj['discount'] = discount[1]
                if budget:
                    newobj['sbudget'] = budget[0][1]
                    newobj['budget'] = keysutils.process_rmb(budget[0][1])
                if share:
                    newobj['share'] = share[1]

            if bid_type in KEYWORDS_Z:
                if ner_type not in ['ORG','PER']:
                    print("wrong ner:%s" % ner_type)
                    #continue
                companies.append(name)
                newobj['type'] = '中选'
                newobj['org'] = name
                newobj['candidate'] = name
                if False:
                  if discount:
                    newobj['discount'] = discount[1]
                  if budget:
                    newobj['budget'] = keysutils.process_rmb(budget[0][1])
                  if share:
                    newobj['share'] = share[1]
                newobjs.append(newobj)
            elif len(bid_type) > 0:
              if bid_type[0] in ['比','采','招','发'] and ner_type == 'ORG':
                companies.append(name)
                newobj['type'] = '招标'
                newobj['org'] = name
                newobjs.append(newobj)
              elif bid_type[0] in ['代','商'] and ner_type == 'ORG':
                companies.append(name)
                newobj['type'] = '代理'
                newobj['org'] = name
                newobjs.append(newobj)
            else:
                newobj['type'] = ''
                newobj['ner_type'] = ner_type
                newobj['org'] = name
                newobjs.append(newobj)
 
    return newobjs

if __name__ == "__main__":
    import bs4
    from urllib.request import urlopen
    url = sys.argv[1]
    html = urlopen(url)
    bsObj = bs4.BeautifulSoup(html)
    print(getner(bsObj.text))
    #ztb(bsObj.text)
