#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import send_from_directory
from flask import render_template,flash,redirect,url_for,make_response
from flask_cors import *
from . import app


CORS(app,supports_credentials=True,resources=r'/*')

@app.route('/',methods=["GET"])
@app.route('/index',methods=["GET"])
@app.route('/index.html',methods=["GET"])
def index():
    sendfrom = send_from_directory('static', 'generated/page/index.html')
    res = make_response(sendfrom)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/tags',methods=["GET"])
def tag():
    sendfrom = send_from_directory('static', 'generated/page/tags.html')
    res = make_response(sendfrom)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/tag/<tag>',methods=["GET"])
def tag_post(tag):

    sendfrom = send_from_directory('static', 'generated/page/tag/{tag}.html'.format(tag=tag))
    res = make_response(sendfrom)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/categories',methods=["GET"])
def category():
    sendfrom = send_from_directory('static', 'generated/page/categories.html')
    res = make_response(sendfrom)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/category/<category>',methods=["GET"])
def category_post(category):
    sendfrom = send_from_directory('static', 'generated/page/category/{category}.html'.format(category=category))
    res = make_response(sendfrom)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/page/<page>',methods=["GET"])
def page(page):
    sendfrom = send_from_directory('static', 'generated/page/{page}.html'.format(page=page))
    res = make_response(sendfrom)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/post/<year>/<month>/<post>',methods=["GET"])
def post(year, month, post):
    sendfrom = send_from_directory('static',
                'generated/post/{year}/{month}/{post}.html'.format(year=year, month=month, post=post))
    res = make_response(sendfrom)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

