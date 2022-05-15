
import platform, sys, os, json

mysystem = platform.system()
if mysystem == 'Windows':
    root = r"D:/PythonCode/mypythonpath/jsCode/"

elif mysystem == "Linux":
    root = "/home/terry/anaconda3/lib/python3.7/site-packages/mtools/jsCode/"

else:
    raise 'not Windows or Linux'




def get_jsCode(jsName):
    jsFile = jsName+'.js'
    filePath = os.path.join(root,jsFile)
    with open(filePath,'r',encoding='utf-8') as f:
        js_code = f.read()
    return js_code

