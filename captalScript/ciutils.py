import jieba
import logging

logging.basicConfig(filename='logger_ztb2.log', level=logging.INFO)

def ciratetext(text):
    kc = {}
    ci = jieba.cut(text)
    counts = 0
    for c in ci:
        if c.strip() == '':
            continue
        if c not in kc:
            kc[c] = 0
        kc[c] += 1
        counts += 1
    vv = 0
    for k,v in kc.items():
        vv += v
        #print(k,v)

    if counts == 0:
        return 0
    #print("vv:%d cc:%d" % (vv,counts))
    return 1.0 * vv / counts

KEYS = ['0','1','2','3','4','5','6','7','8','9']
EKEYS = ['通过','不通过','合格','不合格']
def ratetext(text, num = 2):
    kc = {}
    ci = text.split("\n")
    counts = 0
    for c in ci:
        c = c.strip()
        if c == '':
            continue
        if c not in kc:
            kc[c] = 0
        kc[c] += 1
        counts += 1
    vv = 0
    for k,v in kc.items():
        if v >= num and k[0] not in KEYS and k not in EKEYS and len(k) > 1:
            vv += v
        #print(k,v)
            logging.info("key:%s, c:%d" % (k,v))

    if counts == 0:
        return 0
    #print("vv:%d cc:%d" % (vv,counts))
    return 1.0 * vv / counts
