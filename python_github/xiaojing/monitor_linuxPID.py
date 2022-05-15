# -*- coding:utf-8 -*-
import subprocess
import sys,os
import shutil
import psutil
import datetime
import time
log_file = 'monitor_log.txt'




if __name__ == '__main__':

    pids = psutil.pids()
    print(pids)