import os
import requests
import json
import hashlib
import datetime
import time

# KEY = "2e01aed923054bb8aba78c9a6d83406f"
KEY = "b40155a182bb45e69181dfb4cc79e01b"
DTYPE = "json"
HISTORY_URL = "http://api.qichacha.com/History/GetHistorytEci"
# "9A9520EA7CC8F8FE4F584B12184C1048"
SECRETKEY = "4500312F4F1F2E097E43C90E537D5671"
BASIC_DETAILS_URL = "http://api.qichacha.com/ECIV4/GetBasicDetailsByName"


def load_company_o():
    cc = []
    fp = open("company_list.txt")
    lines = fp.readlines() 
    for line in lines:
        if len(line) > 0:
            cc.append(line.strip())
    fp.close()
    return cc 

def load_cc(filepath):
    ret = []
    if filepath:
        for dir, dirs, files in os.walk(filepath):
            for f in files:
                try:
                    print(f)
                    ret.append(f.replace('.txt',''))
                except os.error:
                    pass
    return ret

def load_company():
    return load_cc("basic_info")
    # return load_cc(r"C:\PthonCode\mysite\basic_info")

def load_db_file(companies):
    cc = []
    fp = open("company_db.txt")
    lines = fp.readlines()
    for line in lines:
        ll = line.split('\t')
        company_name = ll[0]
        ccc = ll[1]
        if int(ccc) > 5 and company_name not in companies:
            cc.append(company_name) 
    fp.close()
    return cc

def write_companyinfo(company_name, text):
    fpath = "basic_info"
    fname = os.path.join(fpath, company_name + ".txt")
    fp = open(fname, "w")
    fp.write(text)
    fp.close()
     
def get_company_info(key, dtype, keyword):
    #timespan = datetime.datetime.now()
    #tstr = timespan.strftime('%Y-%m-%d %H:%M:%S')
    tstr = int(time.time())
    ustr = KEY + str(tstr) + SECRETKEY 
    token = hashlib.md5(ustr.encode("utf8")).hexdigest().upper()
    # print('ustr-----------',ustr)
    # print('token-----------',token)
    headers = {"Token":token, "Timespan":str(tstr)}
    dict1 = {"key":key, "dtype":dtype, "keyWord": keyword}
    qstring = "key=" + key + "&dtype=" + dtype + "&keyWord=" + keyword
    url = BASIC_DETAILS_URL + "?" + qstring
    # print(url)
    resp = requests.get(url, headers = headers)
    ret = resp.content.decode("utf8")
    # print('ret-----------',ret)
    obj = json.loads(ret)
    # import pprint
    # pprint.pprint(obj)
    if obj['Status'] == '200':
        write_companyinfo(keyword, ret)
        return obj
    return None

def write_companies(companies):
    fp = open("company_list.txt", "a")
    for company_name in companies:
        fp.write(company_name)
        fp.write("\n")
    fp.close()

def main():
    print("loading company")
    companies = load_company()
    orgcompanies = []
    print(companies)
    print("loading todo")
    todo = load_db_file(companies)
    print(todo)
    newcompanies = []
    for company_name in todo:
        if company_name in orgcompanies:
            print("%s in original names, skip" % company_name)
            continue
        info = get_company_info(KEY, DTYPE, company_name) 
        if info is None:
            print("%s not found" % company_name)
            continue
        newcompanies.append(company_name)
        companyinfo = json.loads(info)
        onames = companyinfo['Result']['OriginalName']
        if onames is None:
            print("no original names")
            continue
        for name in onames:
            if name not in companies and name not in orgcompanies:
                orgcompanies.append(name['Name'])

    write_companies(orgcompanies)
    write_companies(newcompanies)

if __name__ == "__main__":
    import pprint
    company_name = '北京京盛工程勘察中心'
    info = get_company_info(KEY, DTYPE, company_name)
    pprint.pprint(info)



    exit()
    main()
