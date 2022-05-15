
import xlrd
import pprint,time,re
from datetime import date
from mysql_processing import insert_table,insert_bugfileinfo,pandas_process
from rexTime import strTime2dateTime,regFloat,regIDandCode
from collections import Counter
from rexTime import find_zh

# catName = ['序号', '专业类别', '工程所在地', '建设单位名', '建设单位是否', '建设单位地址', '项目名称', '合同金额', '合同签订日', '发票号', '发票代码', '发票金额',
#            '发票开具时间']

class ExcelMod(object):
    def __init__(self,filepath):
        self.filepath = filepath
        try:
            self.wb = xlrd.open_workbook(filename=filepath)
            self.wbNames = self.wb.sheet_names()

        except Exception:
            return None


        print('正在处理文件------',filepath)
        for i in self.wbNames:
            if '表3' in i:
                self.sheet3 = self.wb.sheet_by_name(i)
                self.table3(self.sheet3)
            elif '表4' in i:
                self.sheet4 = self.wb.sheet_by_name(i)
                self.table4(self.sheet4)
            elif '表6' in i:
                self.sheet6 = self.wb.sheet_by_name(i)
                self.table6(self.sheet6)
            else:
                continue

        self.wb.release_resources()
        del self.wb


    def table3(self,word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows,cols,word)
        if not startNum:
            insert_bugfileinfo(self.filepath,'errorNOTxuhao')
            return None
        self.clockTiem('table-3',rows-startNum['xuhaoX'])
        for i in range(startNum['xuhaoX']+1,rows):
            row = word.row_values(i)
            result = Counter(row)
            if result[''] >= cols - 1:
                continue
            item = self.tryInserdate(row, i, 'null', self.filepath, 3)

        print('tables-3录入完成')

    def table4(self,word):
        rows = word.nrows
        cols = word.ncols
        startNum = self.getStartNum(rows,cols,word)
        if not startNum:
            insert_bugfileinfo(self.filepath,'errorNOTxuhao')
            return None
        self.clockTiem('table-4', rows-startNum['xuhaoX'])
        for i in range(startNum['xuhaoX']+1,rows):
            row = word.row_values(i)
            result = Counter(row)
            if result[''] >= cols - 1:
                continue
            self.tryInserdate(row,i,'null',self.filepath,4)
        print('tables-4录入完成')

    def table6(self,word):

        rows = word.nrows
        cols = word.ncols
        if cols < 13:
            return None
        # 以“序号”为查找对象，确定首块开始位置
        startNum = self.getStartNum(rows,cols,word)
        if not startNum:
            insert_bugfileinfo(self.filepath,'errorNOTxuhao')
            return None

        colnum = self.Table6_Columns(startNum,word)
        self.clockTiem('table-6', rows-startNum['xuhaoX'])
        itemList=[]
        for rowNum in range(startNum['xuhaoX'] + 1,rows):
            itemValue = {}
            itemValue['rowNum'] = rowNum
            for key in colnum.keys():
                colNum = colnum[key]
                itemValue['colNum'] = colNum
                CellValue = self.sheet6.cell_value(rowNum,colNum)
                itemValue[key] = CellValue

            valueList = Counter(itemValue).values()
            result = Counter(valueList)

            if result[''] >= len(itemValue)-4 or len(str(itemValue['id']))>10:
                # print('into the continue')
                continue

            elif result['/'] > 0 or result['— —'] > 0 or result['—'] > 0:
                # print('into the newrow')
                newrow = []
                for key in itemValue.keys():
                    if type(itemValue[key]) is str:
                        itemValue[key] = itemValue[key].replace('/','').strip().replace('— —','').strip().replace('—','').strip()
                item = self.tables6item(itemValue)
                itemList.append(item)

            elif not result[''] and not result['/'] and isinstance(itemValue['invoice_amount'],float):
                # print('into the perfect')
                item = self.tables6item(itemValue)
                itemList.append(item)

            elif isinstance(itemValue['invoice_amount'],str):
                # print('into the row-11')
                row11 = itemValue['invoice_amount'].split('\n')
                if len(row11)>1:
                    for nn in row11:
                        itemValue['invoice_amount'] = nn
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
            try:
                pandas_process((itemList))
            except:
                insert_bugfileinfo(self.filepath,'table6_intomysql_ERROR')
                print('table6-intoMysql_ERROR')
        else:
            return None

        print('tables-6录入完成')

    def tryInserdate(self,row,i,division,filepath,tableNum):
        import json
        erroritem = json.dumps({'tables':tableNum,'rowNum':i+1,'division':division})

        if tableNum==3:
            try:
                item = self.tables3item(row, i)
                insert_table(item=item, num=3)
                return 'Get_Table3_row={}'.format(i+1)
            except:
                insert_bugfileinfo(filepath, erroritem)
                rWORD = 'Table3_row={}_unknow ERROR'.format(i + 1)
                print(rWORD)
                return rWORD

        if tableNum ==4:
            try:
                item = self.tables4item(row, i)
                insert_table(item=item, num=4)
                return 'Get_Table4_row={}'.format(i+1)
            except:
                insert_bugfileinfo(filepath, erroritem)
                rWORD = 'Table4_row={}_unknow ERROR'.format(i + 1)
                print(rWORD)
                return rWORD

    def Table6_Columns(self,startNum,word):

        catRows = word.row_values(startNum['xuhaoX'])
        itemNum = {}
        for n,cR in enumerate(catRows):
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
            elif '合同金额' in cR:
                itemNum['contract_amount'] = n
                continue
            elif '合同签订日' in cR:
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
        return itemNum

    def getStartNum(self,rows,cols,word):
        cellinfo = {}
        for xx in range(rows):
            for yy in range(cols):
                cell_value = word.cell_value(xx,yy)
                if '序号' in str(cell_value):
                    cellinfo['xuhaoX'] = xx
                    cellinfo['xuhaoY'] = yy
                    break
            if cellinfo:
                break
        return cellinfo

    def tables6item(self,itemValues):
        item = {}
        item['excel_rownum'] = itemValues['rowNum']+1
        item['from_excel_path'] = self.filepath
        item['excel_id'] = itemValues['id']
        rege = re.findall("-(.*?)\.xl", self.filepath)
        if rege:
            item['Name'] = rege[0]

        for key in itemValues.keys():
            if key == 'excel_id':
                item[key] = str(itemValues[key])[:990]
                continue

            if key == 'category':
                item[key] = str(itemValues[key])[:990]
                continue

            if key == 'Project_province':
                location = str(itemValues[key]).split('省')
                if len(location) > 1:
                    item[key] = location[0] + '省'
                    item['Project_district'] = location[1]
                else:
                    location_s = str(itemValues[key]).split('市')
                    if len(location_s) > 1:
                        item[key] = location_s[0] + '市'
                        item['Project_district'] = location_s[1]
                    else:
                        item[key] = location_s[0]
                continue

            if key == 'contractor':
                item[key] = str(itemValues[key])[:990]
                continue

            if key == 'Is_it_operator':
                item['Is_it_operator'] = str(itemValues[key])[:990]
                continue

            if key == 'contractor_address':
                item['contractor_address'] = str(itemValues[key])[:990]
                continue

            if key == 'Project_name':
                item['Project_name'] = str(itemValues[key])[:990]
                continue

            if key == 'contract_amount':
                # print(vauleRow,type(vauleRow))
                a = find_zh(str(itemValues[key]))
                b = regFloat(itemValues[key])
                if not a and b:
                    try:
                        floatdate = float(b.replace('..', '.'))
                        item[key] = round(floatdate,2)
                    except:
                        insert_bugfileinfo(self.filepath,'contract_amount_ERROR_row[{}]_col[{}]'.format(itemValues['rowNum'],itemValues['colNum']))
                        item[key] = ''
                continue

            if key == 'contract_date':
                # print(vauleRow,type(vauleRow),i)
                try:
                    aa = strTime2dateTime(self.ctypeTime(itemValues[key]))
                except:
                    aa = ''
                if aa:
                    item[key] = aa
                continue

            if key == 'invoice_num':
                # print(itemValues[key])
                # print(itemValues['rowNum'],itemValues['colNum'])
                item[key] = self.ctypeidandcode(itemValues[key])
                continue

            if key == 'invoice_code':
                # print((10 + divNum,i))
                item['invoice_code'] = self.ctypeidandcode(itemValues[key])
                continue

            if key == 'invoice_amount':
                # print(vauleRow,type(vauleRow))
                a = find_zh(str(itemValues[key]))
                b = regFloat(itemValues[key])
                if not a and b:
                    try:
                        floatdate = float(b.replace('..', '.'))
                        item[key] = round(floatdate,2)
                    except:
                        insert_bugfileinfo(self.filepath,'invoice_amount_ERROR_row[{}]_col[{}]'.format(itemValues['rowNum'],itemValues['colNum']))
                        item[key] = ''
                continue

            if key == 'invoice_date':
                try:
                    aa = strTime2dateTime(self.ctypeTime(itemValues[key]))
                except:
                    aa = ''
                if aa:
                    item[key] = aa
                continue

        # pprint.pprint(item)
        return item

    def tables4item(self, row, i):

        result = Counter(row)

        item = {}
        rege = re.findall("-(.*?)\.xl", self.filepath)
        if rege:
            item['Name'] = rege[0]
        if row[0]:
            item['excel_id'] = str(row[0])
        if row[1]:
            item['certificate_Name'] = str(row[1])
        if row[2]:
            item['certificate_Num'] = str(row[2])
        if row[3]:
            item['certificate_Institution'] = str(row[3])
        if row[4]:
            item['certificate_Range'] = str(row[4])
        if row[5]:
            # print(row[5],type(row[5]))
            try:
                aa = strTime2dateTime(self.ctypeTime4(row, 5, i))
            except:
                aa = ''
            if aa:
                item['certificate_GetTime'] = aa
        if row[6]:
            # print(row[6],type(row[6]),i)
            try:
                aa = strTime2dateTime(self.ctypeTime4(row, 6, i))
            except:
                aa = ''
            if aa:
                item['certificate_Indate'] = aa
        if not result['']:
            item['perfectItem'] = 1

        item['from_excel_path'] = self.filepath
        return item

    def tables3item(self, row, i):
        result = Counter(row)

        item = {}
        rege = re.findall("-(.*?)\.xl", self.filepath)
        if rege:
            item['Name'] = rege[0]
        if row[0]:
            item['excel_id'] = str(row[0])
        if row[1]:
            item['province'] = str(row[1])
        if row[2]:
            item['county'] = str(row[2])
        if row[3]:
            item['address'] = str(row[3])
        if not result['']:
            item['perfectItem'] = 1
        item['from_excel_path'] = self.filepath
        return item

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
                    timeinfo = xlrd.xldate_as_tuple(Cellvalue, self.wb.datemode)
                    # print(timeinfo)
                    # print(Cellvalue)
                    # print('--------------')
                    info = date(*timeinfo[:3]).strftime('%Y-%m-%d')
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
            if isinstance(Cellvalues,float) or isinstance(Cellvalues,int) or isinstance(Cellvalues,str):
                info = regIDandCode(str(Cellvalues))
        return info

    def clockTiem(self,name,rowNum):
        if rowNum > 100000:
            print('开始{}录入，共有{}条。看似很多，其实基本都是空行'.format(name, rowNum))
        else:
            print('开始{}录入，共有{}条'.format(name,rowNum))







if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    filepath = r'C:/PthonCode/Python_script/File/4.河南/附件3：供应商信息核查申报表（通信工程施工服务）-河南江河通信工程有限公司.xlsx'.replace('\\','/')



    ExcelMod(filepath)









