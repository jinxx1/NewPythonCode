import pymongo,pymysql,datetime,time,pprint,random
from bson.objectid import ObjectId


MONGO_INFO = {'MongoClient':'mongodb://localhost:27017/',
    'MongoDBname':'ztb'}

class Couch_obj(object):
    pass

    def __init__(self):
        pass


class MongoDB_obj(object):
    myclinent = pymongo.MongoClient(MONGO_INFO['MongoClient'])
    db = myclinent[MONGO_INFO['MongoDBname']]
    def findMongo(self,collname,ddict):
        if 'issueTime' in ddict.keys():
            issTime = ddict['issueTime']
            del ddict['issueTime']
            try:
                Datime = datetime.datetime.strptime(issTime,"%Y-%m-%d")
                ddict['issueTime'] = Datime
            except:
                return 'issueTime ERROR'
        if 'count' not in ddict.keys():
            ddict['count'] = 1000000

        count = ddict['count']
        del ddict['count']
        mycol = self.db[collname]
        finddate = mycol.find(ddict).limit(count)
        getinfo = [x for x in finddate]
        return getinfo

    def breakpoint(self,collname,urllist):
        mycol = self.db[collname]
        returnlist = []
        for getdict in urllist:

            findict = {'channelCode':getdict['channelCode']}
            findinfo = mycol.find(findict)

            maxday = findinfo.sort('zaoday',1)

            findNum = maxday.sort('Num',-1).limit(1)
            # print(findNum)
            llst = [x for x in findNum]
            # print(llst)
            if llst:

                for i in llst:
                    # print(i)
                    getdict['Num'] = i['Num']
                    # print(i)

                    wanday = datetime.datetime.fromtimestamp(i['wanday'])
                    getdict['wanday'] = wanday.strftime('%Y-%m-%d')
                    # print('wanday',getdict['wanday'])

                    zaoday = datetime.datetime.fromtimestamp(i['zaoday'])
                    getdict['zaoday'] = zaoday.strftime('%Y-%m-%d')

                    # print('zaoday',getdict['zaoday'])
                    returnlist.append(getdict)
                    break

            else:
                getdict['Num'] = 1
                wanday = datetime.date.today()
                zaoday = wanday - datetime.timedelta(days=30)
                getdict['wanday'] = str(wanday.strftime('%Y-%m-%d'))
                getdict['zaoday'] = str(zaoday.strftime('%Y-%m-%d'))
                returnlist.append(getdict)
        # pprint.pprint(returnlist)
        return returnlist

    def url_deWeighting(self,collname,urllist):
        mycol = self.db[collname]
        noGotUrl = []
        for url in urllist:
            findict = {'ArticleUrl': url['articllink']}
            aa = mycol.find_one(findict,{'ArticleUrl': 1})
            if not aa:
                noGotUrl.append(url)
        return noGotUrl

def urllistP():
    chengshiList =[{'catName2': '省直_', 'sitewebId': '4028889705bebb510105bec068b00003'}, {'catName2': '佛山市_', 'sitewebId': '4028889705bebb510105bec1f8670004'}, {'catName2': '梅州市_', 'sitewebId': '4028889705bedd7e0105beec36890004'}, {'catName2': '河源市_', 'sitewebId': '4028889705bedd7e0105beed4b240005'}, {'catName2': '阳江市_', 'sitewebId': '4028889705bedd7e0105bef239d20006'}, {'catName2': '清远市_', 'sitewebId': '4028889705bedd7e0105bef333260007'}, {'catName2': '东莞市_', 'sitewebId': '4028889705bedd7e0105bef45f220008'}, {'catName2': '中山市_', 'sitewebId': '4028889705bedd7e0105bef51d7f0009'}, {'catName2': '揭阳市_', 'sitewebId': '4028889705bedd7e0105bef673b8000b'}, {'catName2': '云浮市_', 'sitewebId': '4028889705bedd7e0105bef70a69000c'}, {'catName2': '汕头市_', 'sitewebId': '4028889705bebb510105becdbed40009'}, {'catName2': '江门市_', 'sitewebId': '4028889705bebb510105becf79c2000a'}, {'catName2': '湛江市_', 'sitewebId': '4028889705bebb510105bed04b88000b'}, {'catName2': '茂名市_', 'sitewebId': '4028889705bebb510105bed1471d000c'}, {'catName2': '广州市_', 'sitewebId': '4028889705bebb510105bec9f3490006'}, {'catName2': '肇庆市_', 'sitewebId': '4028889705bebb510105bed24c86000d'}, {'catName2': '潮州市_', 'sitewebId': '4028889705bedd7e0105bef5da47000a'}, {'catName2': '深圳市_', 'sitewebId': '4028889705bebb510105becb72d30007'}, {'catName2': '汕尾市_', 'sitewebId': '4028889705bebb510105bed6e6ac000f'}, {'catName2': '惠州市_', 'sitewebId': '4028889705bebb510105bed2e21f000e'}, {'catName2': '韶关市_', 'sitewebId': '4028889705bebb510105becc5dbf0008'}, {'catName2': '珠海市_', 'sitewebId': '4028889705bebb510105bec522060005'}]
    infoList = [{'catName1': '广东省_', 'catName2': '中标公告', 'channelCode': '0008', 'requestUrl': 'http://www.gdgpo.gov.cn/queryMoreInfoList.do'}, {'catName1': '广东省_', 'catName2': '审核前公示', 'channelCode': '-4', 'requestUrl': 'http://www.gdgpo.gov.cn/queryMoreInfoList.do'}, {'catName1': '广东省_', 'catName2': '资格预审公告', 'channelCode': '-6', 'requestUrl': 'http://www.gdgpo.gov.cn/queryMoreInfoList.do'}, {'catName1': '广东省_', 'catName2': '采购公告', 'channelCode': '0005', 'requestUrl': 'http://www.gdgpo.gov.cn/queryMoreInfoList.do'}, {'catName1': '广东省_', 'catName2': '更正公告', 'channelCode': '0006', 'requestUrl': 'http://www.gdgpo.gov.cn/queryMoreInfoList.do'}, {'catName1': '广东省_', 'catName2': '电子反拍公告', 'channelCode': '0017', 'requestUrl': 'http://www.gdgpo.gov.cn/queryMoreInfoList.do'}, {'catName1': '广东省_', 'catName2': '批量集中采购', 'channelCode': '-3', 'requestUrl': 'http://www.gdgpo.gov.cn/queryMoreInfoList.do'}]

    urllist1 = []
    # for chengshi in chengshiList:
    for info in infoList:
        dicll ={}
        dicll['catName'] = info['catName1'] + info['catName2']
        dicll['channelCode'] = info['channelCode']
        dicll['requestUrl'] = info['requestUrl']
        urllist1.append(dicll)
    return urllist1


if __name__ == "__main__":
    mongoinfo = MongoDB_obj()
    ddict = {
        'site':'中国移动采购中心',
        # 'url':'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=590274',
        'issueTime':'2019-08-25',
        'count':2
    }



    a = mongoinfo.findMongo(collname='cm_getUrl',ddict=ddict)
        # mongoinfo.findMongo(collname='cm_getUrl',dict=ddict)
    pprint.pprint(a)









