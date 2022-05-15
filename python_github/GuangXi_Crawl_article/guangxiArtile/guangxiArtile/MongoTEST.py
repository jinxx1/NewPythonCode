import pymongo,pymysql,datetime,time,pprint
from bson.objectid import ObjectId

class MongoDB_guangxi_ContentUrl(object):
    myclinent = pymongo.MongoClient('mongodb://localhost:27017/')
    db = myclinent['ztb']
    mycol = db['guangxi_ContentUrl']

    def getMongoALLdate(self,dict=None):
        return self.mycol.find(dict)

    def updateDB(self,url):
        find_date = {'ContentUrl': url}
        newvalues = {"$set":{"inserTOMAINSQL":1}}
        return self.mycol.update(find_date,newvalues)

    def insert_error(self,url,dict):
        find_date = {'ContentUrl': url}
        newvalues = {"$set":dict}
        return self.mycol.update(find_date,newvalues)

    def TOMAINSQL1to0(self):
        inserTOMAINSQL_1 = {'inserTOMAINSQL': 1}
        inserTOMAINSQL_0 = {'inserTOMAINSQL': 0}
        newvalues = {"$set": inserTOMAINSQL_0}
        all_tomiansql_1 = self.mycol.find(inserTOMAINSQL_1)
        for i in all_tomiansql_1:
            self.mycol.update(inserTOMAINSQL_1, newvalues)




class MongoDB_guangxi_ArticleInfo(object):
    myclinent = pymongo.MongoClient('mongodb://localhost:27017/')
    db = myclinent['ztb']
    mycol = db['guangxi_insertoArticleInfo']

    def insertDB(self,dict):
        return self.mycol.insert_one(dict)

if __name__=="__main__":
    MongoDB_ContentUrl = MongoDB_guangxi_ContentUrl()
    print(MongoDB_ContentUrl.TOMAINSQL1to0())
    dictw = {'inserTOMAINSQL': 1}
    print([i for i in MongoDB_ContentUrl.getMongoALLdate(dictw)])


    