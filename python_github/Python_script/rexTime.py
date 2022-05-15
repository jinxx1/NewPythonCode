# -*- coding: utf-8 -*-
from datetime import datetime
import cpca
import re


def strTime_after(timeSTR):
	if not timeSTR:
		return ''
	if timeSTR == '201/8/21':
		return datetime(2011, 8, 21)
	if timeSTR == '201810' or timeSTR == '2018.10':
		return datetime(2018, 10, 1)
	if timeSTR == '218-1-10':
		return datetime(2018, 1, 10)

	if timeSTR == '2018-10-':
		return datetime(2018, 10, 1)
	if timeSTR == '2018-11-31':
		return datetime(2018, 11, 30)
	if timeSTR == '2018.06':
		return datetime(2018, 6, 1)
	if timeSTR == '2018.09':
		return datetime(2018, 9, 1)

	try:
		bb = re.findall(r"（(.*?)）", timeSTR.replace(')', '）').replace('(', '（'))[0]
		cc = ''.join(bb).replace('/', '-').replace('\\', '-').replace('_', '-').replace('.', '-')
		timeSTR = cc
	except:
		pass

	aa = ''
	try:
		regex = re.findall(r"\d{4}.*年\d{1,2}.*月.*?日.*?", timeSTR)[0]
		aa = regex.replace('年', '-').replace('月', '-').replace('日', '').replace(' ', '')
	except:
		try:
			regex = re.findall(r"\d{4}.*年\d{1,2}.*月.*?", timeSTR)[0]
			aa = regex.replace('年', '-').replace('月', '').replace(' ', '')
		except:
			aa = str(timeSTR).replace('/', '-').replace('\\', '-').replace('_', '-').replace('.', '-')

	timeStr = [x for x in aa.split('-') if x]

	if not timeStr:
		return ''

	if int(timeStr[0]) < 1990:
		return ''

	if len(timeStr) == 1:
		T1 = '1'
		T2 = '1'
	elif len(timeStr) == 2:
		if int(timeStr[1]) == 0:
			T1 = '1'
		else:
			T1 = timeStr[1]
		T2 = '1'

	else:
		if int(timeStr[2]) == 0:
			T2 = '1'
		elif int(timeStr[2]) > 31:
			T2 = int(timeStr[2]) // 10
		else:
			T2 = timeStr[2]
		T1 = timeStr[1]

	try:
		return datetime(int(timeStr[0]), int(T1), int(T2))
	except:
		try:
			return datetime(int(timeStr[0]), int(T1), int(T2) - 1)
		except:
			return ''


def strTime_other(timeSTR):
	if not timeSTR:
		return ''
	if timeSTR == '217.7.20':
		return datetime(int(2017), int(7), int(20))
	if timeSTR == '2018年' or timeSTR == '2018':
		return datetime(int(2018), int(1), int(1))
	if timeSTR == '2017年' or timeSTR == '2017':
		return datetime(int(2017), int(1), int(1))
	if timeSTR == '2016年' or timeSTR == '2016':
		return datetime(int(2016), int(1), int(1))
	if timeSTR == '2015年' or timeSTR == '2015':
		return datetime(int(2016), int(1), int(1))
	if timeSTR == '2014年' or timeSTR == '2014':
		return datetime(int(2016), int(1), int(1))
	if timeSTR == '2013年' or timeSTR == '2013':
		return datetime(int(2016), int(1), int(1))
	if timeSTR == '2012年' or timeSTR == '2012':
		return datetime(int(2016), int(1), int(1))
	if timeSTR == '2011年' or timeSTR == '2011':
		return datetime(int(2011), int(1), int(1))

	try:
		timeStr = re.findall(r"(\d{4}).*?(\d{2}).*?(\d{1,2})", str(timeSTR))[0]
	except:
		try:
			timeStr = re.findall(r"(\d{4}).*?(\d{1,2})", str(timeSTR))[0]
		except:
			return ''

	if len(timeStr) == 2:
		T2 = '1'

	elif len(timeStr) > 2 and int(timeStr[2]) > 31:

		T2 = int(timeStr[2]) // 10

	elif len(timeStr) > 2:
		T2 = timeStr[2]
	else:
		T2 = '1'

	if int(timeStr[0]) < 1990:
		return ''

	try:
		return datetime(int(timeStr[0]), int(timeStr[1]), int(T2))
	except:
		return ''


def strTime2dateTime(timeSTR):
	regexTimeStr = ''
	try:
		a = re.findall(r"\d{4}.*年\d{1,2}.*月\d{1,2}.*日", timeSTR)[0]
		regexTimeStr = a.replace('年', '-').replace('月', '-').replace('日', '').replace(' ', '')
	except:
		pass

	if regexTimeStr:
		timeStr = regexTimeStr
	elif '长期' in timeSTR:
		timeStr = '2999-12-31'
	elif find_zh(timeSTR) or len(timeSTR) < 6:
		return ''
	else:
		timeStr = str(timeSTR).replace('/', '-').replace('\\', '-').replace('_', '-').replace('.', '-')
		# print('timeStr -----',timeStr)

	timeL = [int(x) for x in timeStr.strip('-').split('-')]

	if len(timeL) > 2 and timeL[2] > 1000:
		dayint = timeL[0]
		timeL[0] = timeL[2]
		timeL[2] = dayint

	if 100 < timeL[0] < 1949:
		return ''
	elif 10 < timeL[0] < 20:
		timeL[0] = 2000 + timeL[0]
	elif 21 < timeL[0] < 100:
		timeL[0] = 1900 + timeL[0]
	try:
		Date_Time = datetime(timeL[0], timeL[1], timeL[2])
	except:

		Date_Time = ''

	return Date_Time


def find_zh(word):
	zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
	word = word
	match = zh_pattern.search(word)
	return match


def regFloat(word):
	try:
		a = filter(lambda ch: ch in '-0123456789.', str(word))
		straa = ''.join([x for x in a])
		nnmu = straa.count('.')
		stra = straa.replace('.', '', nnmu - 1)
	except:
		stra = ''
	return stra


def regFloat_negative(word):
	try:
		a = filter(lambda ch: ch in '-0123456789.', str(word))
		straa = ''.join([x for x in a])
		nnmu = straa.count('.')
		stra = straa.replace('.', '', nnmu - 1)
	except:
		stra = ''
	return stra


def findstrDifference(word):
	try:
		a = filter(lambda ch: ch in '0123456789.', str(word))
		stra = ''.join([x for x in a])
	except:
		stra = ''

	dic = dict()
	for n in stra:
		dic[n] = dic.get(n, 0) + 1
	for n in word:
		if n in dic:
			dic[n] = dic.get(n, 0) - 1
			if dic[n] == 0:
				del dic[n]
		else:
			return n


def regexName(inputword):
	if '贵州省邮电规划设计院' in inputword:
		return '贵州省邮电规划设计院'
	if '沈阳电信工程局' in inputword:
		return '沈阳电信工程局（有限公司）'
	if '吉林合瑞厂商' in inputword:
		return '吉林合瑞厂商'
	if '统联厂商' in inputword:
		return '统联厂商'
	if '中通国脉厂商' in inputword:
		return '中通国脉厂商'
	if '万兴.厂商' in inputword:
		return '万兴厂商'
	if '盛大厂商' in inputword:
		return '盛大厂商'

	kh = re.findall("（(.*?)）", inputword)
	if kh:
		if len(kh[0]) > 4:
			word = inputword.replace('（{}）'.format(kh[0]), '-').replace('--公示信息', '')
		else:
			word = inputword.replace('--公示信息', '')
	else:
		word = inputword.replace('--公示信息', '')

	re1 = re.findall(".+/(.*?)\.xl", word)[0]  # 匹配最后一个/
	re2 = re.findall(".+-(.*公司)", re1)
	if not re2:
		re3 = re.findall("、(.*公司)", re1)
		if not re3:
			re4 = re.findall("-(.*)-", re1)
			if not re4:
				trueWord = re1.replace('-公示信息', '').replace(' - 公示信息', '')
			else:
				trueWord = re4[0]
		else:
			trueWord = re3[0]
	else:
		trueWord = re2[0]

	return trueWord


def regIDandCode(inputword):
	temp = 'AAABBcccdddeeewww0123456789fffhhhjjjzzzBBCCC'
	word = inputword.replace('；', temp).replace('\n', temp).replace('\\', temp).replace('/', temp).replace('-',
	                                                                                                       temp).replace(
		';', temp).replace(':', temp)
	try:
		a = filter(lambda ch: ch in 'abcdefgh.ijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', str(word))

		stra = ''.join([x for x in a])
	except:

		stra = ''

	return stra.replace(temp, '\n')


def excelTime2unixTime(num):
	import time
	cc = (num - 19 - 70 * 365) * 86400 - 8 * 3600
	strTime = time.strftime("%Y-%m-%d", time.localtime(cc))
	return strTime


def get_location(strword):
	item = {}

	if not isinstance(strword, str):
		return ''
	# if len(strword) > 20:
	#     print(strword)
	if strword and '三台' in strword:
		item['Project_province'] = '四川省'
		item['Project_country'] = '绵阳市'
		item['Project_district'] = '三台县'

	elif strword and '济源' in strword:
		item['Project_province'] = '河南省'
		item['Project_country'] = '济源市'
		item['Project_district'] = ''

	elif strword and '鄂尔多斯' in strword:
		item['Project_province'] = '内蒙古自治区'
		item['Project_country'] = '鄂尔多斯市'
		item['Project_district'] = ''
	elif strword and '兴安' in strword:
		item['Project_province'] = '内蒙古自治区'
		item['Project_country'] = '兴安盟'
		item['Project_district'] = ''
	elif strword and '通辽' in strword:
		item['Project_province'] = '内蒙古自治区'
		item['Project_country'] = '通辽市'
		item['Project_district'] = ''
	elif strword and '赤峰' in strword:
		item['Project_province'] = '内蒙古自治区'
		item['Project_country'] = '赤峰市'
		item['Project_district'] = ''
	elif strword and '呼伦贝尔' in strword:
		item['Project_province'] = '内蒙古自治区'
		item['Project_country'] = '呼伦贝尔市'
		item['Project_district'] = ''
	elif strword and '扎噜特' in strword or '扎鲁特' in strword:
		item['Project_province'] = '内蒙古自治区'
		item['Project_country'] = '扎噜特部'
		item['Project_district'] = ''
	elif strword and '石河子' in strword:
		item['Project_province'] = '新疆维吾尔自治区'
		item['Project_country'] = '石河子县级市'
		item['Project_district'] = ''
	elif strword and '甘孜' in strword:
		item['Project_province'] = '四川省'
		item['Project_country'] = '甘孜藏族自治州'
		item['Project_district'] = ''
	elif strword and '南充' in strword:
		item['Project_province'] = '四川省'
		item['Project_country'] = '南充县级市'
		item['Project_district'] = ''
	elif strword and '凉山' in strword:
		item['Project_province'] = '四川省'
		item['Project_country'] = '凉山彝族自治州'
		item['Project_district'] = ''
	elif strword and '阿坝' in strword:
		item['Project_province'] = '四川省'
		item['Project_country'] = '阿坝藏族羌族自治州'
		item['Project_district'] = ''
	elif strword and '上海市浦东新区金桥镇' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '浦东新区'
		item['Project_district'] = '金桥镇'
	elif strword and '平潭' in strword:
		item['Project_province'] = '福建省'
		item['Project_country'] = '平潭县级市'
		item['Project_district'] = ''
	elif strword and '荔波' in strword:
		item['Project_province'] = '贵州省'
		item['Project_country'] = '布依族苗族自治州'
		item['Project_district'] = '荔波县'
	elif strword and '甘南' in strword:
		item['Project_province'] = '甘肃省'
		item['Project_country'] = '甘南藏族自治州'
		item['Project_district'] = ''
	elif strword and '崆峒' in strword:
		item['Project_province'] = '甘肃省'
		item['Project_country'] = '平凉市'
		item['Project_district'] = '崆峒山'
	elif strword and '武都' in strword:
		item['Project_province'] = '甘肃省'
		item['Project_country'] = '陇南市'
		item['Project_district'] = '武都区'
	elif strword and '博州' in strword:
		item['Project_province'] = '新疆维吾尔自治区'
		item['Project_country'] = '博尔塔拉蒙古自治州'
		item['Project_district'] = ''
	elif strword and '海西' in strword:
		item['Project_province'] = '青海省'
		item['Project_country'] = '海西蒙古族藏族自治州'
		item['Project_district'] = ''
	elif strword and '贵安' in strword:
		item['Project_province'] = '贵州省'
		item['Project_country'] = '贵安新区'
		item['Project_district'] = ''
	elif strword and '宝应' in strword:
		item['Project_province'] = '江苏省'
		item['Project_country'] = '扬州市'
		item['Project_district'] = '宝应区'
	elif strword and '南宁' in strword:
		item['Project_province'] = '广西壮族自治区'
		item['Project_country'] = '南宁市'
		item['Project_district'] = ''
	elif strword and '梅县' in strword:
		item['Project_province'] = '广东省'
		item['Project_country'] = '梅州市'
		item['Project_district'] = '梅县区'
	elif strword and '增城' in strword:
		item['Project_province'] = '广东省'
		item['Project_country'] = '广州市'
		item['Project_district'] = '增城区'
	elif strword and '深圳' in strword:
		item['Project_province'] = '广东省'
		item['Project_country'] = '深圳市'
		item['Project_district'] = ''
	elif strword and '红河' in strword:
		item['Project_province'] = '云南省'
		item['Project_country'] = '红河哈尼族彝族自治州'
		item['Project_district'] = ''
	elif strword and '中山' in strword:
		item['Project_province'] = '广东省'
		item['Project_country'] = '中山市'
		item['Project_district'] = ''
	elif strword and '象山' in strword:
		item['Project_province'] = '浙江省'
		item['Project_country'] = '宁波市'
		item['Project_district'] = '象山县'
	elif strword and '鄞州' in strword:
		item['Project_province'] = '浙江省'
		item['Project_country'] = '宁波市'
		item['Project_district'] = '鄞州县'
	elif strword and '山西晋中' in strword:
		item['Project_province'] = '山西省'
		item['Project_country'] = '晋中市'
		item['Project_district'] = ''
	elif strword and '西藏阿里' in strword:
		item['Project_province'] = '西藏自治区'
		item['Project_country'] = '阿里地区'
		item['Project_district'] = ''
	elif strword and '新疆省' in strword:
		item['Project_province'] = '新疆维吾尔自治区'
		item['Project_country'] = ''
		item['Project_district'] = ''

	elif strword and '内蒙' in strword:
		item['Project_province'] = '内蒙古自治区'
		item['Project_country'] = ''
		item['Project_district'] = ''

	elif strword and '云南昆明' in strword:
		item['Project_province'] = '云南省'
		item['Project_country'] = '昆明市'
		item['Project_district'] = ''

	elif strword and '新疆伊犁' in strword:
		item['Project_province'] = '新疆维吾尔自治区'
		item['Project_country'] = '伊犁市'
		item['Project_district'] = ''

	elif strword and '福建厦门' in strword:
		item['Project_province'] = '福建省'
		item['Project_country'] = '厦门市'
		item['Project_district'] = ''

	elif strword and '奉节' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '奉节县'

	elif strword and '闵行' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '上海市'
		item['Project_district'] = '闵行区'

	elif strword and '徐汇' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '上海市'
		item['Project_district'] = '徐汇区'

	elif strword and '杨浦' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '上海市'
		item['Project_district'] = '杨浦区'

	elif strword and '浦东' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '上海市'
		item['Project_district'] = '浦东区'

	elif strword and '宝山' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '上海市'
		item['Project_district'] = '宝山区'

	elif strword and '六库' in strword:
		item['Project_province'] = '云南省'
		item['Project_country'] = '怒江傈僳族自治州'
		item['Project_district'] = '六库镇'

	elif strword and '怒江' in strword:
		item['Project_province'] = '云南省'
		item['Project_country'] = '怒江傈僳族自治州'
		item['Project_district'] = ''

	elif strword and '铜仁' in strword:
		item['Project_province'] = '贵州省'
		item['Project_country'] = '铜仁市'
		item['Project_district'] = ''

	elif strword and '天门' in strword:
		item['Project_province'] = '湖北省'
		item['Project_country'] = '天门市'
		item['Project_district'] = ''

	elif strword and '那曲' in strword:
		item['Project_province'] = '西藏自治区'
		item['Project_country'] = '那曲市'
		item['Project_district'] = ''

	elif strword and '雄安' in strword:
		item['Project_province'] = '河北省'
		item['Project_country'] = '雄安新区'
		item['Project_district'] = ''

	elif strword and '荷泽' in strword:
		item['Project_province'] = '山东省'
		item['Project_country'] = '荷泽市'
		item['Project_district'] = ''

	elif strword and '海南州' in strword:
		item['Project_province'] = '青海省'
		item['Project_country'] = '海南藏族自治州'
		item['Project_district'] = ''

	elif strword and '海北州' in strword:
		item['Project_province'] = '青海省'
		item['Project_country'] = '海北藏族自治州'
		item['Project_district'] = ''

	elif strword and '大兴安岭' in strword:
		item['Project_province'] = '黑龙江省'
		item['Project_country'] = '大兴安岭地区'
		item['Project_district'] = ''

	elif strword and '伊犁' in strword:
		item['Project_province'] = '新疆维吾尔自治区'
		item['Project_country'] = '伊犁哈萨克自治州'
		item['Project_district'] = ''

	elif strword and '巴州' in strword:
		item['Project_province'] = '新疆维吾尔自治区'
		item['Project_country'] = '巴音郭楞蒙古自治州'
		item['Project_district'] = ''

	elif strword and '天府' in strword:
		item['Project_province'] = '四川省'
		item['Project_country'] = '天府新区'
		item['Project_district'] = ''

	elif strword and '锡林郭勒' in strword:
		item['Project_province'] = '内蒙古自治区'
		item['Project_country'] = '锡林郭勒盟'
		item['Project_district'] = ''

	elif strword and '阿拉善' in strword:
		item['Project_province'] = '内蒙古自治区'
		item['Project_country'] = '阿拉善盟'
		item['Project_district'] = ''

	elif strword and '桔山' in strword:
		item['Project_province'] = '贵州省'
		item['Project_country'] = '兴义市'
		item['Project_district'] = '桔山新区'

	elif strword and '万宁' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '万宁市'
		item['Project_district'] = ''

	elif strword and '乐东' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '乐东黎族自治县'
		item['Project_district'] = ''

	elif strword and '文昌' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '文昌市'
		item['Project_district'] = ''

	elif strword and '临高' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '临高直辖县'
		item['Project_district'] = '临高县'

	elif strword and '陵水' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '陵水黎族自治县'
		item['Project_district'] = ''

	elif strword and '黔南' in strword:
		item['Project_province'] = '贵州省'
		item['Project_country'] = '黔南布依族苗族自治州'
		item['Project_district'] = ''

	elif strword and '黔东南' in strword or '黔东' in strword:
		item['Project_province'] = '贵州省'
		item['Project_country'] = '黔东南苗族侗族自治州'
		item['Project_district'] = ''

	elif strword and '迪庆' in strword:
		item['Project_province'] = '云南省'
		item['Project_country'] = '迪庆藏族自治州'
		item['Project_district'] = ''

	elif strword and '奎山' in strword:
		item['Project_province'] = '江苏省'
		item['Project_country'] = '徐州市'
		item['Project_district'] = '泉山区奎山街道'

	elif strword and '稀土高新区' in strword:
		item['Project_province'] = '内蒙古自治区'
		item['Project_country'] = '包头市'
		item['Project_district'] = '稀土高新技术产业开发区'

	elif strword and '琼海' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '琼海市'
		item['Project_district'] = ''

	elif strword and '定安' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '定安直辖县'
		item['Project_district'] = ''

	elif strword and '保亭' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '保亭黎族苗族自治县'
		item['Project_district'] = ''

	elif strword and '五指山' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '五指山市'
		item['Project_district'] = ''

	elif strword and '恰卜恰' in strword:
		item['Project_province'] = '青海省'
		item['Project_country'] = '海南藏族自治州'
		item['Project_district'] = '恰卜恰镇'

	elif strword and '东方' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '东方'
		item['Project_district'] = ''

	elif strword and '天鹅县' in strword:
		item['Project_province'] = '广西壮族自治区'
		item['Project_country'] = '河池市'
		item['Project_district'] = '天鹅县'

	elif strword and '巴马' in strword:
		item['Project_province'] = '广西壮族自治区'
		item['Project_country'] = '河池市'
		item['Project_district'] = '巴马瑶族自治县'

	elif strword and '大化' in strword:
		item['Project_province'] = '广西壮族自治区'
		item['Project_country'] = '河池市'
		item['Project_district'] = '大化瑶族自治县'

	elif strword and '果洛' in strword:
		item['Project_province'] = '青海省'
		item['Project_country'] = '果洛藏族自治州'
		item['Project_district'] = ''

	elif strword and '海北' in strword:
		item['Project_province'] = '青海省'
		item['Project_country'] = '海北藏族自治州'
		item['Project_district'] = ''

	elif strword and '克州' in strword:
		item['Project_province'] = '新疆维吾尔自治区'
		item['Project_country'] = '克孜勒苏柯尔克孜自治州'
		item['Project_district'] = ''

	elif strword and '西双版纳' in strword:
		item['Project_province'] = '云南省'
		item['Project_country'] = '西双版纳傣族自治州'
		item['Project_district'] = ''

	elif strword and '琼中' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '琼中黎族苗族自治县'
		item['Project_district'] = ''

	elif strword and '昌江' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '昌江黎族自治县'
		item['Project_district'] = ''

	elif strword and '潜江' in strword:
		item['Project_province'] = '湖北省'
		item['Project_country'] = '潜江直管县'
		item['Project_district'] = ''

	elif strword and '仙桃' in strword:
		item['Project_province'] = '湖北省'
		item['Project_country'] = '仙桃市'
		item['Project_district'] = ''

	elif strword and '德宏' in strword:
		item['Project_province'] = '云南省'
		item['Project_country'] = '德宏傣族景颇族自治州'
		item['Project_district'] = ''

	elif strword and '东辽' in strword:
		item['Project_province'] = '吉林省'
		item['Project_country'] = '辽源市'
		item['Project_district'] = '东辽县'

	elif strword and '临安' in strword:
		item['Project_province'] = '浙江省'
		item['Project_country'] = '杭州市'
		item['Project_district'] = '临安区'

	elif strword and '通州' in strword:
		item['Project_province'] = '北京市'
		item['Project_country'] = '北京市'
		item['Project_district'] = '通州区'

	elif strword and '湘西' in strword:
		item['Project_province'] = '湖南省'
		item['Project_country'] = '湘西土家族苗族自治州'
		item['Project_district'] = ''

	elif strword and '澄迈' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '澄迈直辖县'
		item['Project_district'] = ''

	elif strword and '崇明' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '上海市'
		item['Project_district'] = '崇明区'

	elif strword and '密云' in strword:
		item['Project_province'] = '北京市'
		item['Project_country'] = '北京市'
		item['Project_district'] = '密云区'

	elif strword and '塘沽' in strword:
		item['Project_province'] = '天津市'
		item['Project_country'] = '天津市'
		item['Project_district'] = '塘沽区'

	elif strword and '静海' in strword:
		item['Project_province'] = '天津市'
		item['Project_country'] = '天津市'
		item['Project_district'] = '静海区'

	elif strword and '延边' in strword:
		item['Project_province'] = '吉林省'
		item['Project_country'] = '延边朝鲜族自治州'
		item['Project_district'] = ''

	elif strword and '潍城' in strword:
		item['Project_province'] = '山东省'
		item['Project_country'] = '潍坊市'
		item['Project_district'] = '潍城县'

	elif strword and '璧山' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '璧山县'
	elif strword and '江津' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '江津区'

	elif strword and '延庆' in strword:
		item['Project_province'] = '北京市'
		item['Project_country'] = '北京市'
		item['Project_district'] = '延庆区'


	elif strword and '白沙' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '白沙黎族自治县'
		item['Project_district'] = ''

	elif strword and '渝北' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '渝北区'

	elif strword and '江北' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '江北区'

	elif strword and '神农架' in strword:
		item['Project_province'] = '湖北省'
		item['Project_country'] = '神农架林区'
		item['Project_district'] = '神农架林区'


	elif strword and '人民北路' in strword:
		item['Project_province'] = '广东省'
		item['Project_country'] = '广州市'
		item['Project_district'] = ''

	elif strword and '荣昌' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '荣昌县'

	elif strword and '合川' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '合川区'

	elif strword and '大足' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '大足区'

	elif strword and '辽河源' in strword:
		item['Project_province'] = '吉林省'
		item['Project_country'] = '东辽县'
		item['Project_district'] = '辽河源'

	elif strword and '南京路' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '上海市'
		item['Project_district'] = '和平区'

	elif strword and '和平区' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '上海市'
		item['Project_district'] = '和平区'

	elif strword and '铜梁' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '铜梁区'

	elif strword and '彭水' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '彭水苗族土家族自治县'
		item['Project_district'] = '彭水苗族土家族自治县'

	elif strword and '梁平' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '梁平区'

	elif strword and '潼南' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '潼南县'

	elif strword and '蓟州' in strword:
		item['Project_province'] = '天津市'
		item['Project_country'] = '天津市'
		item['Project_district'] = '蓟州区'

	elif strword and '大理' in strword:
		item['Project_province'] = '云南省'
		item['Project_country'] = '大理白族自治州'
		item['Project_district'] = '大理白族自治州'

	elif strword and '文山' in strword:
		item['Project_province'] = '云南省'
		item['Project_country'] = '文山壮族苗族自治州'
		item['Project_district'] = '文山壮族苗族自治州'

	elif strword and '酉阳' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '酉阳土家族苗族自治县'
		item['Project_district'] = '酉阳土家族苗族自治县'

	elif strword and '武隆' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '武隆区'

	elif strword and '丰都' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '丰都县'

	elif strword and '万州' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '万州区'

	elif strword and '沙坪坝' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '沙坪坝区'

	elif strword and '綦江' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '綦江区'

	elif strword and '开县' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '开州区'

	elif strword and '北碚' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '北碚区'

	elif strword and '石柱' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '石柱土家族自治县'
		item['Project_district'] = '石柱土家族自治县'

	elif strword and '哈平' in strword:
		item['Project_province'] = '黑龙江省'
		item['Project_country'] = '哈尔滨市'
		item['Project_district'] = '动力区'

	elif strword and '秀山' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '秀山土家族苗族自治县'
		item['Project_district'] = '秀山土家族苗族自治县'

	elif strword and '万盛区' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '万盛经济技术开发区'

	elif strword and '南川' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '南川区'

	elif strword and '屯昌' in strword:
		item['Project_province'] = '海南省'
		item['Project_country'] = '屯昌直辖县'
		item['Project_district'] = '屯昌直辖县'

	elif strword and '汉沽' in strword:
		item['Project_province'] = '天津市'
		item['Project_country'] = '天津市'
		item['Project_district'] = '汉沽区'


	elif strword and '宝坻' in strword:
		item['Project_province'] = '天津市'
		item['Project_country'] = '天津市'
		item['Project_district'] = '宝坻县'


	elif strword and '高新区' in strword:
		item['Project_province'] = '四川省'
		item['Project_country'] = '成都市'
		item['Project_district'] = '高新技术产业开发区'


	elif strword and '阳光花苑' in strword:
		item['Project_province'] = '新疆维吾尔自治区'
		item['Project_country'] = '乌鲁木齐市'
		item['Project_district'] = '天山区'


	elif strword and '两江新区' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '两江新区'


	elif strword and '宁河' in strword:
		item['Project_province'] = '天津市'
		item['Project_country'] = '天津市'
		item['Project_district'] = '宁河区'


	elif strword and '大港' in strword:
		item['Project_province'] = '天津市'
		item['Project_country'] = '天津市'
		item['Project_district'] = '大港区'


	elif strword and '崇文' in strword:
		item['Project_province'] = '北京市'
		item['Project_country'] = '北京市'
		item['Project_district'] = '崇文区'


	elif strword and '山南' in strword:
		item['Project_province'] = '西藏自治区'
		item['Project_country'] = '山南市'
		item['Project_district'] = '山南地区'



	elif strword and '林芝' in strword:
		item['Project_province'] = '西藏自治区'
		item['Project_country'] = '林芝市'
		item['Project_district'] = ''


	elif strword and '石景山' in strword:
		item['Project_province'] = '北京市'
		item['Project_country'] = '北京市'
		item['Project_district'] = '石景山区'


	elif strword and '康泰街' in strword:
		item['Project_province'] = '河北省'
		item['Project_country'] = '衡水市'
		item['Project_district'] = '开发区'


	elif strword and '大渡口' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '大渡口区'


	elif strword and '宁河' in strword:
		item['Project_province'] = '天津市'
		item['Project_country'] = '天津市'
		item['Project_district'] = '宁河区'


	elif strword and '永川' in strword:
		item['Project_province'] = '重庆市'
		item['Project_country'] = '重庆市'
		item['Project_district'] = '永川区'


	elif strword and '松江' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '上海市'
		item['Project_district'] = '松江区'


	elif strword and '南汇区' in strword:
		item['Project_province'] = '上海市'
		item['Project_country'] = '上海市'
		item['Project_district'] = '南汇区'


	elif strword and '黄畈村' in strword:
		item['Project_province'] = '湖北省'
		item['Project_country'] = '咸宁市'
		item['Project_district'] = '永川区'


	elif strword and '将军庙' in strword or '鼓楼区' in strword:
		item['Project_province'] = '江苏省'
		item['Project_country'] = '南京市'
		item['Project_district'] = '鼓楼区'

	elif strword and '平安镇' in strword:
		item['Project_province'] = '青海省'
		item['Project_country'] = '海东市'
		item['Project_district'] = '平安区'


	elif strword and '华天道' in strword:
		item['Project_province'] = '天津市'
		item['Project_country'] = '天津市'
		item['Project_district'] = '华苑产业区'


	elif strword and 'xxx' in strword:
		item['Project_province'] = ''
		item['Project_country'] = ''
		item['Project_district'] = ''

	else:
		strwordlist = [strword]
		a = cpca.transform(strwordlist)
		item['Project_province'] = a.loc[0]['省']
		item['Project_country'] = a.loc[0]['市']
		item['Project_district'] = a.loc[0]['区']
		item['Project_adress'] = a.loc[0]['地址']
		item['Project_adcode'] = a.loc[0]['adcode']

	return item


if __name__ == "__main__":
	import cpca

	str_temp = '北京市东城区建国门南大街7号C座506号'
	getLocation = cpca.transform(str_temp)
	print(getLocation)
