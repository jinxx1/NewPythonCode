import datetime
import os, random, shutil
import pprint
import time


def file_walk(path):
	for root, dirs, files in os.walk(path):
		if files:
			for file in files:
				filePath = os.path.join(root, file)
				yield filePath, file


# 按间距中的绿色按钮以运行脚本。
def mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)


def timeT():
	import time
	t = time.time()
	nowTime = lambda: int(round(t * 100000000))
	return int(nowTime())


def main():
	splist = ['GIF', 'MP3', 'ZIP', 'JPG_BK', 'MP4', 'PNG', 'JPG', 'TMP', 'LIVP', 'WAV', 'DB', 'HEIC', 'PDF', 'MOV']
	oldpath = r"D:\w"
	newfolder = r"D:\w1"

	for filePath, file in file_walk(oldpath):
		spl = filePath.split('.')[-1]
		newPath = os.path.join(newfolder, spl.upper())
		mkdir(newPath)
		newfileName = str(timeT()) + '_' + file
		newFilePath = os.path.join(newPath, newfileName)
		shutil.move(filePath, newFilePath)


def delSameSizeFile(root):
	mark = 0
	for root, dirs, files in os.walk(root):
		if files:
			filesizeList = []
			for file in files:
				old_filePath = os.path.join(root, file)
				fileSize = os.path.getsize(old_filePath)
				# print(fileSize)
				if fileSize not in filesizeList:
					filesizeList.append(fileSize)
				else:
					os.remove(old_filePath)
					print(old_filePath)
					print(fileSize)
					mark += 1
					print('-----------')

	print(mark)


def picTureMain():
	import exifread
	import json
	import urllib.request
	import re

	old_root = r"D:\w1\JPG"
	# old_root = r"D:\w1\JPG_ClearUp\2021\11\23"
	new_root = r"D:\w1\JPG_ClearUp"

	for root, dirs, files in os.walk(old_root):
		if files:
			for file in files:
				old_filePath = os.path.join(root, file)
				old_file = file
				dateTime = None
				with open(old_filePath, 'rb') as ff:
					try:
						tags = exifread.process_file(ff)
						for key in tags.keys():
							if 'DateTimeOriginal'.upper() in key.upper():
								dateTime = datetime.datetime.strptime(str(tags[key]), '%Y:%m:%d %H:%M:%S')
					except:
						pass
				# print('-----------')
				# continue

				if not dateTime:
					regxTime = re.compile("\d{4}-\d{2}-\d{2}")
					getTime = regxTime.search(file)
					if getTime:
						dateTime = datetime.datetime.strptime(str(getTime.group()), '%Y-%m-%d')

				if not dateTime:
					mtime = os.stat(old_filePath).st_mtime
					ctime = os.stat(old_filePath).st_ctime
					if mtime >= ctime:
						tureTime = ctime
					else:
						tureTime = mtime
					dateTime = datetime.datetime.fromtimestamp(tureTime)

				if dateTime:
					year = dateTime.strftime('%Y')
					month = dateTime.strftime('%m')
					day = dateTime.strftime('%d')
					y_folder = os.path.join(new_root, year)
					mkdir(y_folder)
					m_folder = os.path.join(y_folder, month)
					mkdir(m_folder)
					d_folder = os.path.join(m_folder, day)
					mkdir(d_folder)
					buildHeader = "【{}-{}-{}】".format(year, month, day)
					try:
						cutWord = old_file.split('】')[0] + '】'
						newFileName = old_file.replace(cutWord, buildHeader)
					except:
						newFileName = buildHeader + old_file

					new_jpg_path = os.path.join(d_folder, newFileName)
					shutil.move(old_filePath, new_jpg_path)


def videoTureMain():
	import re

	old_roots = [r"D:\w1\MP4", r"D:\w1\MOV"]
	new_root = r"D:\w1\Video_CleraUp"
	for old_root in old_roots:

		for root, dirs, files in os.walk(old_root):
			if files:
				for old_File in files:
					old_Video_File_Path = os.path.join(root, old_File)

					dateTime = None
					regxTime = re.compile("\d{4}-\d{2}-\d{2}")
					getTime = regxTime.search(old_File)
					if getTime:
						dateTime = datetime.datetime.strptime(str(getTime.group()), '%Y-%m-%d')

					if not dateTime:
						mtime = os.stat(old_Video_File_Path).st_mtime
						ctime = os.stat(old_Video_File_Path).st_ctime
						if mtime >= ctime:
							tureTime = ctime
						else:
							tureTime = mtime

						dateTime = datetime.datetime.fromtimestamp(tureTime)

					if dateTime:
						year = dateTime.strftime('%Y')
						month = dateTime.strftime('%m')
						day = dateTime.strftime('%d')
						y_folder = os.path.join(new_root, year)
						mkdir(y_folder)
						m_folder = os.path.join(y_folder, month)
						mkdir(m_folder)
						d_folder = os.path.join(m_folder, day)
						mkdir(d_folder)
						buildHeader = "【{}-{}-{}】".format(year, month, day)

						try:
							cutWord = old_File.split('_')[0] + '_'
							newFileName = old_File.replace(cutWord, buildHeader)

						except:
							newFileName = buildHeader + old_File
						# print(newFileName)
						new_video_path = os.path.join(d_folder, newFileName)
						shutil.move(old_Video_File_Path, new_video_path)


if __name__ == '__main__':
	# delSameSizeFile(r"D:\w1\Video_CleraUp")
	picTureMain()

	# videoTureMain()
