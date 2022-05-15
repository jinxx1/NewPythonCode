import pprint
import random
import time, datetime
import asyncio
import numpy as np

from guess_numGame import checkNum, creat_NUMBERS

loop = asyncio.get_event_loop()


def allNum(digit):
	str_digi = "%0{}d".format(digit)
	allNumList_str = [str_digi % x for x in range(0, 10 ** digit)]

	finalList = []
	for i in allNumList_str:
		finalNum_nodup = [int(x) for x in list(i)]
		if len(list(set(finalNum_nodup))) == digit:
			finalList.append(finalNum_nodup)
	return finalList


def processNum(inputNum, iterNum, A, B, num, digit):
	'''
	input是输入的数字。是 一维list
	A是位置对，  数对   的个数
	B是位置不对，数对   的个数
	interNum是上一次可迭代后的所有三位数集合，若第一次迭代，则为全部720个数字。是二维list
	'''
	# if num == 0:
	# 	iterNum = allNum(digit=digit)

	# 将输入的inputNum【一维list】跟迭代集合中每个元素list做交集比对。若交集 个数 等于A+B，则将其装入 list1中。
	list1 = []
	for n in iterNum:
		ret = list(set(n).intersection(inputNum))
		if len(ret) == A + B:
			list1.append(n)

	# 获得list1后，再比对每个位置的数字是否相等。若位置对，数对，则mark+1。最终mark跟A相等的，则装入list2中。
	list2 = []
	for n in list1:
		mark = 0
		for i in range(0, digit):
			if inputNum[i] == n[i]:
				mark += 1
		if mark == A:
			list2.append(n)
	# 最终返回list2
	return list2


def main(digit, allNumDict):
	NUMBER = creat_NUMBERS(digit)
	for num in range(0, 8000000):
		if num == 0:
			input_num = random.sample(range(0, 9), digit)
			ln = checkNum(NumBer=NUMBER['number'], inputNum=input_num, digit=digit)
			iterNum = processNum(inputNum=input_num, iterNum=allNumDict, A=ln['A'], B=ln['B'], num=num, digit=digit)
		else:
			input_num = random.choice(iterNum)
			ln = checkNum(NumBer=NUMBER['number'], inputNum=input_num, digit=digit)
			iterNum = processNum(inputNum=input_num, iterNum=iterNum, A=ln['A'], B=ln['B'], num=num, digit=digit)
		print('第{}次，猜的数字为：{}，结果为{}。穷举库中还剩下{}组数字'.format(num + 1, input_num, ln, len(iterNum)))
		# print("正确答案是:",NUMBER['number'])
		# print("筛选后还剩下的数组为：",iterNum)
		# print("剩下的数组个数为：", len(iterNum))
		# print('**' * 60, num+1)

		if len(iterNum) == 1:
			if iterNum[0] == NUMBER['number']:
				print('恭喜猜出来了')
				print('最终得出的数字为：', iterNum[0])
				print('一共猜了{}次'.format(num + 1))
				print('**' * 60, num + 1)
			else:
				print('最终结果有问题')
				print('**' * 60, 'ERROR')
			break


def allNum_asyTest(digit):
	str_digi = "%0{}d".format(digit)
	allNumList_str = []
	for i in range(1, 10 ** digit + 1):
		allNumList_str.append(intnumber_2_strlist(i, digit))
	# loop.run_until_complete(asyncio.wait(allNumList_str))
	# return allNumList_str


# finalList = []
# for i in allNumList_str:
# 	finalNum_nodup = [int(x) for x in list(i)]
# 	if len(list(set(finalNum_nodup))) == digit:
# 		finalList.append(finalNum_nodup)
# return finalList


async def intnumber_2_strlist(intnumber, digit):
	str_digi = "%0{}d".format(digit)
	intList = str_digi % intnumber
	# await asyncio.sleep(0.001)
	return intList


if __name__ == '__main__':
	digit = 6
	starttime = datetime.datetime.now()
	# str_digi = "%0{}d".format(digit)
	# allNumList_str = [str_digi % x for x in range(0, 10 ** digit)]
	# allNum(digit=digit)
	endtime = datetime.datetime.now()
	a = (endtime - starttime).seconds
	print(endtime - starttime)
	print(a)
	'''-----------------------------------------'''
	starttime = datetime.datetime.now()
	# allNum_asyTest(digit)
	endtime = datetime.datetime.now()
	a = (endtime - starttime).seconds
	print(endtime - starttime)
	print(a)
	# exit()

ddict = {}
for nn in range(1, 12):
	digit = random.choice([5])
	if str(digit) in ddict.keys():
		allNumList = ddict[str(digit)]
	else:
		ddict[str(digit)] = allNum(digit=digit)
		allNumList = ddict[str(digit)]

	main(digit=digit, allNumDict=allNumList)

print('电脑自己跟自己玩了\t{}次'.format(nn))

'''
本游戏是猜数字。
根据以下5个条件，推断出准确的密码是多少
条件1：682【一个号码正确，而且位置正确】
条件2：614【一个号码正确，但是位置不正确】
条件3：206【两个号码正确，但是位置都不正确】
条件4：738【没有一个号码正确】
条件5：870【一个号码正确，但是位置不正确】

正确答案：042
'''

# input是根据游戏条件做出来的二维数组。
# 每一个数组元素的前三位是所猜测的数字。后两位分别为A,B
# A是数正确，位置正确     的个数
# B是数正确，位置不正确   的个数
