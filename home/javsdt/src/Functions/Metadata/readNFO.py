# -*- coding:utf-8 -*-
import os, sys, shutil, pprint
import pprint
import json
import re

from bs4 import BeautifulSoup
from Car import find_car_youma
from json import load
import pandas as pd



def read_json_to_dict(path):
	f = open(path, encoding='utf-8')
	dict_json = load(f)
	f.close()
	return dict_json


# 展示所有json中的某一项，某一项由手动输入
def show_jsons_one_element_by_dir_choose():
	dir_choose = r"D:\PythonCode\home\javsdt\【重要须备份】已整理的jsons"
	llist = []
	for root, dirs, files in os.walk(dir_choose):
		for file in files:
			if file.endswith(('.json',)):
				path = os.path.join(root, file)
				try:
					dict_json = read_json_to_dict(path)
				except:
					print('error')
					print(path)
				dict_json['jsonPath'] = path
				llist.append(dict_json)

				yield dict_json


def readNFO(nfoPath):
	with open(nfoPath, 'r', encoding='utf-8') as ff:
		nfoWord = ff.read()
	soup = BeautifulSoup(nfoWord, 'html.parser')
	return soup


import numpy as np


class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, (np.int, np.int_, np.intc)):
			return int(obj)
		elif isinstance(obj, (np.float_, np.float, np.float32, np.float64)):
			return float(obj)
		elif isinstance(obj, (np.ndarray)):
			return obj.tolist()
		return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':

	ww = tuple("mp4、mkv、avi、wmv、iso、rmvb、flv、ts、MP4、MKV、AVI、WMV、RMVB、FLV、TS".split('、'))

	ote = tuple("jpg、JPG、nfo、NFO".split('、'))
	# ['mht', 'gif', 'json', 'zip', 'lnk', 'srt', 'URL', 'png', 'ass', 'chm']
	subsp = tuple(['srt','ass','SRT','ASS'])

	otlist= ww+ote
	nonmosaic = r"D:\PythonCode\home\AV_subtitle\nonMosaic.csv"
	# with open(nonmosaic,'r',encoding='utf-8') as f:
	# 	csv = f.read()
	rootPath = r"Z:\x299\JS寄生虫.720p.1080p.HD中字\6v电影APP 有他不迷路\appsiteweb\PIDEO_ROOT\newRoot\归类完成"
	csvdf = pd.read_csv(nonmosaic,index_col=0)
	csvdf['fanhao'] = csvdf['fanhao'].str.upper()
	# llist = []
	# for root, dirs, files in os.walk(rootPath):
	# 	if not files or '.actors' in root:
	# 		continue
	#
	# 	for ifile in files:
	# 		if ifile.endswith('.nfo'):
	# 			nfoPath = os.path.join(root, ifile)
	# 			nfoSoup = readNFO(nfoPath)
	# 	nfo_title = str(nfoSoup.title.get_text())
	# 	getCar = find_car_youma(nfo_title, [])
	# 	llist.append(getCar)
	# print(llist)

	llist = ['ABP-942', 'ABP-911', 'ABP-041', 'ABP-933', 'ABP-901', 'ABP-651', 'ABP-447', 'ABP-948', 'ABP-724', 'ABP-855', 'ABP-893', 'ABS-141', 'ABS-212', 'ABW-157', 'ACME-003', 'ADN-354', 'ADN-352', 'ADN-122', 'ADZ-178', 'AGAV-022', 'ARM-977', 'ARM-718', 'ATID-318', 'ATID-219', 'AVOP-208', 'AVOP-227', 'BB-003', 'BEB-078', 'BF-567', 'BGN-056', 'BGN-044', 'BLK-414', 'BTYD-002', 'BTYD-007', 'BTYD-013', 'BTYD-019', 'CAND-049', 'CAWD-299', 'CAWD-300', 'CAWD-308', 'CESD-815', 'CESD-586', 'CJOD-173', 'CJOD-182', 'CLUB-557', 'DANDY-421', 'DASD-529', 'DASD-641', 'DASD-732', 'DASD-696', 'DENJ-001', 'DOCP-237', 'DOKS-531', 'DRC-006', 'DV-1623', 'DV-1205', 'DV-1633', 'DV-1656', 'DV-1665', 'DV-1682', 'DV-1625', 'DV-1475', 'DVAJ-0041', 'DVAJ-331', 'DVAJ-355', 'DVDES-808', 'DVDMS-486', 'EBOD-260', 'EBOD-843', 'EKDV-577', 'FAA-239', 'FAX-502', 'FSDSS-257', 'FSDSS-110', 'FSDSS-078', 'FSDSS-304', 'FSDSS-012', 'FSDSS-017', 'FSDSS-039', 'FSDSS-048', 'FSET-324', 'GENM-043', 'GRCH-262', 'GVH-087', 'GVH-103', 'HAVD-837', 'HBAD-360', 'HFD-195', 'HMN-051', 'HND-737', 'HND-656', 'HND-667', 'HND-723', 'HND-658', 'HND-481', 'HND-990', 'HODV-21482', 'HOMA-038', 'HONB-077', 'HUNTA-561', 'HUNTA-219', 'HUNTA-562', 'HUNTA-723', 'HYPN-023', 'IPX-532', 'IPX-457', 'IPX-748', 'IPX-738', 'IPX-439', 'IPX-471', 'IPX-582', 'IPX-744', 'IPX-105', 'IPX-149', 'IPX-265', 'IPX-292', 'IPX-353', 'IPX-384', 'IPX-485', 'IPX-690', 'IPX-742', 'IPX-736', 'IPX-091', 'IPX-273', 'IPX-358', 'IPX-375', 'IPX-299', 'IPX-297', 'IPZ-508', 'IPZ-941', 'IPZ-995', 'IPZ-261', 'JUFE-047', 'JUL-242', 'JUL-401', 'JUL-660', 'JUL-566', 'JUX-377', 'JUY-974', 'JUY-952', 'JUY-812', 'JUY-819', 'JUY-397', 'JUY-816', 'JUY-818', 'KAWD-731', 'KMHRS-023', 'LAS-014', 'LID-047', 'MARA-018', 'MBYD-305', 'MCT-008', 'MDTM-384', 'MDTM-388', 'MDYD-930', 'MEYD-014', 'MEYD-479', 'MEYD-493', 'MEYD-540', 'MEYD-548', 'MEYD-555', 'MEYD-421', 'MIAA-517', 'MIAA-230', 'MIAA-452', 'MIAA-049', 'MIAA-024', 'MIAA-037', 'MIAA-041', 'MIAA-051', 'MIAA-076', 'MIAA-085', 'MIAA-096', 'MIAA-100', 'MIAA-119', 'MIAA-122', 'MIAA-151', 'MIAA-170', 'MIAA-171', 'MIAA-203', 'MIAA-221', 'MIAA-335', 'MIAA-161', 'MIAA-142', 'MIAD-767', 'MIDD-791', 'MIDE-520', 'MIDE-988', 'MIDE-515', 'MIDE-531', 'MIDE-540', 'MIDE-549', 'MIDE-558', 'MIDE-565', 'MIDE-571', 'MIDE-580', 'MIDE-586', 'MIDE-595', 'MIDE-604', 'MIDE-613', 'MIDE-624', 'MIDE-634', 'MIDE-643', 'MIDE-649', 'MIDE-657', 'MIDE-666', 'MIDE-674', 'MIDE-680', 'MIDE-690', 'MIDE-705', 'MIDE-715', 'MIDE-911', 'MIDE-950', 'MIDE-974', 'MIDE-989', 'MIDE-843', 'MIDE-985', 'MIDE-708', 'MIDE-842', 'MIDE-456', 'MIDE-500', 'MIDE-943', 'MIFD-187', 'MIFD-067', 'MILD-736', 'MIMK-056', 'MIMK-070', 'MIZD-157', 'MIZD-168', 'MMGH-220', 'MMND-141', 'MMND-143', 'MMND-168', 'MMND-184', 'MUDR-085', 'MUDR-098', 'MUDR-010', 'MUM-098', 'MVSD-410', 'MVSD-481', 'MXBD-194', 'MXBD-220', 'MXGS-784', 'MXGS-834', 'MXGS-038', 'NDRA-067', 'NHDTA-141', 'NHDTA-540', 'NHDTA-982', 'NHDTA-927', 'NHDTB-359', 'NHDTB-031', 'NKKD-009', 'NKKD-105', 'NNPJ-307', 'NNPJ-475', 'NSPS-281', 'NTR-007', 'OAE-171', 'OAE-185', 'OFJE-329', 'OFJE-318', 'OIGS-029', 'OKSN-285', 'ONSD-340', 'OVG-147', 'PBD-104', 'PBD-358', 'PFES-005', 'PGD-348', 'PPPD-939', 'PPPD-807', 'PRED-116', 'PRED-139', 'PRED-144', 'PRED-170', 'PRED-175', 'PRED-181', 'PRED-189', 'PRED-196', 'PRED-210', 'PRED-218', 'PRED-164', 'PSD-408', 'PTS-443', 'RCT-126', 'RCT-502', 'RCT-446', 'RED-040', 'RED-077', 'RED-097', 'RS-018', 'SABA-727', 'SCG-010', 'SDAB-129', 'SDAM-044', 'SDAM-046', 'SDDE-598', 'SDDE-625', 'SDMF-012', 'SDMM-028', 'SDMM-063', 'SDMS-682', 'SDMT-559', 'SDMT-788', 'SDMU-963', 'SDNM-229', 'SDNT-007', 'SDNT-005', 'SDNT-009', 'SERO-0158', 'SHYN-102', 'SIRO-3749', 'SIRO-3704', 'SIRO-3733', 'SMD-02', 'SMD-03', 'SNIS-386', 'SNIS-917', 'SNIS-937', 'SNIS-960', 'SNIS-983', 'SNIS-642', 'SNIS-675', 'SNIS-573', 'SNIS-585', 'SNIS-206', 'SOE-768', 'SOE-146', 'SPRD-1449', 'SSIS-214', 'SSIS-102', 'SSIS-089', 'SSIS-117', 'SSIS-145', 'SSIS-195', 'SSNI-453', 'SSNI-458', 'SSNI-036', 'SSNI-081', 'SSNI-348', 'SSNI-436', 'SSNI-456', 'SSNI-546', 'SSNI-569', 'SSNI-647', 'SSNI-706', 'SSNI-005', 'SSNI-025', 'SSNI-048', 'SSNI-071', 'SSNI-094', 'SSNI-764', 'SSNI-012', 'SSNI-454', 'SSNI-518', 'SSNI-567', 'SSNI-591', 'SSNI-619', 'SSNI-731', 'SSNI-757', 'SSNI-803', 'SSNI-866', 'SSNI-889', 'SSNI-964', 'SSNI-704', 'SSNI-378', 'SSNI-056', 'SSNI-574', 'SSPD-117', 'SSPD-130', 'STAR-573', 'STAR-236', 'STARS-402', 'STARS-089', 'STARS-140', 'STARS-156', 'STARS-216', 'STARS-229', 'STARS-247', 'STARS-226', 'STARS-238', 'STARS-250', 'STARS-141', 'STARS-253', 'STARS-239', 'STARS-127', 'STARS-145', 'STARS-232', 'STARS-332', 'STARS-408', 'STARS-123', 'STARS-154', 'STARS-252', 'STARS-120', 'STARS-160', 'STARS-323', 'STARS-036', 'STARS-152', 'STARS-182', 'STARS-225', 'STARS-308', 'STKO-004', 'STKO-003', 'SUPA-385', 'SVDVD-264', 'SVDVD-568', 'SW-261', 'SW-561', 'SW-387', 'T28-546', 'TMWD-007', 'TOMN-094', 'TOS-003', 'VDD-116', 'VENU-830', 'VOSS-126', 'VRTM-456', 'VRTM-498', 'WAAA-101', 'WANZ-853', 'WANZ-855', 'WANZ-844', 'WANZ-851', 'WANZ-909', 'WANZ-763', 'ZSD-074']

	newList = []
	for i in range(len(csvdf)):
		# print(csvdf.iloc[i].fanhao)
		# continue
		if str(csvdf.iloc[i].fanhao) not in llist:
			# csvdf.drop(labels=[i],axis=0,inplace=True)
			ddict = {}
			ddict['car'] = str(csvdf.iloc[i].fanhao)
			ddict['cc'] = csvdf.iloc[i].cc
			ddict['name'] = csvdf.iloc[i].name
			ddict['size'] = csvdf.iloc[i].size
			newList.append(ddict)
	df = pd.DataFrame(newList)
	df.to_csv('aaa.csv',encoding='utf_8_sig')





	exit()




	# jsonDB = pd.DataFrame([x for x in show_jsons_one_element_by_dir_choose()])
	# print(jsonDB)
	# jsonDB.rename(columns={'Car':"fanhao"},inplace=True)
	# print(jsonDB)
	# newDF = pd.concat([csvdf,jsonDB,csvdf]).drop_duplicates(keep=False)

	# newDF1= pd.merge(csvdf,jsonDB,on='fanhao',how='outer')
	# newDF1 = csvdf.append(jsonDB)



	# newDF = newDF1.drop_duplicates(subset=['fanhao','cc'],keep='first')
	# newDF = newDF.dropna(subset=['cc'])
	# newDF.to_csv('aaa.csv',encoding='utf_8_sig')
	# # print(newDF)
	# aa = newDF[newDF[['jsonPath']].isnull().T.any()][['fanhao','cc']]
	# print(aa)
	# aa.to_csv('aaa.csv')






	exit()
	nfoName = r"BGN-056㊥ 新人 プレステージ専属デビュー 美女神、爆誕。（日本一エッチなさいとうさん） 斎藤あみり2019.nfo"
	nfoFolder = r"Z:\x299\JS寄生虫.720p.1080p.HD中字\6v电影APP 有他不迷路\appsiteweb\PIDEO_ROOT\newRoot\归类完成\BGN\斎藤あみり\【斎藤あみり】BGN-056㊥"
	rootPath = nfoFolder.replace('BGN\斎藤あみり\【斎藤あみり】BGN-056㊥', '')
	catList = []
	catDUP = []
	for root, dirs, files in os.walk(rootPath):
		if not files or '.actors' in root:
			continue
		mark = 0
		nfoSoup = None


		for ifile in files:
			if ifile.endswith(ww):
				mark += 1
			if ifile.endswith('.nfo'):
				nfoPath = os.path.join(root, ifile)
				nfoSoup = readNFO(nfoPath)
		nfo_title = str(nfoSoup.title.get_text())
		getCar = find_car_youma(nfo_title, [])
		# catList = []
		# catDUP = []
		if getCar in catList:
			catDUP.append(getCar)
		else:
			catList.append(getCar)

		json_Result = jsonDB[jsonDB['Car'] == getCar]
		genreList = [x.get_text() for x in nfoSoup.find_all('genre')]
		ch = ''
		wu = ''
		if '中文字幕' in genreList:
			ch = '㊥'
		if '无码流出' in genreList:
			wu = '【流】'
		try:
			with open(json_Result.iloc[0].jsonPath, 'r', encoding='utf-8') as fjson:
				jsonR = json.load(fjson)
		except:
			continue


		p1 = json_Result.iloc[0]
		if jsonR['Actors']:
			if len(jsonR['Actors']) == 1:
				aa = jsonR['Actors'][0]
			if len(jsonR['Actors']) >= 2:
				aa = '、'.join(jsonR['Actors'][0:2])
			aoctors = "【" + aa + "】"
		else:
			aoctors = ''
		lllist = ["\\","/","|","<",">","?",":","！","”","*","…"]
		titlezh = str(json_Result.iloc[0].TitleZh)[0:30]
		for ii in lllist:
			titlezh = titlezh.replace(ii,'')

		newFileName = '[' + getCar + ']' + wu + ch + aoctors + ' ' + titlezh
		newFileName = newFileName.replace('乳头', '乳首')
		# print(newFileName)
		globFileName = ''
		for ifile in files:
			if ifile.endswith(ww):
				if mark == 2:
					ifilesplit = ifile.split('-cd')
					nfile = newFileName + '-cd' + ifilesplit[1]
					if not globFileName:
						globFileName = nfile
				else:
					sp = ifile.split('.')[-1]
					nfile = newFileName + '.' + sp
					globFileName = nfile

				oldName = os.path.join(root, ifile)
				newName = os.path.join(root, nfile)
				os.rename(oldName, newName)

		for ifile in files:
			globFileName1 = globFileName.split('.')[0]
			if ifile.endswith('nfo'):
				try:
					oldnfo = os.path.join(root, ifile)
					newnfo = os.path.join(root, globFileName1 + '.nfo')
					os.rename(oldnfo, newnfo)
				except:
					continue

			if ifile.endswith(subsp):
				sp = ifile.split('.')[-1]
				try:
					oldsubTitle = os.path.join(root, ifile)
					newsubTitle = os.path.join(root, globFileName1 + '.' + sp)
					os.rename(oldsubTitle, newsubTitle)
				except:
					continue


			if ifile.endswith('jpg'):
				oldjpg = os.path.join(root, ifile)
				if 'fanart' in ifile:
					# print('fanart')
					try:
						newjpg = os.path.join(root, globFileName1 + '-fanart.jpg')
						os.rename(oldjpg, newjpg)
					except:
						continue
				if 'poster' in ifile:
					try:
						newjpg = os.path.join(root, globFileName1 + '-poster.jpg')
						os.rename(oldjpg, newjpg)
					except:
						continue
				else:
					continue

	print(list(set(catDUP)))
	# print(catList)
	exit()
