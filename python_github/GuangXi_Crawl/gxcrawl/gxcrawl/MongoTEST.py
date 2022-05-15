import pymongo,pymysql,datetime,time,pprint
from bson.objectid import ObjectId



class MongoDB_guangxi_ContentUrl(object):

    myclinent = pymongo.MongoClient('mongodb://localhost:27017/')
    db = myclinent['ztb']
    mycol = db['guangxi_ContentUrl']

    def getMongoALLdate(self,dict=None):
        return self.mycol.find(dict)




if __name__=="__main__":

    MongoDB_guangxi_ContentUrl = MongoDB_guangxi_ContentUrl()
    # a = getMongoALLdate()
    # b = {'code': 'wlRj','inserTOMAINSQL': 0}
    b = {'code': 'wlRj','inserTOMAINSQL': 0}
    # b = {'mysql_id': 24761}
    # b = {'_id': ObjectId('5d3555bfbfcef848e290c3ff')}
    # b = {'ContentUrl': 'http://www.ccgp-guangxi.gov.cn/view/staticpags/shengji_zbgg/8ab8814e43302600014332f311261e1e.html'}


    fromkey_all = MongoDB_guangxi_ContentUrl.getMongoALLdate(b)

    for i in fromkey_all:
        print(i)
    print(fromkey_all.count())
    print(type(fromkey_all))




