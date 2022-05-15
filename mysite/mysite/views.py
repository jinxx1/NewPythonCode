import json
import pandas as pd
from django.shortcuts import render
#import stanfordnlp
from django.http import HttpResponse
import pandas as pd
import MySQLdb
import datetime
import dateutil.parser
import time
import hashlib
import os
from mysite import settings
from mysite.scrap import wc
from mysite.scrap import companyload
from mysite.scrap import company

def string2timestamp(strValue): 
  try:     
    d = datetime.datetime.strptime(strValue, "%Y-%m-%d") 
    t = d.timetuple() 
    timeStamp = int(time.mktime(t)) 
    timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000000
    return timeStamp 
  except ValueError as e: 
    return 0

conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="xey123456",db="uxsq",charset="utf8")

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, pd._libs.tslibs.period.Period):
            return str(obj) 
        else:
            return json.JSONEncoder.default(self, obj)

#nlp = stanfordnlp.Pipeline(lang='zh')
# Create your views here.
def myview(text): 
    response = HttpResponse(text) 
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def importPage(request):
    pages_str = request.POST.json()

def nlp_analyze(request):
    company_name = ''
    nlp_text = request.GET['nlp_text']
    if nlp_text:
        doc = nlp(nlp_text)
        b_name = False
        for ii in doc.sentences[0].tokens:
            if b_name:
                company_name += ii.words[0].text
            if ii.words[0].dependency_relation == 'cop':
                b_name = True
        if company_name == '':
            company_name = nlp_text
    obj = {"company_name":company_name}
    return myview(json.dumps(obj))

companies = companyload.load_companies('basic_info')

def get_company(request):
    global companies
    obj = None
    name = request.GET.get("name")
    if name:
        obj = companyload.get_company(companies,name)
        if obj is None:
            obj = companyload.update_company(companies,name)
    ret = {}
    if obj is not None:
        ret['result'] = True
        ret['name'] = name
        ret['obj'] = obj
    else:
        ret['result'] = False
    return myview(json.dumps(ret))
 
def file_exist(fname):
    ret = False
    dpath = settings.STATICFILES_DIRS[1]
    fpath = os.path.join(dpath, fname)
    try:
        fp = open(fpath, "rb")
        fp.close()
        ret = True
    except Exception as e:
        ret = False
        print("file not exist:%s" % fpath)
    return ret
 
def get_static_url(fname):
    return settings.STATIC_NLP_URL + fname

def gen_wc(text, fname = None):
    dpath = settings.STATICFILES_DIRS[1]
    if fname is None:
        tt = time.time()
        fname = str(int(tt * 1000000)) + ".png"
    wc.wc_generate(text, dpath, fname)
    return settings.STATIC_NLP_URL + fname

csv_data = pd.DataFrame()
sql = "select a.id as infoId, guild_id as guildId, page_title as title, project_amount as projectAmount, province, city, b.abbreviation as provinceName, c.name as cityName, business_type as businessType, minor_business_type as minorBusinessType, purchase_source as paramPurchaseSource, d.site_name as purchaseSource, purchase_date as purchaseDate, job_tag as jobTag from ztbInfo as a left join cfgProvince as b on a.province = b.id left join cfgCity as c on a.city = c.id left join ztbSource as d on a.purchase_source = d.id group by a.project_id order by purchase_date desc"
db_data = pd.read_sql(sql,conn,index_col='infoId')

def read_file(filepath):
    ret = {}
    fp = open(filepath)
    lines = fp.readlines()
    for line in lines:
        items = line.split("\t")
        code = items[0]
        name = items[1]
        ret[code] = name.replace('\n','')
    fp.close()
    return ret

#provinces = read_file("cfgProvince.txt")
#cities = read_file("cfgCity.txt")
#print(provinces)
#print(cities)

def get_province_code(name):
    global provinces,cities
    print(name)
    ret = None
    for key,value in provinces.items():
        if value == name:
            ret = key
    print(ret)
    return ret
 
def pandas_data(request):
    global db_data
    jsonData = {}
    csv_path = request.GET.get('csv_path')
    paramSearchkey = request.GET.get('paramSearchkey')
    businessTypeArray = request.GET.get('businessTypeArray')
    paramSourceArray = request.GET.get('paramSourceArray')
    guildId = request.GET.get('guildId') 
    jobTagArray = request.GET.get('jobTagArray') 
    startTime = request.GET.get('startTime')
    endTime = request.GET.get('endTime')
    paramProvincesArray = request.GET.get('paramProvincesArray')
    goDeepType = request.GET.get('goDeepType')
    goDeepData = request.GET.get('goDeepData')
    goDeepLevel = request.GET.get('goDeepLevel')

    csv_data = db_data
    print(type(csv_data['purchaseDate']))
    if guildId:
        csv_data = csv_data[csv_data['guildId']==int(guildId)]
    if paramSourceArray:
        ar = json.loads(paramSourceArray)
        csv_data = csv_data[csv_data['paramPurchaseSource'].isin(ar)]
    if paramSearchkey:
        csv_data = csv_data[csv_data['title'].str.contains(paramSearchkey)]
        print(csv_data.__len__())
    if goDeepType and goDeepData:
        if goDeepType == 'businessType':
            if goDeepLevel == '1':
                csv_data = csv_data[csv_data['businessType'] == goDeepData]
        elif goDeepType == 'zbf':
            csv_data = csv_data[csv_data['purchaseSource'] == goDeepData] 
        elif goDeepType == 'area':
            if goDeepLevel == '1':
                csv_data = csv_data[csv_data['provinceName'] == goDeepData]
            pass
        elif goDeepType == 'time':
            pass
        elif goDeepType == 'jobTag':
            pass
    if businessTypeArray and businessTypeArray != '':
        jsonObj = json.loads(businessTypeArray)
        btype = []
        for obj in jsonObj:
            #print(obj['minorBusinessType'])
            btype.append(obj['minorBusinessType'])
        csv_data = csv_data[csv_data['minorBusinessType'].isin(btype)]

    #csv_data['date'] = pd.to_datetime(csv_data['purchaseDate'])
    #csv_data = csv_data.set_index('date')
    print(csv_data.info())
    if startTime:
       st = int(string2timestamp(startTime))
       #csv_data = csv_data[startTime:]
       #cvs_data = csv_data['2019-01-01':'2019-05-05']
       #csv_data.truncate(before=startTime)
       csv_data = csv_data[csv_data['purchaseDate'] >= pd.to_datetime(startTime)]
    if endTime:
       csv_data = csv_data[csv_data['purchaseDate'] <= pd.to_datetime(endTime)]

    if paramProvincesArray:
       ar = json.loads(paramProvincesArray)
       csv_data = csv_data[csv_data['province'].isin(ar)]

    #if csv_path:
    #    csv_data = pd.read_csv(csv_path, encoding='utf-8')

    if True:
        #csv_data = db_data.sort_values(by=['purchaseDate'])
        per = csv_data['purchaseDate'].dt.to_period("M")
        if goDeepType == 'time' or goDeepType == 'month' or goDeepType == 'quarter':
            per = csv_data['purchaseDate'].dt.to_period("D")
        bytime = per.value_counts()
        #bytime = csv_data.groupby(per).value_counts()
        bytime = bytime.sort_index(ascending=False)
        amount = csv_data.groupby(per)['projectAmount'].sum()
        amount = amount.sort_index(ascending=False)
        amountlist = []
        for number in amount.values.tolist():
            amountlist.append(round(number,2))
        jsonData['dateData'] = {'date': bytime.index.tolist(), 'count': bytime.values.tolist(),'amount': amountlist}
        byBussinessCount = None
        if guildId == '3':
            byBussinessCount = csv_data['jobTag'].value_counts()
        else:
            byBussinessCount = csv_data['businessType'].value_counts()
        if goDeepType == 'businessType':
            if goDeepLevel == '1':
                byBussinessCount = csv_data['minorBusinessType'].value_counts()
                print(byBussinessCount)

        byBussinessCount = byBussinessCount.sort_index(ascending=False)
        byCount = []
        for index in byBussinessCount.index.tolist():
            obj = {'name':index,'value':str(byBussinessCount[index])}
            byCount.append(obj)
        bussinessAmount = None
        if guildId == '3':
            bussinessAmount = csv_data.groupby(by=['jobTag'])['projectAmount'].sum()
        else:
            bussinessAmount = csv_data.groupby(by=['businessType'])['projectAmount'].sum()
        if goDeepType == 'businessType':
            if goDeepLevel == '1':
                bussinessAmount = csv_data.groupby(by=['minorBusinessType'])['projectAmount'].sum()
                print(bussinessAmount)

        bussinessAmount = bussinessAmount.sort_index(ascending=False)
        byAmount = []
        for index in bussinessAmount.index.tolist():
            obj = {'name':index,'value':round(bussinessAmount[index],2)}
            byAmount.append(obj)
        jsonData['business'] = {'byCount':byCount,'byAmount':byAmount}

        csv_data = csv_data.sort_values(by=['provinceName'])
        byAreaCount = csv_data['provinceName'].value_counts()
        if goDeepType == 'area':
            if goDeepLevel == '1':
                byAreaCount = csv_data['cityName'].value_counts()
                print(byAreaCount)

        #byAreaCount = byAreaCount.sort_values(ascending=False)
        byAreaCount = byAreaCount.sort_index(ascending=False)
        byAreaAmount = csv_data.groupby(by=['provinceName'])['projectAmount'].sum()
        byAreaAmount = byAreaAmount.sort_index(ascending=False)
        if goDeepType == 'area':
            if goDeepLevel == '1':
                byAreaAmount = csv_data.groupby(by=['cityName'])['projectAmount'].sum()
                print(byAreaAmount)
        byArea = []
        for index in byAreaCount.index.tolist():
            obj = {'province':index,'count':str(byAreaCount[index]),'amount':round(byAreaAmount[index],2)}
            byArea.append(obj)
        jsonData['area'] = byArea

        bySourceCount = csv_data['purchaseSource'].value_counts()
        bySourceCount = bySourceCount.sort_values(ascending=False)
        byCount_s = []
        for index in bySourceCount.index.tolist():
            obj = {'name':index,'value':str(bySourceCount[index])}
            byCount_s.append(obj)
        byAmount_s = []
        bySourceAmount = csv_data.groupby(by=['purchaseSource'])['projectAmount'].sum()
        bySourceAmount = bySourceAmount.sort_values(ascending=False)
        for index in bySourceCount.index.tolist():
            obj = {'name': index, 'value': round(bySourceAmount[index],2)}
            byAmount_s.append(obj)
        jsonData['source'] = {'byCount':byCount_s,'byAmount':byAmount_s}
        pper = csv_data['purchaseDate'].dt.to_period("Q")
        #bytimeQ = csv_data['purchaseDateQuarter'].value_counts()
        bytimeQ = pper.value_counts()
        bytimeQ = bytimeQ.sort_index(ascending=False)
        amountQ = csv_data.groupby(pper)['projectAmount'].sum()
        amountQ = amountQ.sort_index(ascending=False)
        amountlistQ = []
        for number in amountQ.values.tolist():
            amountlistQ.append(round(number, 2))
        jsonData['quarterData'] = {'date': bytimeQ.index.tolist(), 'count': bytimeQ.values.tolist(),'amount': amountlistQ}
        #text = ''.join(c for c in csv_data['title']) 
        #jsonData['wordcloudURL'] = gen_wc(text)
    return  myview(json.dumps(jsonData,cls=ComplexEncoder))

def gen_word_cloud(request):
    global db_data
    jsonData = {}
    csv_path = request.GET.get('csv_path')
    paramSearchkey = request.GET.get('paramSearchkey')
    businessTypeArray = request.GET.get('businessTypeArray')
    paramSourceArray = request.GET.get('paramSourceArray')
    guildId = request.GET.get('guildId')
    jobTagArray = request.GET.get('jobTagArray')
    startTime = request.GET.get('startTime')
    endTime = request.GET.get('endTime')
    paramProvincesArray = request.GET.get('paramProvincesArray')

    timeMon = None
    if startTime:
       timeMon = startTime[0:7]
    params = "%s_%s_%s_%s_%s_%s" % (businessTypeArray , paramSourceArray , guildId , jobTagArray , timeMon , paramProvincesArray)
    hash_md5 = hashlib.md5(params.encode("utf8"))
    fname = hash_md5.hexdigest() + ".png"
    if file_exist(fname):
        url = get_static_url(fname)
        jsonData = {'url':url}
        return myview(json.dumps(jsonData,cls=ComplexEncoder))

    goDeepType = request.GET.get('goDeepType')
    goDeepData = request.GET.get('goDeepData')
    goDeepLevel = request.GET.get('goDeepLevel')

    csv_data = db_data
    print(type(csv_data['purchaseDate']))
    if guildId:
        csv_data = csv_data[csv_data['guildId']==int(guildId)]
    if paramSourceArray:
        ar = json.loads(paramSourceArray)
        csv_data = csv_data[csv_data['paramPurchaseSource'].isin(ar)]
    if paramSearchkey:
        csv_data = csv_data[csv_data['title'].str.contains(paramSearchkey)]
    if goDeepType and goDeepData:
        if goDeepType == 'businessType':
            if goDeepLevel == '1':
                csv_data = csv_data[csv_data['businessType'] == goDeepData]
        elif goDeepType == 'zbf':
            csv_data = csv_data[csv_data['purchaseSource'] == goDeepData]
        elif goDeepType == 'area':
            if goDeepLevel == '1':
                csv_data = csv_data[csv_data['provinceName'] == goDeepData]
            pass
        elif goDeepType == 'time':
            pass
        elif goDeepType == 'jobTag':
            pass

    if startTime and startTime.startswith('201'):
        csv_data = csv_data[csv_data['purchaseDate'] >= pd.to_datetime(startTime)]

    if endTime and endTime.startswith('201'):
        csv_data = csv_data[csv_data['purchaseDate'] < pd.to_datetime(endTime)]
    
    if paramProvincesArray:
       ar = json.loads(paramProvincesArray)
       csv_data = csv_data[csv_data['province'].isin(ar)]

    if businessTypeArray and businessTypeArray != '':
        jsonObj = json.loads(businessTypeArray)
        btype = []
        for obj in jsonObj:
            #print(obj['minorBusinessType'])
            btype.append(obj['minorBusinessType'])
        csv_data = csv_data[csv_data['minorBusinessType'].isin(btype)]

    text = ' '.join(c for c in csv_data['title'])
    url = gen_wc(text,fname)
    jsonData = {'url':url}
    return myview(json.dumps(jsonData,cls=ComplexEncoder))
