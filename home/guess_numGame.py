import random
import datetime
import sys, os, json


def creat_NUMBERS(digit):
	Root = os.getcwd()
	numGameRoot = os.path.join(Root, 'numGame')
	NUMBER = random.sample(range(0, 9), digit)
	# time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	time = str(datetime.datetime.timestamp(datetime.datetime.now())*1000000).replace('.0','')
	id = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 8)) + "_" + time
	numGameFileName = id + ".json"
	numGameFilePathFull = os.path.join(numGameRoot, str(digit) + "_" + numGameFileName)
	# with open(numGameFilePathFull, 'w') as ff:
	# 	json.dump(NUMBER, ff)
	return {'id': id, 'jsonPath': numGameFilePathFull, 'number': NUMBER,'digit':digit,
	        'i1': None,
	        'i2': None,
	        'i3': None,
	        'i4': None,
	        'i5': None,
	        'i6': None,
	        'i7': None,
	        'crack': False
	        }


def checkNum(NumBer, inputNum, digit):
	# llist = inputNum
	ret = list(set(NumBer).intersection(inputNum))
	mark = 0
	for i in range(0, digit):
		if inputNum[i] == NumBer[i]:
			mark += 1
	# llist.append(mark)
	# llist.append(len(ret) - mark)
	# return llist
	return {'A': mark, 'B': len(ret) - mark}


if __name__ == '__main__':
	a = random.choice([[1,2,3],[4,5,6],[7,8,9]])
	print(a)

	exit()
	for i in range(0,100):
		digit = random.randint(3,4)
		print(creat_NUMBERS(digit))
	exit()

	NumBer = [3, 2, 0, 7]
	inputN = [3, 1, 2, 4]
	a = checkNum(NumBer=NumBer, inputNum=inputN, digit=digit)

	print(a)
