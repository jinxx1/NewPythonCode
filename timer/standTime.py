

import datetime,time,os
from playsound import playsound
from win10toast import ToastNotifier
import tkinter as tk
from tkinter import messagebox

toaster = ToastNotifier()

sitTime = r'D:\PythonCode\timer\sit_over_50.mp3'
standupTime = r'D:\PythonCode\timer\standup_over_5.mp3'

def zw_xiadan():
    # 第1步，实例化object，建立窗口window
    #实例化窗口
    window = tk.Tk()
    #隐藏主窗口
    window.withdraw()
    #这是一个弹出提示框
    messagebox.showinfo(title="坐够50分钟了。站起来",message='坐够50分钟了。站起来')



if __name__ == '__main__':
    # zw_xiadan()
    # print('end')

    # exit()
    # toaster.show_toast("Example two",
    #                    "This notification is in it's own thread!",
    #                    icon_path=None,
    #                    duration=5,
    #                    threaded=True)
    # while toaster.notification_active(): time.sleep(0.1)


    playsound(standupTime)
