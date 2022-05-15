# -*- coding: utf-8 -*-

import platform
import requests
import json
import os
import time,re
import random
import pymysql
from bs4 import BeautifulSoup
from PIL import Image
import pprint
from crawltools import urlIsExist as urlexist
from crawltools import get_timestr as get_timestrbeif

def get_timestr(date,outformat = "%Y-%m-%d",combdata = False):
    date1 = date
    return get_timestrbeif(date=date1,outformat=outformat,combdata=combdata)

def urlIsExist(urllist):
    return urlexist(urllist)

if __name__ == '__main__':
    pass