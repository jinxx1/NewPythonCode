# -*- coding: utf-8 -*-
import cpca
import csv, os
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


def getProvince(xList):
	llist = []
	for i in xList:
		aa = cpca.transform([i])
		a = aa.iloc[0]['省']
		a = a.replace('省', '')
		llist.append(a)
	return llist


def getInterrval(arrlike, mode='省'):
	word = ''
	aa = cpca.transform([arrlike['address']])
	if aa.iloc[0][mode]:
		word = aa.iloc[0][mode]
	return word

def getInterrval_1(arrlike, mode='省'):
	word = ''
	aa = cpca.transform([arrlike['address']])

	arrlike['province'] = aa.iloc[0]['省']
	arrlike['city'] = aa.iloc[0]['市']
	arrlike['distrct'] = aa.iloc[0]['区']

	return arrlike


if __name__ == '__main__':
	a = r"all.csv"
	a = r"202101-202111.csv"
	b = r"D:\SoftWare_ChatLog\WeChat Files\WeChat Files\wxid_z7czcokj3ya612\FileStorage\File\2021-12"
	b = r"C:\Users\jinxx1\Desktop"
	root = os.path.join(b, a)

	df = pd.read_csv(root, header=None, names=['id', 'name', 'name_sort', 'address', 'count', 'issuetime'])
	df1 = df.apply(getInterrval_1, axis=1)
	print(df1)
	# df['city'] = df.apply(getInterrval, axis=1, mode='市')
	# df['distrct'] = df.apply(getInterrval, axis=1, mode='区')

	df1.to_excel('202101.xlsx', index=False, encoding='utf_8_sig')
