import pprint


def processNum(i, n, pp, count):
	if pp == '+':
		a = i + n
	elif pp == '-':
		a = i - n
	elif pp == '*':
		a = i * n
	else:
		try:
			a = i / n
		except ZeroDivisionError:
			a = 0

	return a


def llist_1(inputNum):
	global INPUTNUM
	llist_1 = []
	for i in range(len(inputNum)):
		for n in range(len(inputNum)):
			if i == n:
				continue
			else:
				for pp in ['+', '-', '*', '!!']:
					ddict = {}
					ddict['local'] = [i, n]
					if pp == '+' or pp == '-':
						ddict['shizi'] = "(" + str(inputNum[i]) + pp + str(inputNum[n]) + ")"
					else:
						ddict['shizi'] = str(inputNum[i]) + pp + str(inputNum[n])
					ddict['jg'] = processNum(i=inputNum[i], n=inputNum[n], pp=pp, count=1)
					llist_1.append(ddict)
	return llist_1


def llist_2(inputNum):
	global INPUTNUM
	llist = []
	for dict_i in inputNum:
		for n in range(len(INPUTNUM)):
			if n in dict_i['local']:
				continue
			else:
				for pp in ['+', '-', '*', '!!']:
					ddict = {}
					ddict['local'] = [dict_i['local'][0], dict_i['local'][1], n]
					if '(' in dict_i['shizi']:
						ddict['shizi'] = "[" + dict_i['shizi'] + pp + str(INPUTNUM[n]) + "]"
					else:
						ddict['shizi'] = "[" + dict_i['shizi'] + pp + str(INPUTNUM[n]) + "]"
					ddict['jg'] = processNum(i=dict_i['jg'], n=INPUTNUM[n], pp=pp, count=2)

					llist.append(ddict)

				for pp in ['+', '-', '*', '!!']:
					ddict = {}
					ddict['local'] = [dict_i['local'][0], dict_i['local'][1], n]
					if '(' in dict_i['shizi']:
						ddict['shizi'] = "[" + str(INPUTNUM[n]) + pp + dict_i['shizi'] + "]"
					else:
						ddict['shizi'] = "[" + str(INPUTNUM[n]) + pp + dict_i['shizi'] + "]"
					ddict['jg'] = processNum(n=dict_i['jg'], i=INPUTNUM[n], pp=pp, count=2)

					llist.append(ddict)
	return llist


def llist_3(inputNum):
	global INPUTNUM
	llist = []
	for dict_i in inputNum:
		for n in range(len(INPUTNUM)):
			if n in dict_i['local']:
				continue
			else:
				for pp in ['+', '-', '*', '!!']:
					ddict = {}
					ddict['local'] = [dict_i['local'][0], dict_i['local'][1], dict_i['local'][2], n]
					ddict['shizi'] = dict_i['shizi'] + pp + str(INPUTNUM[n])
					ddict['jg'] = processNum(i=dict_i['jg'], n=INPUTNUM[n], pp=pp, count=3)
					llist.append(ddict)
				for pp in ['+', '-', '*', '!!']:
					ddict = {}
					ddict['local'] = [dict_i['local'][0], dict_i['local'][1], dict_i['local'][2], n]
					ddict['shizi'] = str(INPUTNUM[n]) + pp + dict_i['shizi']
					ddict['jg'] = processNum(n=dict_i['jg'], i=INPUTNUM[n], pp=pp, count=3)

					llist.append(ddict)
	return llist


def shizi_both(list1):
	llist = []
	for i in list1:
		for n in list1:
			ret = list(set(i['local']).intersection(n['local']))
			if len(ret) > 0:
				continue
			else:
				for pp in ['+', '-', '*', '!!']:
					ddict = {}
					ddict['shizi'] = "(" + i['shizi'] + ")" + pp + "(" + n['shizi'] + ")"
					ddict['jg'] = processNum(i=i['jg'], n=n['jg'], pp=pp, count=4)
					llist.append(ddict)
				for pp in ['+', '-', '*', '!!']:
					ddict = {}
					ddict['shizi'] = "(" + n['shizi'] + ")" + pp + "(" + i['shizi'] + ")"
					ddict['jg'] = processNum(n=i['jg'], i=n['jg'], pp=pp, count=4)
					llist.append(ddict)
	return llist


def getINPUNUM(strNum):
	Num2str = list(str(strNum))
	INPUTNUM = []
	for x in Num2str:
		if x == '0':
			a = 10
		else:
			a = int(x)
		INPUTNUM.append(a)
	return INPUTNUM


def main(INPUTNUM,result):

	list1 = llist_1(INPUTNUM)
	list2 = llist_2(list1)
	list3 = llist_3(list2)
	llist_rsult = []
	maxValue = []
	for i in list3:
		maxValue.append(i['jg'])
		if i['jg'] == result or round(i['jg'], 4) == result:
			aa = '{} = {}'.format(i['shizi'], i['jg'])
			aa = aa.replace("!!", '/').replace("((", '(').replace("))", ')')
			llist_rsult.append(aa)
	for i in shizi_both(list1):
		maxValue.append(i['jg'])
		if i['jg'] == result or round(i['jg'], 4) == result:
			aa = '{} = {}'.format(i['shizi'], i['jg'])
			aa = aa.replace("!!", '/').replace("((", '(').replace("))", ')')
			llist_rsult.append(aa)
	llistDUP = list(set(llist_rsult))
	ll = []
	for i in llistDUP:
		aa = i.replace('*', ' x ').replace('-', ' — ').replace('+', ' + ').replace("/", ' / ')
		ll.append(aa)
	# print(max(maxValue),min(maxValue))
	pprint.pprint(ll)
	return ll


if __name__ == '__main__':
	strN = 2067
	result = 50
	a = getINPUNUM(strN)

	INPUTNUM = [17,25,4,9]
	# INPUTNUM = a
	main(INPUTNUM,result=result)
	exit()
	for i in range(1,101):
		a = main(INPUTNUM,result=i)
		if a:
			pprint.pprint(i)
			print('------------'*5)

	exit()
	mark = 0
	for i in range(1000, 9999 + 1):
		INPUTNUM = getINPUNUM(i)
		getresult = main(INPUTNUM)
		if getresult:
			mark += 1
	print(mark / 10000)
