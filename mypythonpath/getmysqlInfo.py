import json

with open(r'D:\PythonCode\mypythonpath\mysqlInfo.json','r',encoding='utf-8') as ff:
	jsonT = json.load(ff)
	ff.close()

jsonInfo = jsonT
