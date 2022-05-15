# -*- coding: utf-8 -*-
import pprint, cpca
import pandas as pd

if __name__ == '__main__':

	wrod = ['天津蓟州区']
	aa = cpca.transform(wrod)
	print(aa)
	exit()


	txtPath = r"D:\PythonCode\wyq_about\20211008_wifi.txt"

	with open(txtPath, 'r', encoding='utf-8') as ff:
		txtInfo = ff.read()
	txtList = txtInfo.split('\n')
	llist = []
	for num, i in enumerate(txtList):
		if i:
			g = i.split(',')
			ddict = {}
			ddict['id'] = g[0]
			ddict['name'] = g[1]
			ddict['tel'] = g[2]
			ddict['address'] = g[3]
			ddict['count'] = g[4]
			ddict['time'] = g[5]
			aa = cpca.transform([g[3]])
			ddict['provice'] = aa.iloc[0]['省']
			ddict['city'] = aa.iloc[0]['市']
			ddict['district'] = aa.iloc[0]['区']
			print((aa))
			llist.append(ddict)
			print('-----------------------------')
	df = pd.DataFrame(llist)
	df.to_excel('dd.xlsx', index=False, encoding='utf_8_sig')
