import os,time,pprint,pymysql,sys
import ctypes
import os
import platform
import binascii
from PIL import Image
from os.path import join, getsize
import io

from home_setting import *
import psutil
import wmi
C = wmi.WMI()

def printMacAddress():
    # macs = []
    for n in  C.Win32_NetworkAdapter():
        mactmp = n.MACAddress
        if mactmp and len(mactmp.strip()) > 5:
            pass
            # tmpmsg = {}
            # tmpmsg['MACAddress'] = n.MACAddress
            if "18:31:BF:2E:52:6C" in n.MACAddress:
                return "x299"
            # tmpmsg['Name'] = n.Name
            # tmpmsg['DeviceID'] = n.DeviceID
            # tmpmsg['AdapterType'] = n.AdapterType
            # tmpmsg['Speed'] = n.Speed
            # macs.append(tmpmsg)
    # return macs
if __name__ == '__main__':

    computer_type = printMacAddress()

