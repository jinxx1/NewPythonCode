
import pandas as pd
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
import json,xlrd


import tkinter as tk
import _tkinter
def outPD(xlsxfilepath):
    sheet = pd.read_excel(io=xlsxfilepath, sheet_name=1)
    sheet['序号'].fillna(method='pad', inplace=True)
    sheet['二级模块'].fillna(method='pad', inplace=True)
    sheet['一级模块'].fillna(method='pad', inplace=True)
    sheet.rename(columns={'序号':'l0','一级模块':'l1','二级模块':'l2','三级模块':'l3','功能描述':'mark',},inplace=True)
    return json.loads(sheet.to_json(orient='records'))


on_hit = False
def hit_save():

    global on_hit
    if not on_hit:
        on_hit = True
        var.set('you hit me')
    else:
        var.set('')




def selection():
    if var.get() != 'no':
        outfile.append(ppath)


def motion(event):
    print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjj')

if __name__ == '__main__':
    import os
    root = os.getcwd()

    jsonPath = os.path.join(root, 'info.json')
    filePath = os.path.join(root, '111111.xlsx')
    print(jsonPath)
    exit()


    sheet = outPD()
    import pprint
    pprint.pprint(json.loads(sheet))


    # level_0_unique = sheet['序号'].unique()
    # level_1 = sheet.loc[sheet['序号'] == '公共事业管理']['一级模块'].unique()
    # level_2 = sheet['二级模块'].unique()
    # print(level_0_unique)
    # sheet2 = sheet.loc[sheet['序号'] == '公共事业管理']
    # print(sheet2.loc[sheet2['一级模块'] == '综合管控平台'])

    # print(level_1)
    # 综合管控平台.




    #
    #
    # window = tk.Tk()
    #
    #
    # window.title('王云琦小妹妹')
    # window.geometry('1024x1024')
    #
    # lb = tk.Listbox(window,
    #                 selectmode="EXTENDED",
    #                 width=200,height=20,
    #                 borderwidth = 4,
    #                 yscrollcommand = 5000)
    #
    # for l0 in level_0_unique:
        # lable_0 = tk.Label(window,text=l0)
        # lable_0.pack()
        # lb.insert(0,l0)
        # lb.pack()


        # level_1_sheet = sheet.loc[sheet['序号'] == l0]
        # #
        # level_1_unique = level_1_sheet['一级模块'].unique()
        # for l1 in level_1_unique:
            # lb.insert(1,l1)
            # lb.pack()
            # lable_1 = tk.Label(window, text=l1)
            # lable_1.pack()



            # level_2_sheet = level_1_sheet.loc[level_1_sheet['一级模块'] == l1]
            # level_2_unique = level_2_sheet['二级模块'].unique()
            #
            # for l2 in level_2_unique:
            #     # lable_2 = tk.Label(window, text=l2)
            #     # lable_2.pack()
            #
            #     level_3_sheet = level_2_sheet.loc[level_2_sheet['二级模块'] == l2]
            #     level_3_unique = level_3_sheet['三级模块'].unique()
            #
            #     for l3 in level_3_unique:
            #         if isinstance(l3,float):
            #             l3 = l2
            #
            #
            #         var = tk.StringVar()
            #
            #         # msg = tk.Message()
            #
            #         wordd = l0 + '-' + l1 + '-' + l2 + '-' + l3
            #
            #         ppath = '选中' + l3
            #
            #         lb.insert(0,wordd)
            #         lb.pack()


                    # cc = tk.Checkbutton(window,text = wordd,
                    #
                    #                     variable = var,onvalue = ppath,
                    #                     offvalue = 'no',
                    #                     command = selection)
                    #
                    # cc.pack()
                    # msga = tk.Message(cc,text = 'ttteeexxxttt')


    #
    #
    # window.mainloop()
    #
    # print(outfile)

    # munubar = tk.Menu(top)
    # filemenu = tk.Menu(munubar,tearoff=0)
    # munubar.add_cascade(label='File',)






    # var = tk.StringVar()
    # l = tk.Label(top,textvariable=var,bg='green')
    # l.pack()
    # b = tk.Button(top,text='hit me',command = hit_save)
    # b.pack()
    #
    # listb = tk.Listbox(top)
    #
    # for item in level_0_unique:
    #     listb.insert(0,item)
    #
    # listb.pack()

    # window.mainloop()