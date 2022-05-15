import os,time,pprint,pymysql,sys
import ctypes
import os
import platform
import binascii
from PIL import Image
from os.path import join, getsize
import json
import pandas as pd

def get_timestr(date,outformat = "%Y-%m-%d %H:%M:%S",combdata = False):
    time_array = ''
    format_string = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H",
        "%Y-%m-%d",
        "%Y:%m:%d %H:%M:%S",
        "%Y:%m:%d %H:%M",
        "%Y:%m:%d %H",
        "%Y:%m:%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %H",
        "%Y/%m/%d",
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d %H:%M",
        "%Y.%m.%d %H",
        "%Y.%m.%d",
        "%Y年%m月%d日 %H:%M:%S",
        "%Y年%m月%d日 %H:%M",
        "%Y年%m月%d日 %H",
        "%Y年%m月%d日",
        "%Y_%m_%d %H:%M:%S",
        "%Y_%m_%d %H:%M",
        "%Y_%m_%d %H",
        "%Y_%m_%d",
        "%Y%m%d%H:%M:%S",
        "%Y%m%d %H:%M:%S",
        "%Y%m%d %H:%M",
        "%Y%m%d %H",
        "%Y%m%d",
        "%Y%m%d%H%M%S",
        "%Y%m%d %H%M%S",
        "%Y%m%d %H%M",
        "%Y%m%d %H",
        "%Y%m%d",
        "%Y\%m\%d %H:%M:%S",
        "%Y\%m\%d %H:%M",
        "%Y\%m\%d %H",
        "%Y\%m\%d",
        "%Y年%m月%d日%H:%M:%S",
        "%Y年%m月%d日%H:%M",
        "%Y年%m月%d日%H",
        "%Y年%m月%d日",
    ]
    for i in format_string:

        try:
            time_array = time.strptime(date, i)
        except:
            continue

    if not time_array:
        return None
    timeL1 = int(time.mktime(time_array))
    timeL = time.localtime(timeL1)
    if combdata:
        ddict = {}
        ttime = time.strftime(outformat, timeL).split(' ')
        ddict['Y'] = ttime[0].split('-')[0]
        ddict['M'] = ttime[0].split('-')[1]
        ddict['D'] = ttime[0].split('-')[2]
        ddict['o'] = ttime[1].split(':')[0]
        ddict['m'] = ttime[1].split(':')[1]
        ddict['s'] = ttime[1].split(':')[2]
        ddict['timeC'] = timeL1
        return ddict
    else:
        return time.strftime(outformat,timeL)


def file_name_walk(file_dir):

    listpath = []
    for root, dirs, files in os.walk(file_dir):
        dictTemp = {}
        dictTemp['root'] = root# 当前目录路径
        dictTemp['dirs'] = dirs# 当前路径下所有子目录
        dictTemp['files'] = files# 当前路径下所有非目录子文件
        listpath.append(dictTemp)
    return listpath


def get_free_space_mb(folder):
    """ Return folder/drive free space (in bytes)
    """
    if platform.system() == 'Windows':
        print('if')
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024
    else:

        print('else')
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024/1024


def getdirsize(dir):
   size = 0
   for root, dirs, files in os.walk(dir):
      size += sum([getsize(join(root, name)) for name in files])
   return size


def process_image_Backup(inputPath,outputPath,):

    image = Image.open(inputPath)

    image.save(outputPath)

def format_lati_long(data):
    list_tmp = str(data).replace('[', '').replace(']', '').split(',')
    list = [ele.strip() for ele in list_tmp]
    data_sec = int(list[-1].split('/')[0]) /(int(list[-1].split('/')[1])*3600)# 秒的值
    data_minute = int(list[1])/60
    data_degree = int(list[0])
    result = data_degree + data_minute + data_sec
    return result

def get_FileSize(filePath,roundNum = 2):
    filesize = getsize(filePath)
    filesize = filesize / float(1024*1024)
    filesize = round(filesize,roundNum)
    return filesize

def nonExifImg(filepath):
    ddict = {}
    ddict['Model'] = 'unknowModel'
    ddict['Make'] = 'unknowMake'
    try:
        souimg = Image.open(filepath)
        imgSize = souimg.size
        ddict['Width'] = int(imgSize[0])
        ddict['Length'] = int(imgSize[1])
        ctime = os.path.getctime(imgpath)
        time1 = int(round(ctime*1000))
        ddict['Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time1 / 1000))
        ddict['badFile'] = 0
        souimg.close()
    except:
        ddict['Width'] = 0
        ddict['Length'] = 0
        ddict['Time'] = '1990-01-01 00:00:00'
        ddict['badFile'] = 1
    return ddict

def get_imginfo(imgpath):
    import exifread

    file_ino = os.stat(imgpath).st_ino

    openImg = open(imgpath,'rb')
    exif = exifread.process_file(openImg)
    openImg.close()

    try:
        ddict = {}
        ddict['Make'] = str(exif['Image Make'])
        ddict['Model'] = str(exif['Image Model'])
        ddict['Time'] = str(exif['EXIF DateTimeOriginal'])
        ddict['Width'] = int(str(exif['EXIF ExifImageWidth']))
        ddict['Length'] = int(str(exif['EXIF ExifImageLength']))
        ddict['Exception'] = ''
        ddict['badFile'] = 0
    except Exception as ff:
        ddict = nonExifImg(imgpath)
        ddict['Exception'] = ff

    ddict['Size'] = get_FileSize(imgpath,roundNum=4)
    ddict['PathOld'] = imgpath
    ddict['Time'] = get_timestr(ddict['Time'])
    ddict['Type'] = 'img'
    ddict['st_ino'] = file_ino
    ddict['PathNew'] = move_file(ddict=ddict)
    return ddict

    # latitude = format_lati_long(str(exif['GPS GPSLatitude']))
    # print(latitude)
    # longitude = format_lati_long(str(exif['GPS GPSLongitude']))
    # print(longitude)

def img_precess(path):
    a = file_name_walk(path)
    imgType = ['JPG', 'jpg', 'PNG', 'png', 'jpge','JPGE']
    imgInfoList = []
    for i in a:
        if len(i['files']) > 0:
            for n in i['files']:
                filepath = i['root'] + '/' + n
                filepath = filepath.replace('\\','/')
                endsplit = os.path.splitext(filepath)[-1].replace('.','')
                if endsplit in imgType:
                    imginfo = get_imginfo(filepath)
                    imgInfoList.append(imginfo)
    df = pd.DataFrame(imgInfoList)
    df.to_csv('imgInfoDB.csv',encoding='utf_8_sig')


def move_file(ddict):
    global root
    import shutil
    import random
    newPath_good = os.path.join(root,ddict['Type'])
    # newPath_bad = os.path.join(root,'{}_bad'.format(ddict['Type']))
    if not ddict['Time']:
        print(ddict)
        return ''

    TimeInfo = get_timestr(ddict['Time'],combdata=True)
    beMove_path = newPath_good + "/{Y}/{M}/{D}/".format(Y=TimeInfo['Y'], M=TimeInfo['M'], D=TimeInfo['D'])
    randomSTR = ''.join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 15))
    endsplitName = os.path.splitext(ddict['PathOld'])[-1]
    newFileName = TimeInfo['Y'] + TimeInfo['M'] + TimeInfo['D'] + TimeInfo['o'] + TimeInfo['m'] + TimeInfo['s'] + \
                  TimeInfo['m'] + "_" + str(TimeInfo['timeC']) + "_" + randomSTR + endsplitName
    newFile = os.path.join(beMove_path, newFileName)

    if ddict['badFile'] == 0:
        if not os.path.exists(beMove_path):
            os.makedirs(beMove_path)
    else:
        return ''
        # if not os.path.exists(newPath_bad):
        #     os.mkdir(newPath_bad)

    returnPath = shutil.move(ddict['PathOld'], newFile)
    return returnPath.replace('\\','/')

if __name__ == '__main__':
    # root = r"D:\w"

    # otherFileType = ['HEIC', 'JPG_bk', 'mov', 'db', 'mp3', 'pdf', 'tmp', 'MOV', 'wav', 'mp4']
    # imgfile = r'D:\w\[备份]祖娅娟的土豪金\相册\2013年09月/IMG_6016.JPG'.replace('\\','/')
    # imgfile = "D:\w\共享\.piccache\XiaoMi\祖娅娟ip6/2AA91447-1214-45B4-B4A2-A2DC54172527-624-00000084E0B9A342_tmp.jpg".replace('\\','/')
    # imgpath = r'\\JINXX1-HTPC-I5\family'
    # imgpath = r"X:\family"
    # imgpath = r"D:\w"
    # get_imginfo(imgfile)
    #
    #
    # exit()
    root = r'D:/w'
    img_precess(root)





