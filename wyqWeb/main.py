from flask import render_template
from scrpt import outPD
from flask import Flask
from flask import request
import datetime,os
import json
from ast import literal_eval
import pprint
app = Flask(__name__)
app.jinja_env.variable_start_string = "{{ "
app.jinja_env.variable_end_string = " }}"

root = os.getcwd()

jsonPath = os.path.join(root,'info.json')
filePath = os.path.join(root,'111111.xlsx')

def jsonload(jsonPath):
    try:
        with open(jsonPath, 'r') as jf:
            jsonLoad = json.load(jf)
            jf.close()
    except:
        with open(jsonPath, 'w') as jf:
            jsonLoad = {}
            jsonLoad['info'] = []
            json.dump(jsonLoad, jf)
            jf.flush()
            jf.close()
    return jsonLoad

def jsonwrite(jsonPath,item):
    with open(jsonPath, 'w') as jf:
        json.dump(item,jf)
        jf.flush()
        jf.close()


Info = jsonload(jsonPath)


def getInfo():
    sheet = outPD(xlsxfilepath=filePath)

    return sheet



@app.route('/',methods=['POST','GET'])
def index():
    if request.method == "POST":
        nowInfo = []


        listInfo = request.values.getlist("checkbox_option")

        for i in listInfo:
            ddict = {}
            ddict['artInfo'] = i
            ddict['preson_name'] = request.values.get("proson_name")
            ddict['preson_tel'] = request.values.get("proson_tel")
            ddict['times'] = str(datetime.datetime.now())
            nowInfo.append(ddict)

        return render_template("indexGet.html", info=nowInfo,okinfo=nowInfo)
    else:
        return render_template("index.html",info = outPD(xlsxfilepath=filePath))

@app.route('/todb',methods=['POST'])
def todb():
    listInfo = request.values.get("subok")
    mlist = literal_eval(listInfo)
    Info['info'].extend(mlist)
    jsonwrite(jsonPath,Info)
    return '已经提交'

@app.route('/myloveisjinxiao',methods=['POST','GET'])
def myLoveisjinxiao():
    getInfo = jsonload(jsonPath)
    print(getInfo)
    return render_template("mylove.html", info=getInfo['info'])

@app.route('/movieList')
def movie_list():
    return '''
            <!DOCTYPE html>
        <html>
        <body>
        <video   controls="controls">
          <source src="static/movies/Massage.mp4" type="video/mp4" />
        </video>
        </body>
        </html>
    '''
@app.route('/killuxue',methods=['POST','GET'])
def kill():
    return "1"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5001',debug=True)
