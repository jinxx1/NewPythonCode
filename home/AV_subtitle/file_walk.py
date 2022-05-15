import os
import pprint, json
import re, sys, shutil
from DB_ORM import *

# root = os.getcwd()
# fanhaoAllJSONPath = os.path.join(root, '00FanHaoAll.json')
# with open(fanhaoAllJSONPath, 'r') as f123:
# 	fanhaoAllList = json.load(f123)
# 	f123.close()
#
# fanhaoAllList.sort(key=lambda x: len(x), reverse=True)
fileType_s = "mp4、mkv、avi、wmv、iso、rmvb、flv、ts".split('、')
fileType_b = [x.upper() for x in fileType_s]
video_sp_list = fileType_s + fileType_b


def mkdir(path):
	folder = os.path.exists(path)

	if not folder:
		os.makedirs(path)
		return None
	else:
		return True


def file_name_walk(file_dir=None, getwhat='files'):
	noListsuffix = [
		# "JPG", 'PNG', 'JPEG',
		# 'DMP', 'ZIP', 'RAR', 'MOV', 'TORRENT', 'TXT', 'ASF'
	]
	listpath = []
	for root, dirs, files in os.walk(file_dir):
		dictTemp = {}
		dictTemp['root'] = root  # 当前目录路径
		dictTemp['dirs'] = dirs  # 当前路径下所有子目录
		dictTemp['files'] = files  # 当前路径下所有非目录子文件
		if not dirs and not files and root != file_dir:
			os.rmdir(root)
		mark = 0
		for f in files:
			sp = f.split('.')[-1].strip()
			if sp in video_sp_list:
				mark = 1
		if mark == 0:
			print(root)
			print(files)
			print('----------')

		if getwhat == 'files':
			if not dictTemp['files']:
				continue

			for x in dictTemp['files']:
				sp = os.path.splitext(x)[-1]
				# ''.upper()
				if "!" not in sp and sp.upper() not in noListsuffix:
					ddict = {}
					sep = os.sep
					ddict['dir'] = root.replace(sep, '/')
					ddict['filepath'] = os.path.join(root, x).replace(sep, '/')
					ddict['file'] = x
					ddict['fanhao'] = regexFanhao(ddict['file'])
					ddict['suffix'] = sp
					listpath.append(ddict)
					yield ddict

		elif getwhat == 'root':
			if not dictTemp['files']:
				continue
			yield dictTemp

		else:
			raise 'not type getwhat'


def regexFanhao(file):
	if 'MXNB-001S' in file.upper():
		car_pref = 'MXNB-'
		car_suf = '001S'
		return f'{car_pref}{car_suf}'
	if 'DVAJ-0041' in file.upper():
		car_pref = 'DVAJ-'
		car_suf = '0041'
		return f'{car_pref}{car_suf}'
	if "LAFBD-41" in file.upper():
		car_pref = 'LAFBD-'
		car_suf = '41'
		return f'{car_pref}{car_suf}'


	cutFanHaoList = ['HEYZO', 'PONDO', 'CARIB', 'OKYOHOT', 'CUTE', '10MU',
	                 '10MUS', '10MUSU', '10MUSUM', '10MUSUME', 'MUS', 'MUSU', 'MUSUM', 'MUSUME',
	                 '1PONDO', 'PON']

	for cutWrod in cutFanHaoList:
		if cutWrod in file.upper():
			return ''

	# car_pref 车牌前缀 ABP-，带横杠；car_suf，车牌后缀 123。
	# 先处理特例 T28 车牌
	mark = 0
	if re.search(r'[^A-Z]?T28[-_ ]*\d\d+', file):
		car_pref = 'T28-'
		car_suf = re.search(r'T28[-_ ]*(\d\d+)', file).group(1)
		mark = 1
	# 以javbus上记录的20ID-020为标准
	if re.search(r'(\d\d)ID[-_ ]*(\d\d+)', file):
		carg = re.search(r'(\d\d)ID[-_ ]*(\d\d+)', file)
		car_pref = 'ID-'
		car_suf = f'{carg.group(1)}{carg.group(2)}'
		mark = 1
	# 一般车牌
	# '''---------------------------------------'''

	if mark == 0:
		fhPath = r"D:\PythonCode\home\AV_subtitle\00FanHaoAll.json"
		with open(fhPath, 'r') as ff1:
			fanhaoAllList = json.load(ff1)
			ff1.close()
		fanhaoAllList.sort(key=lambda x: len(x), reverse=True)
		for fh in fanhaoAllList:

			if fh and fh in file.upper():
				# print(fh)
				reg = re.compile(r"%s\d{3,6}" % fh)
				getreg = reg.search(file.upper())
				if getreg:
					aa = getreg.group().upper().replace(fh, fh + '-')
					bb = aa.replace('--', '-')

					try:
						car_pref = bb.split('-')[0] + '-'
						car_suf = bb.split('-')[1]
						mark = 1
						break
					except:
						mark = 0

	if mark == 0:
		reg = re.compile("([A-Z]{3,6}-\d{3,6})")
		getreg = reg.search(file.upper())
		if getreg:
			aa = getreg.group().upper()
			bb = aa.replace('--', '-')
			try:
				car_pref = bb.split('-')[0] + '-'
				car_suf = bb.split('-')[1]
				mark = 1
			except:
				mark = 0

	if mark == 0:
		reg = re.compile("([A-Z]{3,6}\d{3})")
		getreg = reg.search(file.upper())
		if getreg:
			regsuf = re.compile("\d{3}")
			getregTemp = regsuf.search(getreg.group().upper()).group()
			aa = getreg.group().upper().replace(getregTemp, '-' + getregTemp)
			bb = aa.replace('--', '-')
			try:
				car_pref = bb.split('-')[0] + '-'
				car_suf = bb.split('-')[1]
				mark = 1

			except:
				mark = 0

	if re.search(r'([A-Z]+)[-_ ]*(\d\d+)', file) and mark == 0:
		carg = re.search(r'([A-Z]+)[-_ ]*(\d\d+)', file)
		car_pref = carg.group(1)
		car_pref = f'{car_pref}-'
		car_suf = carg.group(2)
		mark = 1

	if mark == 1:
		# 去掉太多的0，avop00127 => avop-127
		if len(car_suf) > 33:
			car_suf = f'{car_suf[:-3].lstrip("0")}{car_suf[-3:]}'
		return f'{car_pref}{car_suf}'
	else:
		return ''


def readJson_getDict(jsonpath):
	import json
	with open(jsonpath, 'r', encoding='utf-8') as ff:
		return json.load(ff)


def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)


def get_FileSize(filePath):
	# filePath = unicode(filePath,'utf8')
	fsize = os.path.getsize(filePath)
	fsize = fsize / float(1024 * 1024)
	return round(fsize, 2)


if __name__ == '__main__':

	# aa = "lzwm-031-中文"
	# bb = regexFanhao(aa)
	# print(bb)
	#
	# exit()

	subtitleDB = subTitle_OBJ()
	PATH_old = r"D:\BT_download\sucess"
	PATH_new = r"Z:\x299\JS寄生虫.720p.1080p.HD中字\6v电影APP 有他不迷路\appsiteweb\PIDEO_ROOT\newRoot"
	chinese_str_list = ['_C', '_CH', 'ch', 'CH', '_ch', '中文字幕','中文', '字幕', '-C', '-c']
	subtitle_spliter = ['idx', 'sub', 'ass', 'ASS', 'SRT', 'smi', 'ssa', 'srt', 'vtt']
	sep = os.sep
	mark = 0
	for num, rootInfo in enumerate(file_name_walk(file_dir=PATH_old, getwhat='root')):
		for file in rootInfo['files']:
			if file == 'noremove.txt':
				continue
			sp = file.split('.')[-1]
			filePath = os.path.join(rootInfo['root'], file)
			fileSize = get_FileSize(filePath)
			fanhao = regexFanhao(file)
			if not fanhao and fileSize < 400.00 and filePath != PATH_old:
				os.remove(filePath)
				continue
			newFanHaoFolder = os.path.join(PATH_new, fanhao)
			mkdir(newFanHaoFolder)
			chineseGet = ''
			for cc in chinese_str_list:
				if cc in file:
					chineseGet = "中文字幕"
			subTitle_Get_List = subtitleDB.find_info(byid=fanhao)
			if subTitle_Get_List:
				chineseGet = "中文字幕"
				subTitle_Get = subTitle_Get_List[0]
				for i in subTitle_Get_List:
					if i['suffix'].upper() == 'ASS':
						subTitle_Get = i
						break
			wuma = ''
			if '无码流出' in file or 'uncensored' in file:
				wuma = '无码流出'
			newFileName = fanhao + "_" + chineseGet + "_" + wuma
			newFilePath = os.path.join(newFanHaoFolder, newFileName + "." + sp)
			if subTitle_Get_List:
				subTitleFileName = newFileName + "." + subTitle_Get['suffix']
				newsubTitleFilePath = os.path.join(newFanHaoFolder, subTitleFileName)
				shutil.copy(subTitle_Get['filePath'], newsubTitleFilePath)

			if not os.path.exists(newFilePath):
				filemove = shutil.move(filePath, newFilePath)
		try:
			os.rmdir(rootInfo['root'])
		except Exception as ff:
			print(ff)
			pass
