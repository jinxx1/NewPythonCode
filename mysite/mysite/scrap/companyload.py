import os
import json
#import company
from mysite.scrap import company

def load_cc(filepath):
    ret = []
    if filepath:
        for dir, dirs, files in os.walk(filepath):
            for f in files:
                try:
                    ret.append(f.replace('.txt',''))
                except os.error:
                    pass
    return ret

def load_from_file(fpath):
    fp = open(fpath, 'r')
    content = fp.read()
    obj = json.loads(content)
    fp.close()
    return obj
    
def load_companies(dire):
    companies = []
    cc = load_cc(dire)
    for c in cc:
        fpath = os.path.join("basic_info",c + ".txt")
        info = load_from_file(fpath)
        obj = {"name": c, "obj":info}
        companies.append(obj)
        if 'Result' not in info:
            continue
        r = info['Result']
        if 'OriginalName' not in r or r['OriginalName'] is None:
            continue
        for oname in r['OriginalName']:
            name = oname['Name']
            name = name.replace("(","（")
            name = name.replace(")","）")
            obj = {"name": name, "obj":info} 
            companies.append(obj)
    return companies

def get_company(companies,name):
    for c in companies:
        if 'name' not in c.keys():
            continue
        if c['name'] == name:
            return c['obj']
    return None

def update_company(companies,name):
    obj = None
    company.get_company_info()

    info = company.get_company_from_qcc(name)


    if info is not None:
        obj = {"name": name, "obj":info}
        companies.append(obj)
    return obj



if __name__ == "__main__":
    ret = load_companies("basic_info")
    #print(len(ret))
    print(get_company(ret, '阿里云计算有限公司'))
    print(update_company(ret, '润建股份有限公司'))
