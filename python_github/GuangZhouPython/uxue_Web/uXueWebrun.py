#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from quiet import app
from generate import Generate
from flask import render_template,flash,redirect,url_for

if __name__ == '__main__':
    gen = Generate()
    t = time.time()
    gen()
    print('生成完成！！！',time.time()-t)
    app.run(host='0.0.0.0',port=6800,debug=True)




