import subprocess
import os
import io
import whatimage

import traceback
from PIL import Image
import win32api,win32gui,win32con,win32ui

import psutil


def decodeImage(bytesIo):
    try:
        fmt = whatimage.identify_image(bytesIo)
        # print('fmt = ', fmt)
        if fmt in ['heic']:
            i = pyheif.read_heif(bytesIo)
            # print('i = ', i)
            # print('i.metadata = ', i.metadata)
            pi = Image.frombytes(mode=i.mode, size=i.size, data=i.data)
            # print('pi = ', pi)
            pi.save('heeh.jpg', format="jpeg")
    except:
        traceback.print_exc()


def read_image_file_rb(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    return file_data

def heic_to_jpg(imgpath):
    data = read_image_file_rb(imgpath)
    decodeImage(data)

if __name__ == "__main__":


    file_path = 'D:/w\[备份]祖娅娟iPhoneX\其他/IMG_0003.HEIC'
    print('file_path = ', file_path)
    win32api.ShellExecute(1,'open',file_path,'','',1)
    paraid = win32gui.FindWindow('ApplicationFrameWindow','Photos')

    print('father frame:',paraid)
    import time
    time.sleep(2)

    win32gui.PostMessage(paraid,win32con.WM_KEYDOWN,17,0)
    win32gui.PostMessage(paraid,win32con.WM_KEYDOWN,69,0)
win32con.
    exit()

    hwndChildList = []
    win32gui.EnumChildWindows(paraid, lambda hwnd, param: param.append(hwnd), hwndChildList)
    try:
        for i in hwndChildList:
            cc = win32gui.FindWindowEx(paraid,i,None,None)
            # print(win32gui)
            print('id:',cc)
            if cc > 0:
                print('frame type:',win32gui.GetClassName(cc))
                print(win32gui.MenuBar(cc))
                # left, top, right, bottom = win32gui.GetWindowRect(cc)
                # print(left, top, right)
                # print(bottom)
    except Exception as ff:
        print('ERROR------',ff)
    finally:
        win32gui.PostMessage(paraid,win32con.WM_CLOSE,0,0)



        print('-----------')
    win32gui.PostMessage(paraid, win32con.WM_CLOSE, 0, 0)





    # w2hd = win32gui.FindWindowEx(paraid,None,None,None)
    # print(w2hd)
    # w3hd = win32gui.FindWindowEx(w2hd,None,None,'Edit&Create')
    # w3hd = win32gui.FindWindowEx(w2hd,None,None,'Search')

    # print(w3hd)


    # win32api.keybd_event(17,0,0,0)
    # win32api.keybd_event(69,0,0,0)
    # win32api.keybd_event(69,0,win32con.KEYEVENTF_KEYUP,0)
    # win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)




    exit()
    para = win32gui.FindWindow(None,"Photos")
    print(para)
    print(win32gui.GetClassName(para))


    exit()
    data = read_image_file_rb(file_path)
    # print('data = ', data)
    decodeImage(data)