
import xlrd
import pprint,time,re
from datetime import date

from mysql_Final import *
from rexTime import strTime2dateTime,regFloat,regIDandCode,excelTime2unixTime,get_location,findstrDifference,regexName
from collections import Counter
from rexTime import find_zh

# from ex_construction import construction_class
# from ex_design import design_class
# from ex_supervisor import supervisor_class

# from mainFinal import inputWord

import pandas as pd
import numpy as np
line = '------------------------------------'

class ExcelMod(object):

    def __init__(self,filepath,inputWord):
        self.filepath = filepath

        print('正在处理文件------', filepath)
        if 'design' in self.filepath:
            # try:
            self.wb = xlrd.open_workbook(filename=filepath)
            self.wbNames = self.wb.sheet_names()
            design_class(self.filepath, self.wb, self.wbNames,inputWord)
            # except Exception:
            #     insert_bugfileinfo(filepath, 'xlrd error')
            #     print('xlrd error，请查看文件路径是否有特殊字符', filepath)
            #     print('此错误若在录入完毕之后发生，则可忽略。')
            #     return None
            self.wb.release_resources()
            del self.wb
            pass
        elif 'construction' in self.filepath:
            # try:
            self.wb = xlrd.open_workbook(filename=filepath)
            self.wbNames = self.wb.sheet_names()
            construction_class(self.filepath, self.wb, self.wbNames,inputWord)
            # except Exception:
            #     insert_bugfileinfo(filepath, 'xlrd error')
            #     print('xlrd error，请查看文件路径是否有特殊字符', filepath)
            #     print('此错误若在录入完毕之后发生，则可忽略。')
            #     return None
            self.wb.release_resources()
            del self.wb
            pass
        elif 'supervisor' in self.filepath:
            try:
                self.wb = xlrd.open_workbook(filename=filepath)
                self.wbNames = self.wb.sheet_names()
                supervisor_class(self.filepath, self.wb, self.wbNames,inputWord)
            except Exception:
                insert_bugfileinfo(filepath, 'xlrd error')
                print('xlrd error，请查看文件路径是否有特殊字符', filepath)
                print('此错误若在录入完毕之后发生，则可忽略。')
                return None
            self.wb.release_resources()
            del self.wb
            pass
        else:
            pass

    def getStartNum(self,rows,cols,word):
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

    def ctypeTime(self,Cellvalue):


        if Cellvalue:
            if isinstance(Cellvalue,float):
                if 19000000 < Cellvalue < 30000000:
                    intNum = int(Cellvalue)
                    yearint = intNum // 10000
                    monthint = (intNum - intNum // 10000 * 10000) // 100
                    dayint = intNum % 100
                    info = '-'.join([str(yearint), str(monthint), str(dayint)])
                else:

                    info = excelTime2unixTime(Cellvalue)
                    aaaa = info
            else:
                info = str(Cellvalue)
        else:
            info = ''


        return info

    def ctypeTime4(self,row,num,i):

        if row[num]:
            if type(row[num]) is float:
                if 19000000 < row[num] < 30000000:
                    intNum = int(row[num])
                    yearint = intNum // 10000
                    monthint = (intNum - intNum // 10000 * 10000) // 100
                    dayint = intNum % 100
                    info = '-'.join([str(yearint), str(monthint), str(dayint)])
                else:
                    timeinfo = xlrd.xldate_as_tuple(self.sheet4.cell_value(i, num), self.wb.datemode)
                    info = date(*timeinfo[:3]).strftime('%Y-%m-%d')

            elif type(row[num]) is str:
                info = str(row[num])
            else:
                info = ''
        else:
            info = ''

        return info

    def ctypeidandcode(self,Cellvalues):
        info = ''
        if Cellvalues:
            if isinstance(Cellvalues,float):
                info = regIDandCode(str(int(Cellvalues)))
            else:
                info = regIDandCode(str(Cellvalues))
        return info

    def clockTiem(self,name,rowNum):
        if rowNum > 100000:
            print('开始{}录入，共有{}条。看似很多，其实基本都是空行'.format(name, rowNum))
        else:
            print('开始{}录入，共有{}条'.format(name,rowNum))

    def ExcelMod_itemStr(self,strinfo):
        a = str(strinfo).strip()[:990]
        if a != '同上':
            return a

    def ExcelMod_timeProcess(self,path,itemValues,key):
        returnWord = ''
        if '湖北方兴通信有限公司' in path and key == 'contract_date':
            try:
                aa = re.findall(r"\((.*?)\)", itemValues[key])[0]
                returnWord = aa
            except:
                pass

        try:
            aa = strTime2dateTime(self.ctypeTime(itemValues[key]))
        except:
            aa = ''

        if aa and int(aa.strftime('%Y')) < 2050:
            returnWord = aa

        if not aa:
            from rexTime import strTime_other
            cc = strTime_other(itemValues[key])

            if cc:
                returnWord = cc
            else:
                from rexTime import strTime_after
                try:
                    returnWord = strTime_after(itemValues[key])
                except:
                    pass


        return returnWord


class supervisor_class(ExcelMod):

    def __init__(self, filepath, wb, wbNames,inputWord):
        self.filepath = filepath
        self.inputWord = inputWord
        self.Name = regexName(filepath)

        for self.i in wbNames:
            sheet = wb.sheet_by_name(self.i)
            if '表3' in self.i or '常驻机构' in self.i:
                self.table_3(sheet)
                pass
            elif '表7' in self.i or '销售业绩' in self.i:
                self.table_7(sheet)
                pass
            elif '表4' in self.i or '资质证书' in self.i:
                self.table_4(sheet)
                pass
            elif '表5' in self.i or '人员资质' in self.i:
                self.table_5(sheet)
                pass
            else:
                continue

    def table_3(self, word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows, cols, word)
        if not startNum:
            print('not startNum')
            insert_bugfileinfo(self.filepath, 'errorNOTxuhao')
            return None

        colnum = self.Table3_col(startNum, word)
        self.clockTiem(self.i, rows - startNum['xuhaoX'])
        itemList = []
        for rowNum in range(startNum['xuhaoX'] + 1, rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = word.cell_value(rowNum, colNum)
                itemValue[key] = CellValue
            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] >= len(itemValue) - 1:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')
                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/', '').strip().replace('— —', '').strip().replace('—',
                                                                                                                    '').strip()
                item = self.tables3xitem(itemValue)
                itemList.append(item)

            else:
                # print('into the else')
                item = self.tables3xitem(itemValue)
                itemList.append(item)

        if itemList:
            # pprint.pprint(itemList[-1])
            pandas_supervisor_tb3(itemList, self.inputWord)
        else:
            return None

        print('{}录入完成'.format(self.i))

    def Table3_col(self, startNum, word):
        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n, cR in enumerate(catRows):
            if '序' in cR:
                itemNum['excel_id'] = n
                continue
            elif '省份' in cR:
                itemNum['province'] = n
                continue
            elif '地市' in cR:
                itemNum['county'] = n
                continue
            elif '地址' in cR:
                itemNum['address'] = n
                continue
            else:
                continue
        return itemNum

    def tables3xitem(self, itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum'] + 1
        item['from_excel_path'] = self.filepath
        item['Name'] = self.Name
        item['sheetName'] = self.i
        for key in itemValues.keys():
            if key == 'address' or key == 'county' or key == 'province':
                a = self.ExcelMod_itemStr(itemValues[key])
                if a:
                    item[key] = a
        return item

    def table_4(self, word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows, cols, word)
        if not startNum:
            print('not startNum')
            insert_bugfileinfo(self.filepath, 'errorNOTxuhao')
            return None

        colnum = self.Table4_Columns(startNum, word)
        self.clockTiem(self.i, rows - startNum['xuhaoX'])

        itemList = []
        for rowNum in range(startNum['xuhaoX'] + 1, rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = word.cell_value(rowNum, colNum)
                itemValue[key] = CellValue
            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] >= len(itemValue) - 1:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')

                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/', '').strip().replace('— —', '').strip().replace('—',
                                                                                                                    '').strip()
                item = self.tables4item(itemValue)
                itemList.append(item)

            else:
                # print('into the else')
                item = self.tables4item(itemValue)
                itemList.append(item)

        if itemList:
            # pprint.pprint(itemList[-1])
            pandas_supervisor_tb4(itemList, self.inputWord)
        else:
            return None
        print('{}录入完成'.format(self.i))

    def Table4_Columns(self, startNum, word):

        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n, cR in enumerate(catRows):
            if '序号' in cR:
                itemNum['excel_id'] = n
                continue
            elif '证书名称' in cR:
                itemNum['certificate_Name'] = n
                continue
            elif '证书编号' in cR:
                itemNum['certificate_Num'] = n
                continue
            elif '核发机构' in cR:
                itemNum['certificate_Institution'] = n
                continue
            elif '认证范围' in cR:
                itemNum['certificate_Range'] = n
                continue
            elif '颁发日期' in cR:
                itemNum['certificate_GetTime'] = n
                continue
            elif '有效期' in cR:
                itemNum['certificate_Indate'] = n
                continue
            else:
                continue

        return itemNum

    def tables4item(self, itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum'] + 1
        item['from_excel_path'] = self.filepath
        item['sheetName'] = self.i
        item['Name'] = self.Name
        for key in itemValues.keys():
            if key == 'certificate_Name' or key == 'certificate_Num' or key == 'certificate_Institution' or key == 'certificate_Range':
                a = self.ExcelMod_itemStr(itemValues[key])
                if a:
                    item[key] = a
                continue

            if key == 'certificate_GetTime' or key == 'certificate_Indate':
                timeWord = self.ExcelMod_timeProcess(self.filepath, itemValues, key)
                if timeWord:
                    item[key] = timeWord
                continue

        return item

    def table_5(self, word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows, cols, word)
        if not startNum:
            print('not startNum')
            insert_bugfileinfo(self.filepath, 'errorNOTxuhao')
            return None

        colnum = self.Table5_Columns(startNum, word)
        self.clockTiem(self.i, rows - startNum['xuhaoX'])

        itemList = []
        for rowNum in range(startNum['xuhaoX'] + 1, rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = word.cell_value(rowNum, colNum)
                itemValue[key] = CellValue
            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] >= len(itemValue) - 4:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')

                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/', '').strip().replace('— —', '').strip().replace('—',
                                                                                                                    '').strip()
                item = self.tables5item(itemValue)
                itemList.append(item)

            else:
                # print('into the else')
                item = self.tables5item(itemValue)
                itemList.append(item)

        if itemList:
            # pprint.pprint(itemList[-1])
            pandas_supervisor_tb5(itemList, self.inputWord)
        else:
            return None
        print('{}录入完成'.format(self.i))

    def Table5_Columns(self, startNum, word):

        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n, cR in enumerate(catRows):
            if '序号' in cR:
                # itemNum['excel_id'] = n
                continue
            elif '注册监理' in cR and '注册号' in cR:
                itemNum['register_Num'] = n
                continue
            elif '姓名' in cR:
                itemNum['personName'] = n
            elif '其他工程类' in cR and '名称' in cR:
                itemNum['Other_register_Name'] = n
                continue
            elif '其他工程类' in cR and '注册号' in cR:
                itemNum['Other_register_Num'] = n
                continue
            elif '安全生产' in cR and '证书编号' in cR:
                itemNum['safe_Num'] = n
                continue
            elif '安全生产' in cR and '类别' in cR:
                itemNum['safe_Cat'] = n
                continue
            elif '学历' in cR:
                itemNum['major'] = n
                continue
            elif '职称等级' in cR:
                itemNum['professional_Level'] = n
                continue
            elif '监理培训证书' in cR and '名称' in cR:
                itemNum['supervisor_Title'] = n
                continue
            elif '监理培训证书' in cR and '证号' in cR:
                itemNum['supervisor_Num'] = n
                continue
            elif '培训证书' in cR and '颁发' in cR:
                itemNum['supervisor_Org'] = n
                continue
            elif '雇员属性' in cR:
                itemNum['attribute'] = n
            elif '从事' in cR and '工作年限' in cR:
                itemNum['worklimit'] = n
            else:
                continue

        return itemNum

    def tables5item(self, itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum'] + 1
        item['from_excel_path'] = self.filepath
        item['sheetName'] = self.i
        item['Name'] = self.Name
        del itemValues['rowNum']
        del itemValues['colNum']
        for key in itemValues.keys():
            if key == 'worklimit':
                b = regFloat(itemValues[key])
                if b:
                    try:
                        floatdate = float(b.replace('..', '.'))
                        item[key] = round(floatdate, 2)
                    except:
                        continue
                continue
            else:
                a = self.ExcelMod_itemStr(itemValues[key])
                if a:
                    item[key] = itemValues[key]

        return item

    def table_7(self, word):

        rows = word.nrows
        cols = word.ncols

        # 以“序号”为查找对象，确定首块开始位置
        startNum = self.getStartNum(rows, cols, word)
        if not startNum:
            print('not startNum')
            insert_bugfileinfo(self.filepath, 'errorNOTxuhao')
            return None

        colnum = self.Table7_Columns(startNum, word)
        self.clockTiem('table-7', rows - startNum['xuhaoX'])
        itemList = []
        for rowNum in range(startNum['xuhaoX'] + 1, rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = word.cell_value(rowNum, colNum)
                itemValue[key] = CellValue

            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] >= len(itemValue) - 4:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')
                newrow = []
                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/', '').strip().replace('— —', '').strip().replace('—',
                                                                                                                    '').strip()
                item = self.tables7item(itemValue)
                itemList.append(item)

            elif not result[''] and not result['/'] and isinstance(itemValue['invoice_amount'], float):
                # print('into the perfect')
                item = self.tables7item(itemValue)
                itemList.append(item)

            elif itemValue['invoice_amount'] and isinstance(itemValue['invoice_amount'], str):
                # print('into the row-11')
                cutMark = findstrDifference(itemValue['invoice_amount'])
                row11 = itemValue['invoice_amount'].split(cutMark)
                if len(row11) > 1:
                    for num, nn in enumerate(row11):
                        itemValue['invoice_amount'] = nn
                        if num != 0:
                            itemValue['contract_amount'] = 0

                        item = self.tables7item(itemValue)
                        itemList.append(item)
                else:
                    itemValue['invoice_amount'] = row11[0]
                    item = self.tables7item(itemValue)
                    itemList.append(item)
            else:
                # print('into the else')
                item = self.tables7item(itemValue)
                itemList.append(item)

        if itemList:
            pandas_supervisor_tb7(itemList, self.inputWord)
        else:
            return None

        print('tables-7录入完成')

    def tables7item(self, itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum'] + 1
        item['from_excel_path'] = self.filepath
        item['sheetName'] = self.i
        item['Name'] = self.Name

        for key in itemValues.keys():
            if key == 'article_sid' or key == 'invoice_sid' or key == 'category' or key == 'contractor' or key == 'protocol' or key == 'contract_name' or key == 'registration_id':
                a = self.ExcelMod_itemStr(itemValues[key])
                if a:
                    item[key] = a
                continue

            if key == 'contract_date' or key == 'invoice_date':
                timeWord = self.ExcelMod_timeProcess(self.filepath, itemValues, key)
                if timeWord:
                    item[key] = timeWord
                continue

            if key == 'contract_amount' or key == 'invoice_amount':
                a = find_zh(str(itemValues[key]))
                b = regFloat(itemValues[key])
                if not a and b:
                    floatdate = float(b.replace('..', '.'))
                    try:
                        item[key] = round(floatdate, 2)
                    except:
                        insert_bugfileinfo(self.filepath,
                                           'invoiceCodeERROR,{}-{}'.format(itemValuesp['rowNum'], itemValues['colNum']))
                        item[key] = ''
                continue

            if key == 'invoice_num' or key == 'invoice_code':
                item[key] = self.ctypeidandcode(itemValues[key])
                continue

            if key == 'Project_province':
                item['location_original_str'] = itemValues[key]

                location = get_location(itemValues[key])

                for lokey in location:
                    a = location[lokey]
                    if a:
                        item[lokey] = a
                continue

        return item

    def Table7_Columns(self, startNum, word):

        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n, cR in enumerate(catRows):
            if '订单序号' in cR:
                itemNum['article_sid'] = n
                continue
            elif '发票序号' in cR:
                itemNum['invoice_sid'] = n
                continue
            elif '省份' in cR:
                itemNum['Project_province'] = n
                continue
            elif '建设单位名称' in cR:
                itemNum['contractor'] = n
                continue
            elif '框架协议' in cR:
                itemNum['protocol'] = n
                continue
            elif '合同名称' in cR:
                itemNum['contract_name'] = n
                continue
            elif '订单签订日期' in cR:
                itemNum['contract_date'] = n
                continue
            elif '发票号' in cR:
                itemNum['invoice_num'] = n
                continue
            elif '发票代码' in cR:
                itemNum['invoice_code'] = n
                continue
            elif '发票开具时间' in cR:
                itemNum['invoice_date'] = n
                continue
            elif '发票金额' in cR:
                itemNum['invoice_amount'] = n
                continue
            elif '纳税人' in cR:
                itemNum['registration_id'] = n
                continue
            elif '涉及专业' in cR:
                itemNum['category'] = n
                continue
            elif '订单金额' in cR:
                itemNum['contract_amount'] = n
                continue
            else:
                continue
        return itemNum

class design_class(ExcelMod):

    def __init__(self, filepath, wb, wbNames,inputWord):
        self.filepath = filepath
        self.inputWord = inputWord
        self.Name = regexName(filepath)

        for self.i in wbNames:
            sheet = wb.sheet_by_name(self.i)
            if '表3' in self.i:
                self.table_3(sheet)
                pass
            elif '表6' in self.i:
                self.table_6(sheet)
                pass
            elif '表4' in self.i:
                self.table_4(sheet)
                pass
            else:
                continue

    def table_3(self, word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows, cols, word)
        if not startNum:
            print('not startNum')
            insert_bugfileinfo(self.filepath, 'errorNOTxuhao')
            return None

        colnum = self.Table3x_Columns(startNum, word)
        self.clockTiem(self.i, rows - startNum['xuhaoX'])
        itemList = []
        for rowNum in range(startNum['xuhaoX'] + 1, rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = word.cell_value(rowNum, colNum)
                itemValue[key] = CellValue
            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] >= len(itemValue) - 1:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')
                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/', '').strip().replace('— —', '').strip().replace('—',
                                                                                                                    '').strip()
                item = self.tables3xitem(itemValue)
                itemList.append(item)

            elif not result[''] and not result['/']:
                # print('into the perfect')
                item = self.tables3xitem(itemValue)
                itemList.append(item)

            else:
                # print('into the else')
                item = self.tables3xitem(itemValue)
                itemList.append(item)

        if itemList:
            # pprint.pprint(itemList[-1])
            pandas_design_tb3(itemList, self.inputWord)
        else:
            return None

        print('{}录入完成'.format(self.i))

    def Table3x_Columns(self, startNum, word):
        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n, cR in enumerate(catRows):
            if '序' in cR:
                itemNum['excel_id'] = n
                continue
            elif '证书名称' in cR:
                itemNum['certificate_Name'] = n
                continue
            elif '证书编号' in cR:
                itemNum['certificate_Num'] = n
                continue
            elif '核发机构' in cR:
                itemNum['certificate_Institution'] = n
                continue
            elif '认证范围' in cR:
                itemNum['certificate_Range'] = n
                continue
            elif '颁发日期' in cR:
                itemNum['certificate_GetTime'] = n
                continue
            elif '有效期' in cR:
                itemNum['certificate_Indate'] = n
                continue
            else:
                continue
        return itemNum

    def tables3xitem(self, itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum'] + 1
        item['from_excel_path'] = self.filepath
        item['sheetName'] = self.i
        item['Name'] = self.Name

        for key in itemValues.keys():
            if key == 'certificate_Name' or key == 'certificate_Institution' or key == 'certificate_Range':
                a = self.ExcelMod_itemStr(itemValues[key])
                if a:
                    item[key] = a
                continue

            if key == 'certificate_Num':
                if isinstance(itemValues[key], float):
                    item[key] = str(int(itemValues[key]))[:990]
                else:
                    item[key] = str(itemValues[key])[:990]
                continue

            if key == 'certificate_GetTime' or key == 'certificate_Indate':
                timeWord = self.ExcelMod_timeProcess(self.filepath, itemValues, key)
                if timeWord:
                    item[key] = timeWord
                continue

        return item

    def table_6(self, word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows, cols, word)
        if not startNum:
            print('not startNum')
            insert_bugfileinfo(self.filepath, 'errorNOTxuhao')
            return None

        colnum = self.Table6x_Columns(startNum, word)
        self.clockTiem(self.i, rows - startNum['xuhaoX'])
        itemList = []
        for rowNum in range(startNum['xuhaoX'] + 1, rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = word.cell_value(rowNum, colNum)
                itemValue[key] = CellValue
            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] >= len(itemValue) - 4:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')

                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/', '').strip().replace('— —', '').strip().replace('—',
                                                                                                                    '').strip()
                item = self.tables6xitem(itemValue)
                itemList.append(item)

            elif not result[''] and not result['/'] and isinstance(itemValue['invoice_amount'], float):
                # print('into the perfect')
                item = self.tables6xitem(itemValue)
                itemList.append(item)

            elif itemValue['invoice_amount'] and isinstance(itemValue['invoice_amount'], str):
                # print('into the row-11')
                cutMark = findstrDifference(itemValue['invoice_amount'])
                row11 = itemValue['invoice_amount'].split(cutMark)

                if len(row11) > 1:
                    for num, nn in enumerate(row11):
                        itemValue['invoice_amount'] = nn
                        if num != 0:
                            itemValue['contract_amount'] = 0

                        item = self.tables6xitem(itemValue)
                        itemList.append(item)


                else:
                    itemValue['invoice_amount'] = row11[0]
                    item = self.tables6xitem(itemValue)
                    itemList.append(item)
            else:
                # print('into the else')
                item = self.tables6xitem(itemValue)
                itemList.append(item)

        if itemList:
            # pprint.pprint(itemList[-1])
            pandas_design_tb6(itemList, self.inputWord)
        else:
            return None
        print('{}录入完成'.format(self.i))

    def Table6x_Columns(self, startNum, word):

        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n, cR in enumerate(catRows):
            if '订单序号' in cR:
                itemNum['article_sid'] = n
                continue
            elif '发票序号' in cR:
                itemNum['invoice_sid'] = n
                continue
            elif '省份' in cR:
                itemNum['Project_province'] = n
                continue
            elif '建设单位' in cR:
                itemNum['contractor'] = n
                continue
            elif '框架协议' in cR:
                itemNum['protocol'] = n
                continue
            elif '合同名称' in cR:
                itemNum['contract_name'] = n
                continue
            elif '订单签订日期' in cR:
                itemNum['contract_date'] = n
                continue
            elif '发票号' in cR:
                itemNum['invoice_num'] = n
                continue
            elif '发票代码' in cR:
                itemNum['invoice_code'] = n
                continue
            elif '发票开具时间' in cR:
                itemNum['invoice_date'] = n
                continue
            elif '发票金额' in cR:
                itemNum['invoice_amount'] = n
                continue
            elif '纳税人' in cR:
                itemNum['registration_id'] = n
                continue
            elif '涉及专业' in cR:
                itemNum['category'] = n
                continue
            elif '订单金额' in cR:
                itemNum['contract_amount'] = n
                continue
            elif '年度' in cR:
                itemNum['years'] = n
            else:
                continue

        return itemNum

    def tables6xitem(self, itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum'] + 1
        item['from_excel_path'] = self.filepath
        item['sheetName'] = self.i
        item['Name'] = self.Name
        for key in itemValues.keys():
            if key == 'article_sid' or key == 'invoice_sid' or key == 'category' or key == 'contractor' or key == 'protocol' or key == 'contract_name' or key == 'registration_id':
                a = self.ExcelMod_itemStr(itemValues[key])
                if a:
                    item[key] = a
            if key == 'years':
                try:
                    item[key] = str(int(itemValues[key]))[:990]
                except:
                    item[key] = ''
                continue

            if key == 'contract_amount' or key == 'invoice_amount':
                # print(vauleRow,type(vauleRow))
                a = find_zh(str(itemValues[key]))
                b = regFloat(itemValues[key])
                if not a and b:

                    try:
                        floatdate = float(b.replace('..', '.'))
                        item[key] = round(floatdate, 2)
                    except:
                        insert_bugfileinfo(self.filepath,
                                           'invoiceCodeERROR,{}-{}'.format(itemValuesp['rowNum'], itemValues['colNum']))
                        item[key] = ''
                continue

            if key == 'invoice_num' or key == 'invoice_code':
                item[key] = self.ctypeidandcode(itemValues[key])
                continue

            if key == 'invoice_date' or key == 'contract_date':
                timeWord = self.ExcelMod_timeProcess(self.filepath, itemValues, key)
                if timeWord:
                    item[key] = timeWord

                continue

            if key == 'Project_province':
                # print(key)
                item['location_original_str'] = itemValues[key]
                location = get_location(itemValues[key])
                # print(location)
                for lokey in location:
                    item[lokey] = location[lokey]
                continue

        return item

    def table_4(self, word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows, cols, word)
        if not startNum:
            print('not startNum')
            insert_bugfileinfo(self.filepath, 'errorNOTxuhao')
            return None

        colnum = self.Table4x_Columns(startNum, word)
        self.clockTiem(self.i, rows - startNum['xuhaoX'])

        itemList = []
        for rowNum in range(startNum['xuhaoX'] + 1, rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = word.cell_value(rowNum, colNum)
                itemValue[key] = CellValue
            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] >= len(itemValue) - 4:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')

                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/', '').strip().replace('— —', '').strip().replace('—',
                                                                                                                    '').strip()
                item = self.tables4xitem(itemValue)
                itemList.append(item)

            else:
                # print('into the else')
                item = self.tables4xitem(itemValue)
                itemList.append(item)

        if itemList:
            # pprint.pprint(itemList[-1])
            pandas_design_tb4(itemList, self.inputWord)
        else:
            return None
        print('{}录入完成'.format(self.i))

    def Table4x_Columns(self, startNum, word):

        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n, cR in enumerate(catRows):
            if '序号' in cR:
                itemNum['excel_id'] = n
                continue
            elif '姓名' in cR:
                itemNum['personName'] = n
                continue
            elif '专业' in cR:
                itemNum['major'] = n
                continue
            elif '工作时间' in cR:
                itemNum['startWorkTime'] = n
                continue
            elif '工作年限' in cR:
                itemNum['worklimit'] = n
                continue
            elif '最高学历' in cR:
                itemNum['education'] = n
                continue
            elif '职称等级' in cR:
                itemNum['professional_Level'] = n
                continue
            elif '职称名' in cR:
                itemNum['professional_Title'] = n
                continue
            elif '职称证书编号' in cR:
                itemNum['professional_Code'] = n
                continue
            elif '签发单位' in cR:
                itemNum['professional_Org'] = n
                continue
            elif '验证网址' in cR:
                itemNum['verification_Website'] = n
                continue
            elif '其他相关证书' in cR:
                itemNum['Other_Certificates'] = n
                continue
            elif '相关证书编号' in cR:
                itemNum['Other_Cer_Code'] = n
                continue
            elif '相关证书评审' in cR:
                itemNum['Other_Cer_Org'] = n
                continue
            elif '雇员属性' in cR:
                itemNum['attribute'] = n
            elif '社保证明' in cR:
                itemNum['insurance_PageNum'] = n
            elif '名称1' in cR:
                itemNum['projectName1'] = n
            elif '规模1' in cR:
                itemNum['investment1'] = n
            elif '获奖情况1' in cR:
                itemNum['prize1'] = n
            elif '名称2' in cR:
                itemNum['projectName2'] = n
            elif '规模2' in cR:
                itemNum['investment2'] = n
            elif '获奖情况2' in cR:
                itemNum['prize2'] = n
            elif '其他情况' in cR:
                itemNum['others'] = n
            elif '备注' in cR:
                itemNum['remarks'] = n

            else:
                continue

        return itemNum

    def tables4xitem(self, itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum'] + 1
        item['from_excel_path'] = self.filepath
        item['sheetName'] = self.i
        item['Name'] = self.Name
        strList = ['personName', 'major', 'education', 'professional_Level', 'professional_Title', 'professional_Code',
                   'professional_Org', 'verification_Website', 'Other_Cer_Code', 'Other_Certificates', 'Other_Cer_Org',
                   'attribute', 'projectName1', 'prize1', 'projectName2', 'prize2', 'others', 'insurance_PageNum']
        for key in itemValues.keys():

            if key in strList:
                item[key] = str(itemValues[key])[:990]
                continue

            if key == 'startWorkTime':
                timeWord = self.ExcelMod_timeProcess(self.filepath, itemValues, key)
                aaaaa = datetime.datetime(3157, 1, 7)
                # print(aaaaa)
                # print('-------------------------------------', item['excel_rownum'])

                if aaaaa == timeWord:
                    print(itemValues)
                    print('-------------------------------------', item['excel_rownum'])

                if timeWord:
                    item[key] = timeWord

                continue
            if key == 'investment1' or key == 'investment2':
                # print(vauleRow,type(vauleRow))
                a = find_zh(str(itemValues[key]))
                b = regFloat(itemValues[key])
                if not a and b:

                    try:
                        floatdate = float(b.replace('..', '.'))
                        item[key] = round(floatdate, 2)
                    except:
                        insert_bugfileinfo(self.filepath,
                                           'invoiceCodeERROR,{}-{}'.format(itemValues['rowNum'], itemValues['colNum']))
                        item[key] = ''
                continue

            if key == 'worklimit':
                b = regFloat(itemValues[key])
                if b:
                    try:
                        floatdate = float(b.replace('..', '.'))
                        item[key] = round(floatdate, 2)
                    except:
                        continue
                continue
        # pprint.pprint(item)

        return item

class construction_class(ExcelMod):

    def __init__(self, filepath, wb, wbNames,inputWord):
        self.inputWord = inputWord
        self.filepath = filepath
        self.Name = regexName(filepath)

        for self.i in wbNames:
            sheet = wb.sheet_by_name(self.i)
            if '表3' in self.i or '常驻机构' in self.i:
                self.table_3(sheet)
                pass
            elif '表6' in self.i or '销售业绩' in self.i:
                self.table_6(sheet)
                pass
            elif '表4' in self.i or '资质证书' in self.i:
                self.table_4(sheet)
                pass
            else:
                continue

    def table_3(self, word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows, cols, word)
        if not startNum:
            print('not startNum')
            insert_bugfileinfo(self.filepath, 'errorNOTxuhao')
            return None

        colnum = self.Table3_col(startNum, word)
        self.clockTiem(self.i, rows - startNum['xuhaoX'])
        itemList = []
        for rowNum in range(startNum['xuhaoX'] + 1, rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = word.cell_value(rowNum, colNum)
                itemValue[key] = CellValue
            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] >= len(itemValue) - 1:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')
                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/', '').strip().replace('— —', '').strip().replace('—',
                                                                                                                    '').strip()
                item = self.tables3xitem(itemValue)
                itemList.append(item)

            else:
                # print('into the else')
                item = self.tables3xitem(itemValue)
                itemList.append(item)

        if itemList:
            # pprint.pprint(itemList[-1])
            pandas_construction_tb3(itemList,self.inputWord)
        else:
            return None

        print('{}录入完成'.format(self.i))

    def Table3_col(self, startNum, word):
        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n, cR in enumerate(catRows):
            if '序' in cR:
                itemNum['excel_id'] = n
                continue
            elif '省份' in cR:
                itemNum['province'] = n
                continue
            elif '区' in cR:
                itemNum['county'] = n
                continue
            elif '地址' in cR:
                itemNum['address'] = n
                continue
            else:
                continue
        return itemNum

    def tables3xitem(self, itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum'] + 1
        item['from_excel_path'] = self.filepath
        item['Name'] = self.Name
        item['sheetName'] = self.i
        for key in itemValues.keys():
            if key == 'address' or key == 'county' or key == 'province':
                a = self.ExcelMod_itemStr(itemValues[key])
                if a:
                    item[key] = a
        return item

    def table_6(self, word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows, cols, word)
        if not startNum:
            print('not startNum')
            insert_bugfileinfo(self.filepath, 'errorNOTxuhao')
            return None

        colnum = self.Table6_Columns(startNum, word)
        self.clockTiem(self.i, rows - startNum['xuhaoX'])
        itemList = []
        for rowNum in range(startNum['xuhaoX'] + 1, rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = word.cell_value(rowNum, colNum)
                itemValue[key] = CellValue
            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] + result['/'] >= len(itemValue) - 4:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')
                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/', '').strip().replace('— —', '').strip().replace('—',
                                                                                                                    '').strip()
                item = self.tables6item(itemValue)
                itemList.append(item)

            elif itemValue['invoice_amount'] and isinstance(itemValue['invoice_amount'], str):
                # print('into the row-11')
                cutMark = findstrDifference(itemValue['invoice_amount'])
                row11 = itemValue['invoice_amount'].split(cutMark)
                if len(row11) > 1:
                    for num, nn in enumerate(row11):
                        itemValue['invoice_amount'] = nn
                        if num != 0:
                            itemValue['contract_amount'] = 0
                        item = self.tables6item(itemValue)
                        itemList.append(item)
                else:
                    itemValue['invoice_amount'] = row11[0]
                    item = self.tables6item(itemValue)
                    itemList.append(item)
            else:
                # print('into the else')
                item = self.tables6item(itemValue)
                itemList.append(item)

        if itemList:
            # pandas_construction_tb6(itemList, self.inputWord)
            pandas_construction_tb6_tmp(itemList, self.inputWord)
            # pandas_TimeInfo(itemList,self.inputWord)

            pass
        else:
            return None
        print('{}录入完成'.format(self.i))

    def Table6_Columns(self, startNum, word):

        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n, cR in enumerate(catRows):
            if '序号' in cR:
                itemNum['id'] = n
                continue
            elif '专业类别' in cR:
                itemNum['category'] = n
                continue
            elif '工程所在地' in cR:
                itemNum['Project_province'] = n
                continue
            elif '建设单位名' in cR:
                itemNum['contractor'] = n
                continue
            elif '建设单位是否' in cR:
                itemNum['Is_it_operator'] = n
                continue
            elif '建设单位地址' in cR:
                itemNum['contractor_address'] = n
                continue
            elif '项目名称' in cR:
                itemNum['Project_name'] = n
                continue
            elif '合同金额' in cR or '订单金额' in cR:
                itemNum['contract_amount'] = n
                continue
            elif '合同签订日' in cR or '合同签订期' in cR:
                itemNum['contract_date'] = n
                continue
            elif '发票号' in cR:
                itemNum['invoice_num'] = n
                continue
            elif '发票代码' in cR:
                itemNum['invoice_code'] = n
                continue
            elif '发票金额' in cR:
                itemNum['invoice_amount'] = n
                continue
            elif '发票开具时间' in cR:
                itemNum['invoice_date'] = n
                continue
            else:
                continue
        return itemNum

    def tables6item(self, itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum'] + 1
        item['from_excel_path'] = self.filepath

        item['Name'] = self.Name
        item['sheetName'] = self.i

        for key in itemValues.keys():
            if key == 'category' or key == 'contractor' or key == 'Project_name' or key == 'contractor_address':
                a = self.ExcelMod_itemStr(itemValues[key])
                if a:
                    item[key] = a
                continue
            if key == 'Is_it_operator':
                a = self.ExcelMod_itemStr(itemValues[key])
                item['Is_it_operator_remark'] = a
                if a:
                    if a == '是' or a == '否':
                        item[key] = a
                    elif a == '-' or a == '同上' or a == ' ':
                        continue
                    else:
                        item[key] = ''
                else:
                    item['Is_it_operator_remark'] = 'notStr'
                continue

            if key == 'contract_amount' or key == 'invoice_amount':
                if key == 'contract_amount' and itemValues[key] == 23:
                    continue

                a = find_zh(str(itemValues[key]))
                b = regFloat(itemValues[key])
                if not a and b:
                    try:
                        floatdate = float(b.replace('..', '.'))
                        item[key] = round(floatdate, 2)
                    except:
                        insert_bugfileinfo(self.filepath,
                                           'invoiceCodeERROR,{}-{}'.format(itemValuesp['rowNum'], itemValues['colNum']))
                        item[key] = ''
                continue

            if key == 'contract_date' or key == 'invoice_date':

                timeWord = self.ExcelMod_timeProcess(self.filepath, itemValues, key)
                if timeWord:
                    item[key] = timeWord

                if key == 'contract_date':
                    item['contract_ReMark'] = '{}'.format(itemValues[key])
                if key == 'invoice_date':
                    item['invoicet_ReMark'] = '{}'.format(itemValues[key])

                continue

            if key == 'invoice_code' or key == 'invoice_num':
                item[key] = self.ctypeidandcode(itemValues[key])
                continue

            if key == 'Project_province':
                # print(key)
                item['location_original_str'] = itemValues[key]
                location = get_location(itemValues[key])
                # print(location)
                for lokey in location:
                    a = location[lokey]
                    if a:
                        item[lokey] = a
                continue

        return item

    def table_4(self, word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows, cols, word)
        if not startNum:
            print('not startNum')
            insert_bugfileinfo(self.filepath, 'errorNOTxuhao')
            return None

        colnum = self.Table4_Columns(startNum, word)
        self.clockTiem(self.i, rows - startNum['xuhaoX'])

        itemList = []
        for rowNum in range(startNum['xuhaoX'] + 1, rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = word.cell_value(rowNum, colNum)
                itemValue[key] = CellValue
            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] >= len(itemValue) - 1:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')

                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/', '').strip().replace('— —', '').strip().replace('—',
                                                                                                                    '').strip()
                item = self.tables4item(itemValue)
                itemList.append(item)

            else:
                # print('into the else')
                item = self.tables4item(itemValue)
                itemList.append(item)

        if itemList:
            # pprint.pprint(itemList[-1])
            pandas_construction_tb4(itemList, self.inputWord)
        else:
            return None
        print('{}录入完成'.format(self.i))

    def Table4_Columns(self, startNum, word):

        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n, cR in enumerate(catRows):
            if '序号' in cR:
                itemNum['excel_id'] = n
                continue
            elif '证书名称' in cR:
                itemNum['certificate_Name'] = n
                continue
            elif '证书编号' in cR:
                itemNum['certificate_Num'] = n
                continue
            elif '核发机构' in cR:
                itemNum['certificate_Institution'] = n
                continue
            elif '认证范围' in cR:
                itemNum['certificate_Range'] = n
                continue
            elif '颁发日期' in cR:
                itemNum['certificate_GetTime'] = n
                continue
            elif '有效期' in cR:
                itemNum['certificate_Indate'] = n
                continue
            else:
                continue

        return itemNum

    def tables4item(self, itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum'] + 1
        item['from_excel_path'] = self.filepath
        item['sheetName'] = self.i
        item['Name'] = self.Name
        for key in itemValues.keys():
            if key == 'certificate_Name' or key == 'certificate_Num' or key == 'certificate_Institution' or key == 'certificate_Range':
                a = self.ExcelMod_itemStr(itemValues[key])
                if a:
                    item[key] = a
                continue

            if key == 'certificate_GetTime' or key == 'certificate_Indate':
                timeWord = self.ExcelMod_timeProcess(self.filepath, itemValues, key)
                if timeWord:
                    item[key] = timeWord
                continue

        return item

if __name__ == "__main__":
    # pass

    filepath = r'C:\PthonCode\python_github\Python_script\File/construction：供应商信息核查申报表（通信工程施工服务）-河北省-河北省通信建设有限公司V0725.xlsx'.replace('\\','/')

    ExcelMod(filepath,inputWord=None)

