# -*- coding: utf-8 -*-

from contextlib import closing
import requests
import xlrd
import os

def file_name_walk(file_dir):
    listpath = []
    for root, dirs, files in os.walk(file_dir):
        dictTemp = {}
        dictTemp['root'] = root# 当前目录路径
        dictTemp['dirs'] = dirs# 当前路径下所有子目录
        dictTemp['files'] = files# 当前路径下所有非目录子文件
        listpath.append(dictTemp)
    return listpath


def getStartNum(rows,cols,word):
    cellinfo = {}
    for xx in range(rows):
        for yy in range(cols):
            cell_value = word.cell_value(xx,yy)
            if '序' in str(cell_value):
                cellinfo['xuhaoX'] = xx
                cellinfo['xuhaoY'] = yy
                break
        if cellinfo:
            break
    return cellinfo

def dDict():
    ddict = {}

    ddict['tb2'] = {}
    ddict['tb2']['ori_id'] = []
    ddict['tb2']['declare_year'] = []
    ddict['tb2']['year_2017'] = []
    ddict['tb2']['year_2018'] = []

    ddict['tb3'] = {}
    ddict['tb3']['ori_id'] = []
    ddict['tb3']['certificate_name'] = []
    ddict['tb3']['certificate_id'] = []
    ddict['tb3']['certificate_organization'] = []
    ddict['tb3']['certificate_around'] = []
    ddict['tb3']['certificate_getdate'] = []
    ddict['tb3']['certificate_enddate'] = []

    ddict['tb4'] = {}
    ddict['tb4']['ori_id'] = []
    ddict['tb4']['name'] = []
    ddict['tb4']['work_experience'] = []
    ddict['tb4']['credentials'] = []
    ddict['tb4']['professional_title'] = []
    ddict['tb4']['professional_level'] = []
    ddict['tb4']['professional_id'] = []
    ddict['tb4']['professional_organization'] = []
    ddict['tb4']['attribute'] = []
    ddict['tb4']['introduction'] = []
    ddict['tb4']['professional_verification'] = []
    ddict['tb4']['social_security'] = []
    ddict['tb4']['preson_id'] = []



    ddict['tb5'] = {}
    ddict['tb5']['ori_id'] = []
    ddict['tb5']['name'] = []
    ddict['tb5']['province'] = []
    ddict['tb5']['exam_name'] = []
    ddict['tb5']['professional'] = []
    ddict['tb5']['exam_region'] = []
    ddict['tb5']['grade'] = []
    ddict['tb5']['starttime'] = []
    ddict['tb5']['endtime'] = []
    ddict['tb5']['other_introduction'] = []
    ddict['tb5']['preson_id'] = []

    ddict['tb7'] = {}
    ddict['tb7']['ori_id'] = []
    ddict['tb7']['receipts'] = []
    ddict['tb7']['year'] = []
    ddict['tb7']['ori_province'] = []
    ddict['tb7']['ori_city_or_Company'] = []
    ddict['tb7']['framework_name'] = []
    ddict['tb7']['contract_name'] = []
    ddict['tb7']['contract_date'] = []
    ddict['tb7']['contract_amount'] = []
    ddict['tb7']['invoice_num'] = []
    ddict['tb7']['invoice_code'] = []
    ddict['tb7']['registration_id'] = []
    ddict['tb7']['invoice_date'] = []
    ddict['tb7']['invoice_amount'] = []
    ddict['tb7']['category'] = []
    ddict['tb7']['original_Remark'] = []


    return ddict

if __name__ == '__main__':





    rootPath = os.getcwd().replace('\\','/')
    jsonPath = rootPath + '/pathJson.json'
    FilePath = rootPath + '/File'

    fileAll = file_name_walk(FilePath)
    ddict = dDict()


    for tis in fileAll:
        if tis['files']:
            for num, fileName in enumerate(tis['files']):
                # if num>1:
                #     break
                winPath = tis['root'] + '/' + fileName
                filePath = winPath.replace('\\','/')
                wb = xlrd.open_workbook(filename=filePath)
                wbNames = wb.sheet_names()

                for wbName in wbNames:
                    sheet = wb.sheet_by_name(wbName)
                    startNum = getStartNum(rows=sheet.nrows, cols=sheet.ncols, word=sheet)
                    catRows = sheet.row_values(startNum['xuhaoX'])
                    if '表4' in wbName:
                        for num,ii in enumerate(catRows):
                            if '验证网址' in ii:
                                ddict['tb4']['professional_verification'].append(ii)
                                ddict['tb4']['professional_verification'] = list(set(ddict['tb4']['professional_verification']))
                                catRows[num] = 'jjjj'
                            if '社保' in ii:
                                ddict['tb4']['social_security'].append(ii)
                                ddict['tb4']['social_security'] = list(set(ddict['tb4']['social_security']))
                                catRows[num] = 'jjjj'
                            if '身份证' in ii:
                                ddict['tb4']['preson_id'].append(ii)
                                ddict['tb4']['preson_id'] = list(set(ddict['tb4']['preson_id']))
                                catRows[num] = 'jjjj'
                            if len(ii) <= 1:
                                catRows[num] = 'jjjj'

                        catRows = [x for x in catRows if x != 'jjjj']

                        ddict['tb4']['ori_id'].append(catRows[0])
                        ddict['tb4']['name'].append(catRows[1])
                        ddict['tb4']['work_experience'].append(catRows[2])
                        ddict['tb4']['credentials'].append(catRows[3])
                        ddict['tb4']['professional_title'].append(catRows[4])
                        ddict['tb4']['professional_level'].append(catRows[5])
                        ddict['tb4']['professional_id'].append(catRows[6])
                        ddict['tb4']['professional_organization'].append(catRows[7])
                        ddict['tb4']['attribute'].append(catRows[8])
                        ddict['tb4']['introduction'].append(catRows[9])

                        ddict['tb4']['ori_id'] = list(set(ddict['tb4']['ori_id']))
                        ddict['tb4']['name'] = list(set(ddict['tb4']['name']))
                        ddict['tb4']['work_experience'] = list(set(ddict['tb4']['work_experience']))
                        ddict['tb4']['credentials'] = list(set(ddict['tb4']['credentials']))
                        ddict['tb4']['professional_title'] = list(set(ddict['tb4']['professional_title']))
                        ddict['tb4']['professional_level'] = list(set(ddict['tb4']['professional_level']))
                        ddict['tb4']['professional_id'] = list(set(ddict['tb4']['professional_id']))
                        ddict['tb4']['professional_organization'] = list(set(ddict['tb4']['professional_organization']))
                        ddict['tb4']['attribute'] = list(set(ddict['tb4']['attribute']))
                        ddict['tb4']['introduction'] = list(set(ddict['tb4']['introduction']))

                    if '表5' in wbName:

                        for num,ii in enumerate(catRows):
                            if '终' in ii:
                                ddict['tb5']['endtime'].append(ii)
                                ddict['tb5']['endtime'] = list(set(ddict['tb5']['endtime']))
                                catRows[num] = 'jjjj'
                            if '起' in ii:
                                ddict['tb5']['starttime'].append(ii)
                                ddict['tb5']['starttime'] = list(set(ddict['tb5']['starttime']))
                                catRows[num] = 'jjjj'
                            if '其他说明' in ii:
                                ddict['tb5']['other_introduction'].append(ii)
                                ddict['tb5']['other_introduction'] = list(set(ddict['tb5']['other_introduction']))
                                catRows[num] = 'jjjj'

                            if '身份证' in ii:
                                ddict['tb5']['preson_id'].append(ii)
                                ddict['tb5']['preson_id'] = list(set(ddict['tb5']['preson_id']))
                                catRows[num] = 'jjjj'

                            if len(ii) <= 1 or '等级' in ii:
                                catRows[num] = 'jjjj'
                        catRows = [x for x in catRows if x != 'jjjj']

                        if len(catRows) < 7:
                            continue

                        try:
                            ddict['tb5']['ori_id'].append(catRows[0])
                            ddict['tb5']['name'].append(catRows[1])
                            ddict['tb5']['province'].append(catRows[2])
                            ddict['tb5']['exam_name'].append(catRows[3])
                            ddict['tb5']['professional'].append(catRows[4])
                            ddict['tb5']['exam_region'].append(catRows[5])
                            ddict['tb5']['grade'].append(catRows[6])

                            ddict['tb5']['ori_id'] = list(set(ddict['tb5']['ori_id']))
                            ddict['tb5']['name'] = list(set(ddict['tb5']['name']))
                            ddict['tb5']['province'] = list(set(ddict['tb5']['province']))
                            ddict['tb5']['exam_name'] = list(set(ddict['tb5']['exam_name']))
                            ddict['tb5']['professional'] = list(set(ddict['tb5']['professional']))
                            ddict['tb5']['exam_region'] = list(set(ddict['tb5']['exam_region']))
                            ddict['tb5']['grade'] = list(set(ddict['tb5']['grade']))
                        except:
                            print(filePath)



                        print(catRows)
                        print(len(catRows))
                        print('----------------------')

    # import pprint
    # pprint.pprint(ddict)
    print(ddict)


