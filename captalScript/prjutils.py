import sys
import json
import datetime
import requests
import re
import keysutils
import ztbutils
import os
import datagram
import jsonutils
import reutils
import logging
import db2mongo
import pprint

logging.basicConfig(filename='logger_ztb2.log', level=logging.INFO)

KEYWORDS_DIS = ['(开发区|自治县|示范区|产业聚集区|管理区|林区|保税区|园区)$']
KEYWORDS_DIS1 = ['(新区)$']
KEYWORDS_DIS2 = ['(市|区|县)$']


def getshortname(name):
    if re.findall(KEYWORDS_DIS, name) > 0:
        return name
    elif re.findall(KEYWORDS_DIS1, name) > 0:
        return name[:len(name) - 2]
    elif re.findall(KEYWORDS_DIS2, name) > 0:
        return name[:len(name) - 1]
    return name


KEYWORDS_M = ['金额', '份额', '工程费', '施工费', '区域', '地市', '总价', '标段', '采购包', '选包', '子项']
KEYWORDS_PM = ['pm_license', '证书编号']


def checkfield(keywords, keys):
    ret = False
    for key in keys:
        for keyword in keywords:
            if key.find(keyword) >= 0:
                ret = True
                break
    return ret


def checkduplicate(objs, obj, name='package'):
    for item in objs:
        # TODO
        if name not in item.keys():
            print("%s not in %s" % (name, item))
            continue
        elif name not in obj.keys():
            print("%s not in %s" % (name, obj))
            continue
        if item[name] == obj[name]:
            return True
    return False


KEYWORDS_HJ = ['总计', '合计', '小计']


def checksummary(share):
    if 'sequence' in share.keys() and isinstance(share['sequence'], str):
        if share['sequence'] in KEYWORDS_HJ:
            return False
    if 'order' in share.keys() and isinstance(share['order'], str):
        if share['order'] in KEYWORDS_HJ:
            return False
    return True


KEYWORDS_TBN = "(((中选|中标).*?份额)|(份额(划分|分配)))"
# except: 中选人数量：本项目中选人数量为3个，各中选人对应
# KEYWORDS_TBN_BID = "(入围|准入|推荐|候选|中选|中标)(人|服务商|单位|厂家|公司)[^数对]"
KEYWORDS_TBN_BID = "((中标|成交|中选|签约|入围|合格|通过|通过审查)的?(人|厂家|公司|候选人|供应商|申请人).{0,3}?[下是为:：])"


def checktablename(pkg, keywords=KEYWORDS_TBN):
    if pkg is None or 'tablename' not in pkg.keys() or pkg['tablename'] is None:
        return False
    tablename = pkg['tablename']
    m1 = re.findall(keywords, tablename)
    if len(m1) > 0:
        return True
    return False


def json_default(value):
    if isinstance(value, datetime.datetime):
        # return dict(year=value.year, month=value.month, day=value.day)
        return value.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return value.__dict__


def getfloat(floatstr):
    if isinstance(floatstr, str):
        return float(reutils.getfloatstr(floatstr))
    elif isinstance(floatstr, float) or isinstance(floatstr, int):
        return floatstr
    else:
        return 0


def getsharesbudgetmax(shares):
    budget = 0
    for key in shares.keys():
        if not key.startswith('budget'):
            continue
        if shares[key] > budget:
            if 'duplicate' not in shares.keys():
                budget = shares[key]
            elif shares['duplicate'].find(key) < 0:
                budget = shares[key]
    return budget


def getsharebudgetuniq(shares):
    budget = 0
    for share in shares:
        if 'duplicate' not in share.keys():
            continue
        for key in share.keys():
            if not key.startswith('budget'):
                continue
            if share['duplicate'].find(key) >= 0:
                budget = share[key]
                break
    return budget


def getpackagebudget(obj, name='budget'):
    budget = 0
    if 'mshares' not in obj.keys():
        return 0
    if name in obj.keys():
        budget += obj[name]
        if budget > 0:
            return budget
    for package in obj['mshares']:
        if 'package2' in package.keys() and 'mshares' in package.keys():
            logging.debug("getpkg budget:%s" % package)
            budget += getsharebudgetuniq(package['mshares'])
            # for shares in package['mshares']:
            #    budget += getsharesbudgetmax(shares)
        elif name in package.keys() and package[name] is not None:
            budget += package[name]
    logging.info("getpackagebudget:%f" % budget)
    logging.info(obj)
    return budget


def getpkgbudget(obj):
    budget = 0
    if 'budget' in obj.keys():
        budget = obj['budget']
    if budget is None or budget == 0:
        budget = getpackagebudget(obj, 'budget')
    return budget


def getpackagesbudget(objs):
    budget = 0
    for obj in objs:
        budget += getpackagebudget(obj, 'budget')
    return budget


def getsumbudget(objs):
    ret = 0
    lastpos = len(objs) - 1
    if lastpos < 0:
        return 0
    if 'package' not in objs[lastpos].keys():
        return 0
    if objs[lastpos]['package'] in KEYWORDS_HJ:
        obj = objs[lastpos]
        if 'budget' in obj.keys() and obj['budget'] > 0:
            ret = obj['budget']
        elif 'budget2' in obj.keys() and obj['budget2'] > 0:
            ret = obj['budget2']
        elif 'budget3' in obj.keys() and obj['budget3'] > 0:
            ret = obj['budget3']
    logging.debug("getbudget:%s" % ret)
    return ret


def getbudget2(info):
    ret = 0
    for obj in info['list']:
        budget = 0
        if 'budget' in obj.keys():
            budget += obj['budget']
            if obj['budget'] == 0:
                budget += getpackagebudget(obj)
        ret += budget
    logging.debug("getbudget2:%f" % ret)
    return ret


def getbudget(info):
    ret = 0
    reto = 0
    if 'budget' in info.keys() and info['budget'] > 0:
        reto = info['budget']

    budgets = []
    if 'list' in info.keys():
        for o in info['list']:
            # not a package dict, instead it is package list
            if o is None:
                logging.info("none obj in list")
                print("list is None")
                continue
            if 'objs' not in o.keys():
                print("no objs in list")
                return getbudget2(info)
            # print(o)
            budget = getsumbudget(o['objs'])
            if budget > 0:
                ret += budget
            else:
                budget = 0
                for obj in o['objs']:
                    # budget = 0
                    if not checksummary(obj):
                        continue
                    if 'budget' in obj.keys():
                        if obj['budget'] is None:
                            obj['budget'] = 0
                        budget += obj['budget']
                        if obj['budget'] == 0:
                            budget += getpackagebudget(obj)
                    if budget == 0 and 'budget2' in obj.keys():
                        if obj['budget2'] is None:
                            obj['budget2'] = 0
                        budget += obj['budget2']
                        if obj['budget2'] == 0:
                            budget += getpackagebudget(obj, 'budget2')
                    if budget == 0 and 'budget3' in obj.keys():
                        if obj['budget3'] is None:
                            obj['budget3'] = 0
                        budget += obj['budget3']
                        if obj['budget3'] == 0:
                            budget += getpackagebudget(obj, 'budget3')
                            # ret += budget
            budgets.append(budget)
    if len(budgets) > 0:
        b = budgets[0]
        ret = 0
        for bb in range(len(budgets)):
            print(budgets[bb])
            if b == budgets[bb]:
                ret = budgets[bb]
            else:
                ret += budgets[bb]
    if reto > ret:
        ret = reto
    return ret


def coorelationprj(title):
    infolist = getinfolist(title)


str_p1 = "([一二三四五六七八九]?[十一二三四五六七八九]{1,}[服采比]?[务购选]?[标包][段包]*)|([A-Z123456789][0123456789]?[服采比]?[务购选]?[标包][段包]*)|([服采比]?[务购选]?[标包][段包]*[一二三四五六七八九]?[十一二三四五六七八九]{1,2})|([服采比]?[务购选]?[标包][段包]*[A-Z123456789][0123456789]?)"


def splitpkg(pkg_name):
    ret = []
    m1 = re.findall(str_p1, pkg_name)
    if len(m1) > 0:
        # print(m1)
        for mm in m1:
            if mm[0] != '':
                ret.append(mm[0])
            elif mm[1] != '':
                ret.append(mm[1])
            elif mm[2] != '':
                ret.append(mm[2])
            elif mm[3] != '':
                ret.append(mm[3])
    else:
        ret.append(pkg_name)
    return ret


def getdefaultpkg(prj):
    if 'packages' not in prj.keys() or len(prj['packages']) == 0:
        return None
    for pkg in prj['packages']:
        if 'mshares' in pkg.keys():
            return pkg
    return None


str_x1 = "(([一二三四五六七八九]?[十一二三四五六七八九]{1,})([服采比]?[务购选]?[标包][段包]*))|(([A-Z123456789][0123456789]?)([服采比]?[务购选]?[标包][段包]*))|(([服采比]?[务购选]?[标包][段包]*)([一二三四五六七八九]?[十一二三四五六七八九]{1,2}))|(([服采比]?[务购选]?[标包][段包]*)([A-Z123456789][0123456789]?))"


def issamepackage(str1, str2):
    if len(str1) == 0 or len(str2) == 0:
        print("wrong pag:%s %s" % (str1, str2))
        return False
    if str1 == str2:
        return True
    else:
        tmp_str1 = str1
        tmp_str2 = str2
        if str1[0] in ['标', '包']:
            tmp_str1 = str1[1:]
        if str2[0] in ['标', '包']:
            tmp_str2 = str2[1:]
        if str1.startswith('NO.'):
            tmp_str1 = str1[3:]
        if str2.startswith('NO.'):
            tmp_str2 = str2[3:]
        if tmp_str1 == tmp_str2:
            return True
    if True:
        seq1 = jsonutils.seq_order(str1)
        seq2 = jsonutils.seq_order(str2)
        mm = re.findall(str_x1, str1)
        # print(mm,str1)
        if mm:
            mm = mm[0]
            if mm[0] != '':
                seq1 = jsonutils.seq_order(mm[1])
            elif mm[3] != '':
                seq1 = jsonutils.seq_order(mm[4])
            elif mm[6] != '':
                seq1 = jsonutils.seq_order(mm[8])
            elif mm[9] != '':
                seq1 = jsonutils.seq_order(mm[11])
        mm = re.findall(str_x1, str2)
        # print(mm,str2)
        if mm:
            mm = mm[0]
            if mm[0] != '':
                seq2 = jsonutils.seq_order(mm[1])
            elif mm[3] != '':
                seq2 = jsonutils.seq_order(mm[4])
            elif mm[6] != '':
                seq2 = jsonutils.seq_order(mm[8])
            elif mm[9] != '':
                seq2 = jsonutils.seq_order(mm[11])
        if seq1 != 0 and seq2 != 0 and seq1 == seq2:
            # print("same pkg")
            return True
    return False


def getbid(i, shares):
    if i == 0:
        return True
    elif len(shares) == 2:
        return (i == 0)
    elif len(shares) == 3:
        return (i == 0)
    elif len(shares) == 4:
        return (i <= 1)
    elif len(shares) == 5:
        return (i <= 1)
    else:
        return (i < len(shares) - 2)


def getpackage(prj, pkg_name, default_order=None):
    ret = None
    logging.info("finding pkg:%s" % pkg_name)
    print("finding pkg:%s" % pkg_name)
    if 'packages' not in prj.keys() or len(prj['packages']) == 0:
        logging.info("no packages")
        return None
    for pkg in prj['packages']:
        if 'package' not in pkg.keys():
            logging.info('no package in pkg:%s' % pkg)
            continue
        logging.debug("current pkg:%s" % pkg['package'])
        mm = splitpkg(pkg_name)
        # print(mm,pkg['package'])
        if len(mm) > 0 and issamepackage(mm[0], pkg['package']):
            logging.info("got package:%s" % mm[0])
            logging.info(pkg)
            ret = pkg
            if len(mm) > 1 and 'mshares' in pkg.keys():
                logging.info("finding package2:%s" % mm[1])
                for pkg2 in pkg['mshares']:
                    if 'package2' in pkg2.keys():
                        if mm[1] == pkg2['package2']:
                            logging.info("got package2:%s" % mm[1])
                            ret = pkg2
                            # ret['mshares'] = pkg2['mshares']
                            break
                    else:
                        logging.info("no package2")
            else:
                logging.info("no second level:%s" % mm)
        else:
            pass
    if ret is None:
        logging.info("find no package:%s" % pkg_name)
    else:
        logging.info("found package:%s" % ret)
    if ret is None and default_order is not None and len(prj['packages']) >= default_order:
        if 'mshares' not in prj['packages'][default_order - 1].keys():
            print("no mshares")
        ret = prj['packages'][default_order - 1]
        # ret['mshares'] = prj['packages'][default_order-1]['mshares']
    return ret


def getpackage_back(prj, pkg_name, default_order=None):
    ret = None
    print(pkg_name)
    if 'packages' not in prj.keys() or len(prj['packages']) == 0:
        return None
    for pkg in prj['packages']:
        if 'package' not in pkg.keys():
            logging.info('no package in pkg:%s' % pkg)
            continue
        logging.debug(pkg['package'])
        mm = splitpkg(pkg_name)
        if issamepackage(pkg['package'], pkg_name):
            ret = {}
            ret['budget'] = getpackagebudget(pkg)
            if 'mshares' not in pkg.keys() and 'kshares' in pkg.keys():
                if len(pkg['kshares']) == 1:
                    ret['shares'] = pkg['kshares']
            elif 'mshares' not in pkg.keys():
                ret['shares'] = []
            elif len(pkg['mshares']) > 1:
                ret['shares'] = pkg['mshares']
            else:
                ret['shares'] = pkg['mshares']  # change from []
            break
        elif len(mm) > 0 and issamepackage(mm[0], pkg['package']):
            ret = {}
            if len(mm) > 1:
                for pkg2 in pkg['mshares']:
                    if mm[1] == pkg2['package2']:
                        ret['shares'] = pkg2['mshares']
        else:
            logging.info("find no package:%s" % pkg_name)
    if ret is None and default_order is not None and len(prj['packages']) >= default_order and 'mshares' in \
            prj['packages'][default_order - 1].keys():
        ret = {}
        ret['shares'] = prj['packages'][default_order - 1]['mshares']
    return ret


def process_non_package_noshare(prj, info):
    logging.info("process_non_package_noshare")
    ret = False
    if 'list' not in info.keys():
        logging.info("no list in info")
        return ret
    ilist = info['list']
    for item in ilist:
        objs = item['objs']
        for obj in objs:
            if 'candidate' not in obj.keys():
                continue
            prj['second_party'] = obj
            ret = True
    return ret


def process_non_package_emptyshare(prj, info):
    logging.info("process_non_package_emptyshare")
    print("not handle.just skip")
    return False
    ret = False
    ilist = info['shares']
    for item in ilist:
        if 'candidate' not in item.keys():
            continue
        prj['second_party'] = item
        ret = True
        break
    return ret


def process_non_package_withshare(prj, info):
    logging.info("process_non_package_withshare")
    ret = False
    if 'shares' not in info.keys():
        return ret
    ilist = info['shares']
    # already has the candidates
    if 'second_party' in prj.keys():
        return True
        for second_party in prj['second_party']:
            # TODO bid or not?
            pass
    else:
        prj['second_party'] = []
    i = 0
    for item in ilist:
        if 'share' not in item.keys():
            item['bid'] = getbid(i, ilist)
        else:
            item['bid'] = True
        # if the ner_type is not in items:
        if 'ner_type' not in item.keys():
            prj['second_party'].append(item)
            continue
        # if more then one bid, then it should be a org.
        if i > 0:
            if item['ner_type'] == 'ORG':
                prj['second_party'].append(item)
        else:
            if item['ner_type'] == 'LOC':
                if len(ilist) > 1:
                    pass
                else:
                    prj['second_party'].append(item)
            else:
                prj['second_party'].append(item)
        # prj['second_party'].append(item)
        ret = True
        i += 1
    return ret


def getshares(prj):
    shares = None
    ilist = prj['list']
    for item in ilist:
        if 'keys' in item.keys():
            pass
        if 'objs' in item.keys():
            for obj in item['objs']:
                if 'shares' in obj.keys():
                    shares = obj['shares']
                    break
    return shares


def process_shares(prj, info):
    print("processing shares")
    print(prj['shares'])
    print(info['shares'])
    shares = prj['shares']  # getshares(prj)
    for share in shares:
        if 'share' in share.keys() and 'share2' in share.keys():
            if share['share'] > 1:
                share['budget'] = share['share']
                share['share'] = share['share2']
                share.pop('share2')
    if shares is not None:
        lastobj = None
        if len(shares) > 0:
            lastobj = shares[0]
        else:
            lastobj = {}
            if 'budget' not in lastobj.keys():
                lastobj['budget'] = prj['budget']
        for i in range(len(info['shares'])):
            if len(shares) > i:
                if 'result' not in shares[i].keys():
                    shares[i]['result'] = info['shares'][i]
                lastobj = shares[i]
            else:
                nshare = {}
                nshare['share'] = 0
                nshare['bid'] = False
                # nshare['budget'] = lastobj['budget']
                nshare['result'] = info['shares'][i]
                shares.append(nshare)
        return True
    return False


def process_package(prj, info):
    logging.info("process package")
    pkg_found = False
    ilist = info['list']
    iorder = 0
    for item in ilist:
        if item is None:
            print("empty item in list")
            continue
        iorder += 1
        if 'package' in item.keys():
            pkg_name = item['package']
            if pkg_name == '':
                iorder -= 1
                continue
            pkg = getpackage(prj, pkg_name, iorder)
            if pkg:
                logging.info("found pkg:%s" % pkg)
                # TODO
                if 'mshares' not in pkg.keys():
                    print("n/a shares")
                    pkg['mshares'] = []
                if len(pkg['mshares']) == 0:
                    print("empty shares")
                pkg_found = True
                shares = None
                if isinstance(pkg['mshares'], list) and len(pkg['mshares']) > 0 and 'mshares' in pkg['mshares'][
                    0].keys():
                    shares = pkg['mshares'][0]['mshares']
                else:
                    shares = pkg['mshares']
                lastobj = None
                for i in range(len(item['mshares'])):
                    sc = item['mshares'][i]
                    if len(shares) > i:
                        shares[i]['result'] = sc
                        shares[i]['bid'] = True
                        lastobj = shares[i]
                    else:
                        nshare = {}
                        nshare['result'] = sc
                        if 'share' in sc.keys() and sc['share'] > 0:
                            nshare['bid'] = True
                        else:
                            nshare['bid'] = getbid(i, item['mshares'])
                        shares.append(nshare)
            else:
                logging.info("find no package in prj:%s" % pkg_name)
                if 'tmp_packages' not in prj.keys():
                    prj['tmp_packages'] = []
                prj['tmp_packages'].append(item)
            continue

        if 'keys' in item.keys() and item['keys'] is not None:
            logging.debug("found keys:%s" % item['keys'])
            if checkfield(KEYWORDS_PM, item['keys']):
                logging.info("keywords found in table:%s" % item.keys())
                continue
        elif pkg_found:
            logging.info("already has packages!skip:%s" % item)
            continue
        objs = None
        if 'objs' in item.keys():
            objs = item['objs']
        else:
            logging.info("process package in else")
            if 'package' not in item.keys():
                print("no package in item:%s" % item)
                continue
            obj = item
            if 'package' not in obj.keys() and 'shares' in obj.keys():
                shares = getshares(prj)
                if shares is not None:
                    lastobj = None
                    if len(shares) > 0:
                        lastobj = shares[0]
                    else:
                        lastobj = {}
                        if 'budget' not in lastobj.keys():
                            lastobj['budget'] = obj['budget']
                    for i in range(len(obj['shares'])):
                        sc = obj['shares'][i]
                        if len(shares) > i:
                            shares[i]['result'] = obj['shares'][i]
                            shares[i]['bid'] = True
                            lastobj = shares[i]
                        else:
                            nshare = {}
                            nshare['budget'] = lastobj['budget']
                            nshare['result'] = obj['shares'][i]
                            if 'share' in sc.keys() and sc['share'] > 0:
                                nshare['bid'] = True
                            else:
                                nshare['bid'] = getbid(i, obj['shares'])
                            # nshare['bid'] = (i == 0)
                            shares.append(nshare)
                    pkg_found = True
                continue
            pkg_found = True
            pkg_name = obj['package']
            pkg = getpackage(prj, pkg_name, iorder)
            if pkg is not None:
                shares = pkg['shares']
                lastobj = None
                if len(shares) > 0:
                    lastobj = shares[0]
                else:
                    lastobj = {}
                    if 'budget' not in lastobj.keys():
                        lastobj['budget'] = pkg['budget']
                for i in range(len(obj['mshares'])):
                    if len(shares) > i:
                        shares[i]['result'] = obj['mshares'][i]
                        shares[i]['bid'] = True
                        lastobj = shares[i]
                    else:
                        nshare = {}
                        if 'budget' in lastobj.keys():
                            nshare['budget'] = lastobj['budget']
                        nshare['result'] = obj['mshares'][i]
                        nshare['bid'] = getbid(i, obj['mshares'])
                        shares.append(nshare)
                # if len(pkg['shares']) == 0:
                #    pkg['shares'] = shares
            else:
                print("no pkg found:%s" % pkg_name)
                print(prj)
            continue
        iiorder = 0
        for obj in objs:
            iiorder += 1
            if 'package' not in obj.keys():
                print("no package in obj:%s" % obj)
                break
            if 'mshares' not in obj.keys():
                print("no mshares in obj:%s" % obj)
            pkg_found = True
            pkg_name = obj['package']
            if pkg_name == '':
                print("pkg_name is null")
                iiorder -= 1
                continue
            pkg = getpackage(prj, pkg_name, iiorder)
            if pkg:
                logging.info("found package for:%d%s\n%s" % (iiorder, obj, pkg))
                if 'mshares' not in pkg.keys():
                    if 'mshares' not in obj.keys():
                        logging.info("no mshares found in obj and pkg")
                        pkg['result'] = obj
                        continue
                    else:
                        pkg['mshares'] = []
                else:
                    if 'mshares' not in obj.keys():
                        # TODO
                        for pm in pkg['mshares']:
                            pm['result'] = obj
                        continue
                shares = pkg['mshares']
                lastobj = None
                for i in range(len(obj['mshares'])):
                    if len(shares) > i:
                        shares[i]['result'] = obj['mshares'][i]
                        shares[i]['bid'] = True
                        lastobj = shares[i]
                    else:
                        nshare = {}
                        # nshare['budget'] = lastobj['budget']
                        nshare['result'] = obj['mshares'][i]
                        nshare['bid'] = getbid(i, obj['mshares'])
                        shares.append(nshare)
            else:
                logging.info("no package found in prj but in info:%s" % pkg_name)
                print("CCCCCCDDDDDD")
                if 'tmp_packages' not in prj.keys():
                    prj['tmp_packages'] = []
                prj['tmp_packages'].append(obj)
        if not pkg_found:
            if 'shares' in prj.keys() and len(prj['shares']) > 0:
                # TODO SHARES
                logging.info("setting shares")
                print("setting shares")
                info['shares'] = objs
            elif 'tmp_packages' not in prj.keys() or len(prj['tmp_packages']) == 0:
                pkgs = []
                pkg = {}
                pkg['package'] = 'x'
                pkg['mshares'] = objs
                # pkg_found  = True
                pkgs.append(pkg)
                prj['tmp_packages'] = pkgs
            else:
                if 'mshares' not in prj['tmp_packages'][0].keys():
                    logging.error("should not reach here! mshare is none%s" % prj)
                    prj['tmp_packages'][0]['mshares'] = []
                prj['tmp_packages'][0]['mshares'].extend(objs)
    if 'shares' in info.keys() and len(info['shares']) > 0:
        if not pkg_found:
            logging.info("processing shares")
            pkg = getdefaultpkg(prj)
            if pkg:
                pkg_found = True
                shares = pkg['mshares']
                lastobj = None
                for i in range(len(info['shares'])):
                    if len(shares) > i:
                        shares[i]['result'] = info['shares'][i]
                        shares[i]['bid'] = True
                        lastobj = shares[i]
                    else:
                        nshare = {}
                        nshare['result'] = info['shares'][i]
                        nshare['bid'] = getbid(i, info['shares'])
                        shares.append(nshare)
    if 'tmp_packages' in prj.keys():
        prj['packages'] = prj.pop('tmp_packages')
        pkg_found = True
    return pkg_found


def getcity(prj):
    text1 = prj['project_name']
    text = ""
    ret = None
    if 'first_party' in prj.keys() and prj['first_party'] is not None:
        text = prj['first_party']
    for item in datagram.CITY:
        if text.find(item) >= 0:
            ret = item
            break
        elif text1.find(item) >= 0:
            ret = item
            break
    return ret


def getprovince(prj):
    text1 = prj['project_name']
    text = ""
    ret = None
    if 'first_party' in prj.keys() and prj['first_party'] is not None:
        text = prj['first_party']
    for item in datagram.PROVINCE:
        if text.find(item) >= 0:
            ret = item
            break
        elif text1.find(item) >= 0:
            ret = item
            break
    if ret is None and prj['city'] is not None:
        for key, val in datagram.PCINDEX.items():
            if prj['city'] in val:
                ret = key
                break
    return ret


def checkmodify(title):
    str1 = '(变更|更改)'
    m = re.findall(str1, title)
    if len(m) > 0:
        return True
    return False


def loadtail(prj, info):
    prj['guild_id'] = info['guild_id']
    prj['site'] = info['site']
    prj['purchase_method'] = info['purchase_method']
    prj['business_type'] = info['business_type']
    prj['minor_business_type'] = info['minor_business_type']


def namecompare(name1, name2):
    n1 = name1.replace("（", "").replace("）", "").replace("(", "").replace(")", "")
    n2 = name2.replace("（", "").replace("）", "").replace("(", "").replace(")", "")
    return n1 == n2


g_counts = 0


def parselist(infolist, seqmode=True):
    print('prjutiles.py-----813---infolist', infolist)
    global g_counts
    todolist = []
    prj = {}
    i = 0
    prj['project_name'] = None
    prj['first_open_time'] = None
    prj['last_open_time'] = None
    prj['first_bid_time'] = None
    prj['last_bid_time'] = None
    prj['reg_end_date'] = None
    prj['enroll_date'] = None
    prj['budget'] = 0
    prj['budget2'] = 0
    prj['packages'] = []
    # prj['shares'] = []
    prj['broker'] = None
    prj['status'] = 'start'
    prj['first_party'] = None
    prj['stype'] = 0
    prj['infolist'] = []
    prj['attachments'] = []
    prj['project_seq_name'] = None
    print("prjutils----835-----list size of info:%d" % len(infolist))

    pprint.pprint(infolist)
    for info in infolist:
        # 招标
        if seqmode:
            if prj['project_name'] is not None and not namecompare(info['project_name'], prj['project_name']):
                print("project_name is diff!current:%s expected:%s" % (info['project_name'], prj['project_name']))
                todolist.append(info)
                continue
        else:
            if prj['project_seq_name'] is not None and not namecompare(
                    ztbutils.process_biaoex(info['title'], False, True, False), prj['project_seq_name']):
                print("project_name is diff!current:%s expected:%s" % (info['title'], prj['project_seq_name']))
                todolist.append(info)
                continue

        logging.debug("info..............")
        logging.info(info['title'])
        logging.info(info)
        prj['infolist'].append(info['infoId'])
        prj['attachments'].extend(info['attachments'])
        if info['stype'] > prj['stype']:
            prj['stype'] = info['stype']

        if prj['budget'] == 0:
            prj['budget'] = getbudget(info)
        if prj['budget2'] == 0:
            prj['budget2'] = prj['budget']

        if prj['project_seq_name'] is None:
            prj['project_seq_name'] = ztbutils.process_biaoex(info['title'], False, True, False)
        if prj['project_name'] is None and info['project_name'] is not None:
            prj['project_name'] = info['project_name']
        if 'first_party' in info.keys() and info['first_party'] is not None and prj['first_party'] is None:
            prj['first_party'] = info['first_party']
        if 'broker' in info.keys() and info['broker'] is not None and prj['broker'] is None:
            prj['broker'] = info['broker']

        loadtail(prj, info)

        if info['type'] == '0':
            if 'list' in info.keys() and info['reg_end_date'] is None:
                for pkg in info['list']:
                    if checktablename(pkg, KEYWORDS_TBN_BID):
                        g_counts += 1
                        print("%d info is 1:%s" % (g_counts, info['title']))
                        info['type'] = '1'
                        break

        if info['type'] == '-1':
            prj['status'] = 'fail'
        elif info['type'] == '0':
            """
            if prj['status'] == 'init':
                logging.info("skip the same type 0 info")
                continue
            """
            if info['reg_start_date'] is not None:
                prj['reg_start_date'] = info['reg_start_date']
            if info['reg_end_date'] is not None:
                prj['reg_end_date'] = info['reg_end_date']
            if info['enroll_date'] is not None:
                prj['enroll_date'] = info['enroll_date']

            tmpbudget = getbudget(info)
            if tmpbudget != 0 and tmpbudget != prj['budget']:
                prj['budget'] = tmpbudget
            tmpbudget = info['budget2']
            if tmpbudget != 0 and tmpbudget != prj['budget2']:
                prj['budget2'] = tmpbudget

            if prj['status'] not in ['ok', 'final']:
                prj['status'] = 'init'
            else:
                logging.error("reopen project:%s", info['title'])
                continue
            prj['last_open_time'] = info['issue_time']
            if prj['first_open_time'] is None:
                prj['first_open_time'] = info['issue_time']
            if 'shares' in info.keys() and len(info['shares']) > 0:
                prj['shares'] = info['shares']
            if 'packages' in prj.keys() and len(prj['packages']) > 0:
                logging.info("skip the type 0 info since already has packages")
                continue
            for pkgs in info['list']:
                if pkgs is None:
                    print("empty pkgs")
                    continue
                # terry add 20191009
                if 'type' in pkgs.keys() and pkgs['type'] == 'normal':
                    logging.info("this is a regular table, skip")
                    continue
                # terry add 20190828 to skip the fake table
                # not handle the empty keys
                if 'keys' in pkgs.keys() and pkgs['keys'] is not None:
                    if checkfield(KEYWORDS_PM, pkgs['keys']):
                        print("keywords found in table:%s" % pkgs['keys'])
                        continue
                # if 'type' not in info.keys() and 'shares' in info.keys() and 'list' in info.keys():
                #    prj['shares'] = pkgs['objs']
                if 'objs' in pkgs.keys() and len(pkgs['objs']) > 0:
                    if len(pkgs['objs']) == 1:
                        pkg = pkgs['objs'][0]
                        if 'package' in pkg.keys():
                            if not checkduplicate(prj['packages'], pkg):
                                prj['packages'].append(pkg)
                        logging.info("append one obj")
                        obj = pkgs['objs'][0]
                        if 'mshares' in obj.keys():
                            prj['shares'] = obj['mshares']
                    else:
                        logging.info("appending package")
                        """
                        if len(prj['packages']) > len(pkgs['objs']):
                            print("already has packages:%s" % prj['packages'])
                            #prj['packages'] = []
                            continue
                        elif len(prj['packages']) == len(pkgs['objs']):
                            b1 = getpackagesbudget(prj['packages']) 
                            b2 = getpackagesbudget(pkgs['objs'])
                            if b1 >= b2:
                                print("skip package:%s" % pkgs['objs'])
                                continue
                        """
                        tmpshares = []
                        for pkg in pkgs['objs']:
                            if 'package' not in pkg.keys():
                                logging.info("no package key")
                                logging.info(pkg)
                                if 'share' in pkg.keys() or checktablename(pkgs):
                                    logging.info("process share in list")
                                    if checksummary(pkg):
                                        tmpshares.append(pkg)
                                continue
                            if not checkduplicate(prj['packages'], pkg):
                                prj['packages'].append(pkg)
                        if 'shares' not in prj.keys() or len(prj['shares']) == 0:
                            prj['shares'] = tmpshares
        elif info['type'] == '1':
            if prj['status'] in ['ok', 'final'] and not checkmodify(info['title']):
                print("skip this info:%s" % info['title'])
                continue
            if prj['first_open_time'] is None:
                prj['first_open_time'] = info['issue_time']
            prj['last_bid_time'] = info['issue_time']
            if prj['first_bid_time'] is None:
                prj['first_bid_time'] = info['issue_time']
            found = False
            if 'list' in info.keys():
                found = process_package(prj, info)
                print("prjutils----984-----after process package:%s" % prj)
                print("prjutils----985-----found----------", found)
            if not found and 'shares' in prj.keys() and len(prj['shares']) > 0:
                found = process_shares(prj, info)
            if not found:
                if 'list' in info.keys() and len(info['list']) > 0:
                    prj['shares'] = info['list'][0]['objs']
                    lastitem = prj['shares'][len(prj['shares']) - 1]
                    if 'candidate' in lastitem.keys():
                        if 'candidate' in lastitem.keys() and lastitem['candidate'][0:2] in ["总计", "合计"]:
                            print("remove the last share:%s" % lastitem['candidate'])
                            prj['shares'].remove(lastitem)
                        for share in prj['shares']:
                            # TODO
                            share['result'] = {}
                            for key, val in share.items():
                                share['result'][key] = val
                        found = True
            if not found:
                if 'shares' in info.keys():
                    found = process_non_package_withshare(prj, info)
                else:
                    found = process_non_package_emptyshare(prj, info)
            if not found:
                found = process_non_package_noshare(prj, info)
            if not found:
                if 'tmp_party' in info.keys():
                    prj['second_party'] = info['tmp_party']['candidate']

            if found:
                if prj['status'] != 'ok':
                    prj['status'] = 'ok'
                if info['title'].find('结果') >= 0:
                    prj['status'] = 'final'

    prj['city'] = getcity(prj)
    prj['province'] = getprovince(prj)
    print('prjutils---------1025---prj')
    pprint.pprint(prj)
    return prj, todolist


def checkcandidate(share):
    ret = False
    candidate = ''
    if 'candidate2' in share.keys():
        candidate = share['candidate2'].strip()
    elif 'candidate' in share.keys():
        candidate = share['candidate'].strip()
    elif 'org' in share.keys():
        candidate = share['org'].strip()
    if candidate not in ['', '/', '-', '小计', '合总', '总计']:
        ret = True
    return ret


def dumpinfo(info):
    # TODO
    pass


# TODO
def dumpprj_summary(prj):
    pass


def sharecheck(share):
    text = None
    ner_type = None
    if 'candidate2' in share.keys():
        text = share['candidate2']
    elif 'candidate' in share.keys():
        text = share['candidate']
    elif 'org' in share.keys():
        text = share['org']
    if 'ner_type' in share.keys():
        ner_type = share['ner_type']
    return ztbutils.nerfilter(text, ner_type)


def firstpartycheck(prj, share):
    name = ""
    if 'candidate2' in share.keys():
        name = share['candidate2']
    elif 'candidate' in share.keys():
        name = share['candidate']
    elif 'org' in share.keys():
        name = share['org']
    first_party = prj['first_party']
    if first_party is None:
        first_party = ''
    if first_party == name:
        return False
    if len(first_party) >= 4 and len(name) >= 4:
        if first_party[:4] == name[:4]:
            print("check:%s %s" % (first_party, name))
            return False
    if len(first_party) >= len(name):
        if first_party.endswith(name):
            return False
    first_party = prj['broker']
    if first_party is None:
        first_party = ''
    if first_party == name:
        return False
    if len(first_party) >= 4 and len(name) >= 4:
        if first_party[:4] == name[:4]:
            return False
    # 中国移动－－》中国铁塔－－》中国电信
    if len(name) == 4 and len(first_party) >= 4:
        if name[:3] == first_party[0:3]:
            return False
    # 三亚市分公司
    if len(name) == 6 or len(name) == 5:
        if name.endswith('市分公司'):
            return False
        if name.endswith('分公司'):
            return False
    return True


def dumpbiaoduan(prj):
    text = ''
    if 'packages' in prj.keys() and len(prj['packages']) > 0:
        i = 0
        for pkg in prj['packages']:
            if 'package' in pkg.keys():
                if pkg['package'] not in KEYWORDS_HJ:
                    i += 1
        if i < len(prj['packages']):
            text += '1\t' + str(i) + '\t'
        else:
            text += '1\t' + str(len(prj['packages'])) + '\t'
    else:
        text += '0\t0\t'
    return text


def dumptail(prj):
    text = ""
    text += str(prj['guild_id']) + '\t'
    text += prj['purchase_method'] + '\t'
    text += prj['site'] + '\t'
    text += str(prj['business_type']) + '\t'
    text += str(prj['minor_business_type']) + '\t'
    text += dumpbiaoduan(prj)
    if 'url' in prj.keys():
        text += prj['url']
    else:
        pass
        # text += db2mongo.geturl(prj['project_name'], prj['first_open_time'])
        text += db2mongo.URL + str(prj['infolist'][0]) + '\t'
    text += str(prj['infolist']) + '\t'
    text += str(len(prj['attachments']))

    return text


def dumpprj(prj):
    # if prj['status'] != 'init':
    #    return ''
    text = ""
    text += str(prj['project_name']) + '\t'
    if 'budget2' in prj.keys():
        text += str(prj['budget']) + '\t' + str(prj['budget2']) + '\t'
    else:
        text += str(prj['budget']) + '\t' + str(prj['budget']) + '\t'
    text += str(prj['first_open_time']) + '\t'
    text += str(prj['province']) + '\t'
    text += str(prj['city']) + '\t'
    text += str(prj['first_party']) + '\t'
    if prj['first_party'] != prj['broker']:
        text += str(prj['broker']) + '\t'
    else:
        text += '\t'
    text += str(prj['reg_end_date']) + '\t'
    text += str(prj['enroll_date']) + '\t'
    text += dumptail(prj)
    text += '\n'
    return text


str_can2 = "(第[1234567890一二三四五六七八九十]{1,})名?(中标|中选)?候?选?人?[:： ](.*)"
str_can1 = "((第[1234567890一二三四五六七八九十]{1,})(名|((中标|中选)?候?选?人)))"


def getcan(candidate):
    ret = candidate
    m1 = re.findall(str_can2, candidate)
    if len(m1) > 0:
        ret = m1[0][2]
    else:
        m1 = re.findall(str_can1, candidate)
        if len(m1) > 0:
            ret = ''
    return ret


def getcandidate(share):
    candidate = ''
    if 'candidate2' in share.keys():
        candidate = getcan(share['candidate2'])
    if (candidate == '' or candidate.find('公司') < 0) and 'candidate' in share.keys():
        candidate = getcan(share['candidate'])
    if candidate == '' and 'org' in share.keys():
        candidate = getcan(share['org'])
    if candidate.startswith("\"") and not candidate.endswith("\""):
        candidate = candidate[1:]
    return candidate


def dumpshare(prj, pkg, share, i, icounts):
    print("prjutils----1185------dumpshare:%s" % share)
    if not sharecheck(share):
        return ''
    if not firstpartycheck(prj, share):
        return ''
    text = ""
    text += str(prj['project_name']).replace('"', '') + '\t'
    if 'budget2' in prj.keys():
        text += str(prj['budget']) + '\t' + str(prj['budget2']) + '\t'
    else:
        text += str(prj['budget']) + '\t' + str(prj['budget']) + '\t'
    text += str(prj['first_open_time']) + '\t'
    text += str(prj['province']) + '\t'
    text += str(prj['city']) + '\t'
    text += str(prj['first_party']) + '\t'
    if prj['first_party'] != prj['broker']:
        text += str(prj['broker']) + '\t'
    else:
        text += '\t'
    text += str(prj['reg_end_date']) + '\t'
    text += str(prj['enroll_date']) + '\t'
    text += str(prj['last_bid_time']) + '\t'
    pkg_name = ''
    if 'package' in pkg.keys():
        pkg_name = pkg['package']
        text += pkg['package'] + '\t'
    else:
        text += '\t'
    if 'budget' in pkg.keys():
        text += str(pkg['budget']) + '\t'
    else:
        text += '\t'

    text += getcandidate(share) + '\t'

    ishare = 0
    if 'share' in share.keys():
        ishare = share['share']
        text += str(share['share']) + '\t'
    else:
        text += '\t'
    if 'bid' in share.keys():
        if share['bid']:
            if pkg_name == 'x':
                ibid = runxrule(i, icounts, ishare, prj)
                if ibid:
                    text += '1\t'
                else:
                    text += '0\t'
            else:
                text += '1\t'
            # text += '1\t'
        else:
            text += '0\t'
    elif prj['stype'] == 0:
        if 'share' in share.keys() and share['share'] > 0:
            text += '1\t'
        else:
            ibid = runxrule(i, icounts, ishare, prj)
            if ibid:
                text += '1\t'
            else:
                text += '0\t'
            # text += '0\t'
    else:
        text += '1\t'
    if 'budget' in share.keys():
        text += str(share['budget']) + '\t'
    else:
        text += '\t'
    if 'share' in share.keys() and 'budget' in share.keys():
        text += str(share['share'] * share['budget']) + '\t'
    elif 'share' in share.keys() and 'budget' in pkg.keys():
        text += str(share['share'] * pkg['budget']) + '\t'
    else:
        text += '\t'
    if 'discount' in share.keys():
        text += str(share['discount']) + '\t'
    else:
        text += '\t'
    text += dumptail(prj)
    text += "\n"
    return text


def checkshares(shares, share, pos):
    sharescounts = len(shares)
    if sharescounts == 1:
        return True
    if 'ner_type' in share.keys():
        if share['ner_type'] == 'PER':
            return False
    return sharecheck(share)


def dumpmshares(prj, pkg, pkg2):
    print("dumpmshares")
    text = ""
    for share in pkg2['mshares']:
        # print(share)
        # if 'result' not in share.keys():
        #     continue
        # if not sharecheck(share['result']):
        #     continue
        # if not firstpartycheck(prj, share['result']):
        #     continue
        text += str(prj['project_name']).replace('"', '') + '\t'
        if 'budget2' in prj.keys():
            text += str(prj['budget']) + '\t' + str(prj['budget2']) + '\t'
        else:
            text += str(prj['budget']) + '\t' + str(prj['budget']) + '\t'
        text += str(prj['first_open_time']) + '\t'
        text += str(prj['province']) + '\t'
        text += str(prj['city']) + '\t'
        text += str(prj['first_party']) + '\t'
        if prj['first_party'] != prj['broker']:
            text += str(prj['broker']) + '\t'
        else:
            text += '\t'
        text += str(prj['reg_end_date']) + '\t'
        text += str(prj['enroll_date']) + '\t'
        text += str(prj['last_bid_time']) + '\t'
        if 'package2' in pkg2.keys():
            text += pkg['package'] + pkg2['package2'] + '\t'
        else:
            text += pkg['package'] + '\t'

        text += getcandidate(share['result']) + '\t'

        if 'share' in share['result'].keys():
            text += str(share['result']['share']) + '\t'
            if share['result']['share'] > 0:
                text += '1\t'
            else:
                text += '0\t'
            if 'budget' in share['result'].keys():
                text += str(share['result']['budget']) + '\t'
            else:
                text += '\t'
            if 'budget' in share.keys():
                text += str(share['result']['share'] * share['budget']) + '\t'
            else:
                text += '\t'
        elif 'share' in share.keys():
            text += str(share['share']) + '\t'
            if share['share'] > 0:
                text += '1\t'
            else:
                text += '0\t'
            if 'budget' in share['result'].keys():
                text += str(share['result']['budget']) + '\t'
            else:
                text += '\t'
            if 'budget' in share.keys():
                text += str(share['share'] * share['budget']) + '\t'
            else:
                text += '\t'
        elif 'bid' in share['result'].keys():
            if share['result']['bid']:
                text += '1\t'
                text += '1\t'
                text += '0\t'
                text += '0\t'
        else:
            text += '\t'
            text += '\t'
            text += '\t'
            text += '\t'
        if 'discount' in share['result'].keys():
            text += str(share['result']['discount']) + '\t'
        else:
            text += '\t'
        text += dumptail(prj)
        text += "\n"
    return text


def runxrule(i, icounts, ishare, prj):
    print("run xrule:%d %d" % (i, icounts))
    if prj['stype'] == 1:
        return True
    if ishare > 0:
        return True
    if icounts <= 3:
        return (i <= 1)
    if icounts <= 4:
        return ((icounts - i) >= 2)
    elif icounts == 5:
        return ((icounts - i) >= 3)
    else:
        return ((icounts - i) >= 2)


def dumppackages(prj):
    print("prjutils------1375------dumppackages")
    print(prj)
    logging.info("dumpping packages")
    logging.info(prj)
    text = ""
    for pkg in prj['packages']:

        if 'mshares' not in pkg.keys():
            logging.info("mshares not in pkg:%s" % pkg)
            if 'result' in pkg.keys():
                text += dumpshare(prj, pkg, pkg['result'], 1, 1)
            continue
        i = 0
        icounts = len(pkg['mshares'])
        for pkg2 in pkg['mshares']:
            i += 1
            if 'mshares' not in pkg2.keys():
                logging.info("mshares not in pkg2:%s" % pkg2)
                print("prjutils ----- 1456-----mshares not in pkg2:%s" % pkg2)
                if 'result' not in pkg2.keys():
                    logging.info('result not in share keys')
                    print('prjutils ----- 1459----result not in share keys')
                    if 'candidate' in pkg2.keys() or 'org' in pkg2.keys():
                        # SKIP the wrong candidates
                        if i < len(pkg['mshares']):
                            if checkcandidate(pkg2):
                                pass
                            if 'bid' in pkg2.keys() and pkg2['bid']:
                                pass
                            elif 'ner_type' in pkg2.keys() and pkg2['ner_type'] != 'ORG':
                                continue
                            elif 'type' in pkg2.keys() and pkg2['type'] != '中选':
                                continue
                        # only one candidate
                        if i == 1 and i == len(pkg['mshares']):
                            pkg2['bid'] = True
                        text += dumpshare(prj, pkg, pkg2, i, icounts)
                        # print("prjutils ----- 1479----",text)
                        # ddict = {}
                        # ddict['prj'] = prj
                        # ddict['pkg'] = pkg
                        # ddict['pkg2'] = pkg2
                        # ddict['i'] = i
                        # ddict['icounts'] = icounts
                        # print(ddict)

                        continue
                    else:
                        continue
                presult = pkg2['result']
                if i < len(pkg['mshares']):
                    if checkcandidate(presult):
                        pass
                    if 'bid' in pkg2.keys() and pkg2['bid']:
                        pass
                    elif 'ner_type' in presult.keys() and presult['ner_type'] != 'ORG':
                        continue
                    elif 'type' in presult.keys() and presult['type'] != '中选':
                        # TODO
                        continue
                share = pkg2
                # if not sharecheck(share['result']):
                #     continue
                # if not firstpartycheck(prj, share['result']):
                #     continue
                text += str(prj['project_name']) + '\t'
                if 'budget2' in prj.keys():
                    text += str(prj['budget']) + '\t' + str(prj['budget2']) + '\t'
                else:
                    text += str(prj['budget']) + '\t' + str(prj['budget']) + '\t'
                text += str(prj['first_open_time']) + '\t'
                text += str(prj['province']) + '\t'
                text += str(prj['city']) + '\t'
                text += str(prj['first_party']) + '\t'
                if prj['first_party'] != prj['broker']:
                    text += str(prj['broker']) + '\t'
                else:
                    text += '\t'
                text += str(prj['reg_end_date']) + '\t'
                text += str(prj['enroll_date']) + '\t'
                text += str(prj['last_bid_time']) + '\t'
                pkg_name = ''
                if 'package' in pkg.keys():
                    pkg_name = pkg['package']
                    text += pkg['package'] + '\t'
                else:
                    text += '\t'

                budget = getpkgbudget(pkg)
                text += str(budget) + '\t'

                text += getcandidate(share['result']) + '\t'

                ishare = 0
                if 'share' in share.keys():
                    text += str(share['share']) + '\t'
                    ishare = share['share']
                elif 'share' in share['result'].keys():
                    text += str(share['result']['share']) + '\t'
                    ishare = share['result']['share']
                else:
                    text += '\t'
                if 'bid' in share.keys():
                    if share['bid']:
                        if pkg_name == 'x':
                            ibid = runxrule(i, icounts, ishare, prj)
                            if ibid:
                                ishare = 1
                                text += '1\t'
                            else:
                                text += '0\t'
                        else:
                            text += '1\t'
                            if ishare == 0:
                                ishare = 1
                    else:
                        text += '0\t'
                else:
                    text += '\t'
                    ishare = 0
                ibudget = 0
                if 'budget' in share['result'].keys():
                    ibudget = share['result']['budget']
                    text += str(ibudget) + '\t'
                else:
                    text += '\t'
                if 'budget' in share.keys():
                    ibudget = share['budget']
                    ishare = 1.0
                elif 'budget' in pkg.keys():
                    ibudget = pkg['budget']
                if ibudget is None:
                    ibudget = 0
                if ishare is None:
                    ishare = 0
                iibudget = ibudget * ishare
                text += str(iibudget) + '\t'

                if 'discount' in share['result'].keys():
                    text += str(share['result']['discount']) + '\t'
                else:
                    text += '\t'
                text += dumptail(prj)
                text += "\n"
            else:
                text += dumpmshares(prj, pkg, pkg2)
    return text


def dumpsecondparty(prj):
    print("dumpsecondparty")
    text = ""
    second_parties = []
    second_party = prj['second_party']
    if True:
        if isinstance(second_party, list):
            second_parties = second_party
        elif isinstance(second_party, dict):
            second_parties.append(second_party)
        else:
            second_parties.append({'candidate': prj['second_party'], 'bid': True})
        # TODO
        # if second_party is None
    for second_party in second_parties:
        if not sharecheck(second_party):
            continue
        if not firstpartycheck(prj, second_party):
            continue
        text += str(prj['project_name']) + '\t'
        if 'budget2' in prj.keys():
            text += str(prj['budget']) + '\t' + str(prj['budget2']) + '\t'
        else:
            text += str(prj['budget']) + '\t' + str(prj['budget']) + '\t'
        text += str(prj['first_open_time']) + '\t'
        text += str(prj['province']) + '\t'
        text += str(prj['city']) + '\t'
        text += str(prj['first_party']) + '\t'
        if prj['first_party'] != prj['broker']:
            text += str(prj['broker']) + '\t'
        else:
            text += '\t'
        text += str(prj['reg_end_date']) + '\t'
        text += str(prj['enroll_date']) + '\t'
        text += str(prj['last_bid_time']) + '\t'
        text += '\t'
        text += '\t'
        text += str(second_party['candidate']) + '\t'
        ishare = 1
        if 'share' in second_party.keys():
            text += str(second_party['share']) + '\t'
            ishare = second_party['share']
        else:
            text += '\t'
        if second_party['bid'] or prj['stype'] == 1:
            text += '1\t'
        else:
            text += '0\t'
        ibudget = 0
        if 'budget' in second_party.keys():
            text += str(second_party['budget']) + '\t'
            ibudget = second_party['budget']
        else:
            text += '\t'
        if ibudget is None:
            ibudget = 0
        if ishare is None:
            ishare = 0
        text += str(ibudget * ishare) + '\t'
        if 'discount' in second_party.keys():
            text += str(second_party['discount']) + '\t'
        else:
            text += '\t'
        text += dumptail(prj)
        text += "\n"
    return text


def dumpshares(prj):
    print("prjtils------1576------dumpshares")
    found = False
    text = ''
    if 'shares' in prj.keys():
        i = 0
        for share in prj['shares']:
            i += 1
            if 'result' not in share.keys():
                print("no result in:%s" % share)
                continue
            if not checkshares(prj['shares'], share['result'], i):
                print("invalid share:%s" % share)
                continue

            text += str(prj['project_name']) + '\t'
            if 'budget2' in prj.keys():
                text += str(prj['budget']) + '\t' + str(prj['budget2']) + '\t'
            else:
                text += str(prj['budget']) + '\t' + str(prj['budget']) + '\t'

            text += str(prj['first_open_time']) + '\t'
            text += str(prj['province']) + '\t'
            text += str(prj['city']) + '\t'
            text += str(prj['first_party']) + '\t'
            if prj['first_party'] != prj['broker']:
                text += str(prj['broker']) + '\t'
            else:
                text += '\t'
            text += str(prj['reg_end_date']) + '\t'
            text += str(prj['enroll_date']) + '\t'
            text += str(prj['last_bid_time']) + '\t'
            text += '\t'
            text += '\t'

            text += getcandidate(share['result']) + '\t'

            if 'share' in share['result'].keys():
                text += str(share['result']['share']) + '\t'
            elif 'share' in share.keys():
                text += str(share['share']) + '\t'
            else:
                text += '\t'
            if 'bid' in share.keys() and prj['stype'] == 0:
                if share['bid']:
                    text += '1\t'
                else:
                    text += '0\t'
            else:
                text += '1\t'

            if 'budget' in share.keys():
                text += str(share['budget']) + '\t'
            else:
                text += '\t'
            if 'share' in share.keys() and 'budget' in prj.keys():
                if share['share'] is not None:
                    # TODO
                    fshare = getfloat(share['share'])
                    text += str(fshare * prj['budget']) + '\t'
                else:
                    text += str(0) + '\t'
            elif 'share' in share['result'].keys() and 'budget' in prj.keys():
                if share['result']['share'] is not None:
                    fshare = getfloat(share['result']['share'])
                    text += str(fshare * prj['budget']) + '\t'
                    # text += str(share['share']) + '\t'
                else:
                    text += str(0) + '\t'
                    # text += str(share['share']) + '\t'
            else:
                text += '\t'
            if 'discount' in share['result'].keys():
                text += str(share['result']['discount']) + '\t'
            else:
                text += '\t'
            text += dumptail(prj)
            text += "\n"
            found = True
    return text, found


def dumpprj_detail(prj):
    logging.debug(prj)
    print('prjutils.py----1661---dump detail')
    print('prjutils.py----1662---', prj['status'])
    print('prjutils.py----1663---', prj['packages'], len(prj['packages']))
    print('prjutils.py----1664---')
    print(prj)
    found = False
    text = ""

    if prj['status'] not in ['ok', 'final']:
        # pass
        print('not in -----1669------')
        return ''

    if len(prj['packages']) > 0:
        text += dumppackages(prj)
        if text != '':
            found = True
        print('prjutils------1683----text')
        print(text)
        print(found)

    if len(prj['packages']) == 0 or not found:
        print('prjutils.py----1677---')
        text, found = dumpshares(prj)
        print('prjutils.py----1679---found  and  text', found)
        print(text)
    if 'second_party' in prj.keys() and not found:
        text += dumpsecondparty(prj)
        print('prjutils.py---text----1687')
        print(text)
    print('prjutils-----1774----text')
    print(text)
    print('prjutils-----1776----end')
    return text


def json2csv(prjs):
    """
    header = '项目名称\t项目总投资\t项目费用\t发布时间\t招标方\t代理\t报名时间\t投标时间\t中标时间\t标段\t中标人\t份额\t金额\t折扣'
    header2 = '项目名称\t项目总投资\t项目费用\t发布时间\t招标方\t代理\t报名时间\t投标时间'
    text = header2 + '\n'
    text_detail = header + '\n'
    """
    text = ""
    text_detail = ""
    for prj in prjs:
        text += dumpprj(prj)
        text_detail += dumpprj_detail(prj)

    return text, text_detail


def loadsprj(urls):
    obj = []
    for url in urls:
        html = requests.get(url)  # urlopen(url)
        info = json.loads(html.content)
        print(info)
        obj.append(info)
    ret = parselist(obj)
    return ret


def test(url):
    urls = url.split(' ')
    obj = loadsprj(urls)
    fp = open('test.json', 'w')
    fp.write(json.dumps(obj, default=json_default))
    fp.close()

    # text = dumpprj(obj)
    text, text2 = json2csv([obj])
    fp = open('test.csv', 'w')
    fp.write(text)
    fp.close()
    fp = open('test_detail.csv', 'w')
    fp.write(text2)
    fp.close()


def testmerge(url, itype):
    import bs4
    import requests
    from urllib.request import urlopen
    urls = url.split(' ')
    obj = {}
    obj['type'] = itype
    obj['issue_time'] = datetime.datetime.now()
    obj['list'] = []
    for url in urls:
        html = requests.get(url)  # urlopen(url)
        info = json.loads(html.content)
        for item in info:
            obj['list'].append(item)
    fp = open("test.json", 'w')
    fp.write(json.dumps(obj, default=json_default))
    fp.close()
    # print(geetbudget(obj))


def dumphead(outputdir, prefix='test'):
    header = '项目名称\t项目总投资\t项目金额\t发布时间\t省\t市\t招标方\t代理\t报名时间\t投标时间\t中标时间\t标段\t标段金额\t候选人\t中标份额\t是否中标\t报价金额\t中标金额\t折扣\t行业\t采购方式\t来源\t业务大类\t业务小类\t含标段\t标段数\t链接\tID\t附件\n'
    header2 = '项目名称\t项目总投资\t项目金额\t发布时间\t省\t市\t招标方\t代理\t报名时间\t投标时间\t行业\t采购方式\t来源\t业务大类\t业务小类\t含标段\t标段数\t链接\tID\t附件\n'
    if True:
        fp = open(os.path.join(outputdir, prefix + '.csv'), 'w')
        fp.write(header2)
        fp.close()
        fp = open(os.path.join(outputdir, prefix + 'detail.csv'), 'w')
        fp.write(header)
        fp.close()


def dumpfiles(vv, prefix='test', outputdir=''):
    print("dumpfiles")
    text, text2 = json2csv(vv)
    fp = open(os.path.join(outputdir, prefix + '.csv'), 'a')
    fp.write(text)
    fp.close()
    fp = open(os.path.join(outputdir, prefix + 'detail.csv'), 'a')
    fp.write(text2)
    fp.close()


def loaddir(dir, begin_date, targetdir=None, mdb='ztb', mset='ztb', outputdir='', seqmode=True):
    dumphead(outputdir, mset)
    vv = []
    objs = []
    uniq = []
    for root, dirs, files in os.walk(dir, True):
        for name in files:
            if not name.endswith('.txt'):
                continue
            fpath = os.path.join(root, name)
            obj = ztbutils.readjson(fpath)
            title = obj['title']  # obj['project_name']
            title = ztbutils.process_biaoex(title, False, True, seqmode)
            if title == '':
                print("null title")
                continue
            elif title in uniq:
                continue
            else:
                uniq.append(title)
            # title = zbtutils.rex(title)
            objs = ztbutils.process_mongo(title, dir, begin_date, mdb, mset)
            logging.info("processing:%s" % title)
            if len(objs) < 1:
                print("empty list")
                continue
            while len(objs) > 0:
                v, objs = parselist(objs, seqmode)
                dumpfiles([v], mset, outputdir)
                if targetdir is not None:
                    prj_name = v['project_name'].replace("/", "-").replace(' ', '').replace('\t', '')
                    if len(prj_name) >= 84:
                        prj_name = prj_name[0:77] + prj_name[len(prj_name) - 6:]
                    tfpath = os.path.join(targetdir, prj_name + ".json")
                    if os.path.isfile(tfpath):
                        print("file exists:%s" % tfpath)
                        continue
                    fp = open(tfpath, 'w')
                    try:
                        text = json.dumps(v, default=json_default)
                        fp.write(text)
                    except Exception as e:
                        logging.error(e)
                        logging.error(prj_name)
                    fp.close()
                    # vv.append(v)
        for name in dirs:
            print(os.path.join(root, name))
    # objs = readjson(filename)
    print("process out prj counts:%d" % len(uniq))
    return vv


def loadfile(filepath, dir, targetdir=None, mdb='ztb', mset='ztb', outputdir=None, seqmode=True, forcemode=False,
             attachmode=False):
    dumphead(outputdir, mset)
    vv = []
    objs = []
    uniq = []
    fp = open(filepath, 'r')
    lines = fp.readlines()
    fp.close()
    tfilepath = os.path.join(outputdir, mset + ".txt")
    tfp = open(tfilepath, 'w')
    for title in lines:
        if title.endswith('\n'):
            title = title[:len(title) - 1]
        prj_name = title.replace("/", "-").replace(' ', '').replace('\t', '')
        if len(prj_name) >= 84:
            prj_name = prj_name[0:77] + prj_name[len(prj_name) - 6:]
        # os.system("rm '%s*'" % os.path.join(dir,prj_name))
        ntitle = ztbutils.process_biaoex(title, False, True, seqmode)
        if ntitle == '':
            print("null title:%s" % title)
            tfp.write(title + '\n')
            continue
        elif len(ntitle) <= 4:
            print("short title:%s" % title)
            tfp.write(title + '\n')
    tfp.close()

    for title in lines:
        if title.endswith('\n'):
            title = title[:len(title) - 1]
        # title = ztbutils.process_biao(title)
        title = ztbutils.process_biaoex(title, False, True, seqmode)
        if title == '':
            print("null title:%s" % title)
            continue
        elif len(title) <= 4:
            print("short title:%s" % title)
            continue
        if title in uniq:
            print("duplicate:%s" % title)
            continue
        else:
            uniq.append(title)
        # title = ztbutils.rex(title)
        objs = ztbutils.process_mongo(title, dir, "1900-01-01", mdb, mset, 0, ".*", forcemode, attachmode)
        logging.info("processing:%s" % title)
        if len(objs) < 1:
            print("empty list")
            continue
        print("parselist:%d" % len(objs))
        while len(objs) > 0:
            v, objs = parselist(objs, seqmode)
            dumpfiles([v], mset, outputdir)
            if targetdir is not None:
                prj_name = v['project_name'].replace("/", "-").replace(' ', '').replace('\t', '')
                if len(prj_name) >= 84:
                    prj_name = prj_name[0:77] + prj_name[len(prj_name) - 6:]
                tfpath = os.path.join(targetdir, prj_name + ".json")
                if os.path.isfile(tfpath):
                    print("file exists:%s" % tfpath)
                    continue
                fp = open(tfpath, 'w')
                try:
                    text = json.dumps(v, default=json_default)
                    fp.write(text)
                except Exception as e:
                    logging.error(e)
                    logging.error(prj_name)
                fp.close()
    print("type change:%d " % g_counts)
    return vv


def postprocess_type(dir, mdb='ztb', mset='ztb', mode='rewrite'):
    vv = []
    objs = []
    uniq = []
    for root, dirs, files in os.walk(dir, True):
        for name in files:
            if not name.endswith('.txt'):
                continue
            fpath = os.path.join(root, name)
            obj = ztbutils.readjson(fpath)
            # if obj['reg_end_date'] is None
            if obj['type'] == '0':
                text = ztbutils.loadtext(obj['infoId'], mdb, mset)
                objtype = ztbutils.gettypefromcontent(text)
                if objtype != '0':
                    objs.append(obj['title'])
                    print("this is type:%s for:%s" % (objtype, obj['title']))
                    if mode == 'rewrite':
                        kobj = ztbutils.loadobj(obj['infoId'], mdb, mset)
                        newobj = ztbutils.process_obj(kobj, dir, objtype)
                        if newobj is not None:
                            ztbutils.dump2json(fpath, newobj)
    return objs


def postprocess_dt(dir, mdb='ztb', mset='ztb', ops=True):
    vv = []
    objs = []
    uniq = []
    for root, dirs, files in os.walk(dir, True):
        for name in files:
            if not name.endswith('.txt'):
                continue
            fpath = os.path.join(root, name)
            obj = ztbutils.readjson(fpath)
            """
            k = False
            if obj['reg_end_date'] is not None:
                if obj['reg_end_date'].find('\xa0') >= 0:
                   obj['reg_end_date'] = obj['reg_end_date'].replace('\xa0','')
                   k = True
            if obj['reg_start_date'] is not None:
                if obj['reg_start_date'].find('\xa0') >= 0:
                   obj['reg_start_date'] = obj['reg_start_date'].replace('\xa0','') 
                   k = True
            if k:
                ztbutils.dump2json(fpath, obj)
                #vv.append(obj['infoId'])
                print(obj['title'])
                continue
            """
            if obj['reg_end_date'] is None and obj['type'] == '0':
                text = ztbutils.loadtext(obj['infoId'], mdb, mset)
                objtype = ztbutils.gettypefromcontent(text)
                if objtype != '0':
                    objs.append(obj['infoId'])

            if obj['reg_end_date'] is None and obj['type'] == '0':
                if not ops:
                    if obj['infoId'] not in objs:
                        vv.append(obj['title'])
                    continue
                text = ztbutils.loadtext(obj['infoId'], mdb, mset)
                if text is None:
                    print("unable to load text:%s" % obj['title'])
                    continue
                obj['reg_start_date'], obj['reg_end_date'] = ztbutils.process_datetime2(text)
                if obj['reg_end_date'] is not None:
                    print("rewrite:%s" % fpath)
                    ztbutils.dump2json(fpath, obj)
                    vv.append(obj['infoId'])
    return vv


def dogroup(dir):
    vv = []
    objs = []
    uniq = []
    for root, dirs, files in os.walk(dir, True):
        for name in files:
            if not name.endswith('.txt'):
                continue
            fpath = os.path.join(root, name)
            obj = ztbutils.readjson(fpath)
            title = obj['title']
            obj['project_seq_name'] = ztbutils.process_biaoex(title, False, True, False)
            # ztbutils.dump2json(fpath, obj)
            vv.append(obj['infoId'])
            if obj['project_seq_name'] != ztbutils.process_biaoex(title, False, True, True):
                objs.append(
                    obj['project_seq_name'] + ":" + obj['project_name'] + ":" + ztbutils.process_biaoex(title, True,
                                                                                                        True, False))
    return objs


if __name__ == "__main__":
    cmd = sys.argv[1]
    str1 = sys.argv[2]
    str2 = None
    str3 = None
    str4 = None
    str5 = ''
    str6 = ''
    str7 = ''
    if len(sys.argv) > 8:
        str7 = sys.argv[8]
    if len(sys.argv) > 7:
        str6 = sys.argv[7]
    if len(sys.argv) > 6:
        str5 = sys.argv[6]
    if len(sys.argv) > 5:
        str4 = sys.argv[5]
    if len(sys.argv) > 4:
        str3 = sys.argv[4]
    if len(sys.argv) > 3:
        str2 = sys.argv[3]

    # # 合并
    if cmd == "merge":
        testmerge(url=str1, itype=str2)
    # # 分组
    elif cmd == 'group':
        vv = dogroup(dir=str1)
        print(vv)
    # # 重新写入
    elif cmd == 'rewrite':
        vv = postprocess_type(str1, str2, str3)
        print("processed counts:%d" % len(vv))
    # # 检查核对
    # elif cmd == 'check':
    #     vv = postprocess_type(str1,str2,str3,'')
    #     fp = open(str4,'w')
    #     for v in vv:
    #         fp.write(v + '\n')
    #     fp.close()
    # elif cmd == 'cdt':
    #     vv = postprocess_dt(str1,str2,str3,False)
    #     print("process result:%d" % len(vv))
    #     print(vv)
    # elif cmd == 'pdt':
    #     vv = postprocess_dt(str1,str2,str3)
    #     print("process result:%d" % len(vv))
    # elif cmd == "prj":
    #     loaddir(str1,str2,str3,str4,str5,str6,False)
    # # 文件
    # elif cmd == "file":
    #     loadfile(str1,str2,str3,str4,str5,str6,False)
    # elif cmd == "force":
    #     loadfile(str1,str2,str3,str4,str5,str6,False,True)
    # # 附件
    # elif cmd == "attach":
    #     loadfile(str1,str2,str3,str4,str5,str6,False,False,True) #with attachments
    # elif cmd == "bz":
    #     #"通信工程|网络维护|网络优化|ICT|通信设备"
    #     ztbutils.dump_titles(str1,str2,str3,str4,str5,int(str6),str7)
    #     #loadfile(str1,str2,str3,str4,str5,str6)
    # elif cmd == "mongo":
    #     objs = ztbutils.process_mongo(str1,str2,'1900-01-01',str3,str4,0)
    #     vv = []
    #     for obj in objs:
    #         #print(obj)
    #         if isinstance(obj,str):
    #             continue
    #     while len(objs) > 0:
    #        v,objs = parselist(objs, False)
    #        #print(v)
    #        vv.append(v)
    #     dumpfiles(vv)
    # else:
    #     test(str1)
