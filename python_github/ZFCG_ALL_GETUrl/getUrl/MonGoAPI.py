from flask import Flask, request
import pprint,datetime,json
from flask_pymongo import PyMongo
from flask_restful import Api,Resource
app = Flask(__name__)

app.config['MONGO_URI']='mongodb://localhost:27017/ztb'

api = Api(app)
mongo = PyMongo(app)


def time2Str(dictInfo):
    try:
        capturedTime = dictInfo['capturedTime']
        del dictInfo['capturedTime']
        dictInfo['capturedTime'] = capturedTime.strftime('%Y-%m-%d %H:%M:%S')
    except:
        pass
    try:
        issueTime = dictInfo['issueTime']
        del dictInfo['issueTime']
        dictInfo['issueTime'] = issueTime.strftime('%Y-%m-%d %H:%M:%S')
    except:
        pass
    return dictInfo

class apiGetInfo(Resource):

    def get(self):
        getinfo = mongo.db.monitorUrl.find().limit(50)
        getinfo_list = []
        for i in getinfo:
            dictInfo = time2Str(i)
            getinfo_list.append(dictInfo)
        return dict(result='success', info_list=getinfo_list)

    def post(self):
        getDateStr = request.get_data()
        ddict = json.loads(getDateStr)
        if 'issueTime' in ddict.keys():
            issTime = ddict['issueTime']
            del ddict['issueTime']
            try:
                DatimeSTART = datetime.datetime.strptime(issTime + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
                DatimeEND = datetime.datetime.strptime(issTime + ' 23:59:59', "%Y-%m-%d %H:%M:%S")
                # Datime = datetime.datetime.strptime(issTime,"%Y-%m-%d %H:%M:%S")
                ddict['issueTime'] = {"$gte":DatimeSTART,"$lte":DatimeEND}
            except:
                return dict(result='error', message='issueTime ERROR')
        if 'count' not in ddict.keys():
            ddict['count'] = 1000000

        count = ddict['count']
        del ddict['count']


        finddate = mongo.db.monitorUrl.find(ddict).limit(count)
        getinfo = []
        if finddate is not None:
            for ii in finddate:
                qq = time2Str(ii)
                getinfo.append(qq)
            return dict(result='success', message=getinfo,count=len(getinfo))
        else:
            return dict(result='error', message='not MongoInfo')

class indexGet(Resource):
    def get(self):
        getinfo = mongo.db.monitorUrl.find().limit(50)
        getinfo_list = []
        for i in getinfo:
            dictInfo = time2Str(i)
            getinfo_list.append(dictInfo)
        return dict(result='success', info_list=getinfo_list)

api.add_resource(apiGetInfo, '/apiGetMongoInfo')
api.add_resource(indexGet, '/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111,debug=True)