import os
import json
from mysql_processing import insert_bugfileinfo
from excel_pro import ExcelMod
# from excel_processing import ExcelMod
import datetime
starttime = datetime.datetime.now()

def file_name_walk(file_dir):
    listpath = []
    for root, dirs, files in os.walk(file_dir):
        dictTemp = {}
        dictTemp['root'] = root# 当前目录路径
        dictTemp['dirs'] = dirs# 当前路径下所有子目录
        dictTemp['files'] = files# 当前路径下所有非目录子文件
        listpath.append(dictTemp)
    return listpath

def jsonload(jsonPath):
    try:
        with open(jsonPath, 'r') as jf:
            jsonLoad = json.load(jf)
            jf.close()
    except:
        with open(jsonPath, 'w') as jf:
            jsonLoad = {}
            jsonLoad['path'] = []
            json.dump(jsonLoad, jf)
            jf.close()
    return jsonLoad

def jsonwrite(jsonPath,item):
    with open(jsonPath, 'w') as jf:
        json.dump(item,jf)
        jf.close()

if __name__ == "__main__":
    rootPath = os.getcwd().replace('\\','/')
    jsonPath = rootPath + '/pathJson.json'
    FilePath = rootPath + '/File'
    FilePath = 'C:\PthonCode\Python_script\File'
    pathItem = jsonload(jsonPath)

    # 逐层扫描FilePath中的全部文件，返回list文件，每个list元素为一个字典实例。
    # root是文件集地址，files是文件名称list
    fileAll = file_name_walk(FilePath)
    for tis in fileAll:
        if tis['files']:
            for num,fileName in enumerate(tis['files']):
                # 制作文件path地址

                winPath = tis['root'] + '/' + fileName
                filePath = winPath.replace('\\','/')
                if filePath in pathItem['path']:
                    continue
                try:
                    excel_get = ExcelMod(filePath)
                except PermissionError:
                    insert_bugfileinfo(filePath,'PermissionError')
                    print('请确定是否有这个文件：',fileName)
                    print('已保存到bugfileinfo库中')
                pathItem['path'].append(filePath)
                jsonwrite(jsonPath,pathItem)

    print('\n---------------------------Python Script完成---------------------------')
    endtime = datetime.datetime.now()
    print(endtime - starttime)
