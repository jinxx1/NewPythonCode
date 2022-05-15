import re
from bs4 import BeautifulSoup
from pprint import pprint
import execjs
import requests
import base64
import jsbeautifier
HEA = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,zh-TW;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",


"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}

URL = "https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2"
brow = requests.get(url=URL,headers = HEA,verify=False)
META_CONTENT_rex = re.findall("<meta content=\"(.*?)\">",brow.text)[0]
js_org = re.findall("r=\"m\">(\(function.*?)</script>",brow.text)[0]

e309c5f_url = "https://b2b.10086.cn" + re.findall("charset=\"iso-8859-1\" src=\"(.*?)\" r=",brow.text)[0]
js_brow = requests.get(url=e309c5f_url,headers=HEA,verify=False)

js_windows = jsbeautifier.beautify(js_brow.text)


js_ori = jsbeautifier.beautify(js_org)


# pprint(brow.headers['Set-Cookie'])
e309c5f_rex = re.findall("ts\[\'e309c5f\'\]\=\'(.*?)\'",js_brow.text)[0]
# b64eval = ''.join([chr(ord(i) - idx % enc_int - 0x32) for idx, i in enumerate(e309c5f_rex)])
# b64eval
evalstr = base64.b64decode(e309c5f_rex.encode()).decode()
print(evalstr)



exit()
func_rex = re.findall("function.(_\$.*)\(",js_ori)
func_rex_reName = ['func_' + str(x) + n for x,n in enumerate(func_rex)]
for num,i in enumerate(func_rex_reName):
	js_ori = js_ori.replace(func_rex[num],i)
# print(js_ori)

GLOBAL_VAR_rex = re.findall("var.(_\$.*).=.0",js_ori)[0]
js_ori = js_ori.replace(GLOBAL_VAR_rex,'GLOBAL_VAR' + GLOBAL_VAR_rex)
# print(js_ori)


LIST_rex = re.findall("(_\$.*).=.\[",js_ori)[0]
js_ori = js_ori.replace(LIST_rex,'GLOBAL_LIST' + LIST_rex)
# print(js_ori)
# print(LIST_rex)

unKnowVar_rex = re.findall("function.*\((_\$.*)\)",js_ori)
unKnowVar_rex = sorted(set(unKnowVar_rex), key=unKnowVar_rex.index)
new_unKnowVar_rex = []
for i in unKnowVar_rex:
	n=i.split(',')
	if n:
		for nn in n:
			new_unKnowVar_rex.append(nn.strip())
	else:
		new_unKnowVar_rex.append(i)
unKnowVar_reName = ['args_' + str(x) + n for x,n in enumerate(new_unKnowVar_rex)]
for num,i in enumerate(unKnowVar_reName):
	js_ori = js_ori.replace(new_unKnowVar_rex[num], i)
# print(js_ori)


returnINT_rex = re.findall("(function.*\{\n.*\sreturn \d{1,2}.*\n)",js_ori)
for i in returnINT_rex:
	namerex = re.findall("(func_\d{1,2}_\$.*\(\))",i)[0]
	numrex = re.findall("return (\d{1,2})",i)[0]
	funcNewName = namerex.replace('func_','func_return{}_'.format(numrex))
	js_ori = js_ori.replace(namerex,funcNewName)


WINDOW_GLOBAL_VAR_rex = re.findall("return (_\$.*)\.Math\.abs",js_ori)[0]
js_ori = js_ori.replace(WINDOW_GLOBAL_VAR_rex,'WINDOW_GLOBAL_VAR')
print(js_ori)

# const_jsdom = '''const jsdom = require("jsdom");
# const { JSDOM } = jsdom;
# const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
# window = dom.window;
# document = window.document;
# XMLHttpRequest = window.XMLHttpRequest;
# '''

# all_js = const_jsdom + js_windows + js_ori
# print(all_js)
# add = execjs.compile(all_js)
# print(add.call(func_rex_reName[5]))
# # print(func_rex_reName)