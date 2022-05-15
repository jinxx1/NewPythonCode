from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import login_required, login_user, logout_user, UserMixin
from db import *
import os,shutil,random,pprint,re
from . import app, gen, lm
from utils import ImportData
from config import *


admin = Blueprint('admin', __name__)

user = {'username': ADMIN_USERNAME, 'password': ADMIN_PASSWORD}


class User(UserMixin):
    """
    flask-login 的 UserMixin 类，实现了
    is_authenticated，is_active，is_anonymous 等方法，直接继承
    """
    pass


def query_user(username):
    """
    通过用户名，获取用户记录，如果不存在，则返回None
    """
    if user['username'] == username:
        return user


@lm.user_loader
def load_user(username):
    """
    从会话中加载用户信息
    """
    if query_user(username) is not None:
        curr_user = User
        curr_user.id = username
        return curr_user
    return None


@admin.route('/')
@login_required
def index():

    return render_template('admin.html', title="管理后台")


@admin.route('/login', methods=['GET', 'POST'])
def login():
    """管理员登录"""
    if request.method == 'POST':
        username = request.form.get('username')
        user = query_user(username)
        if user is not None and request.form['password'] == user['password']:
            curr_user = User()
            curr_user.id = username

            login_user(curr_user)

            next = request.args.get('next')
            return redirect(next or url_for('admin.index'))
        flash('用户名或者密码错误！')
    return render_template('login.html', title="管理员登录")


@admin.route('/logout')
@login_required
def logout():
    """管理员登出"""
    logout_user()
    return redirect(url_for('index'))


@admin.route('/upload/post', methods=['GET', 'POST'])
@login_required
def upload_post():
    """
    支持用户上传 md 文件并生成 html
    :return:
    """
    source_folder = app.config['POST_PATH']
    if request.method == 'POST':
        file = request.files['file']
        # print(request.files)
        filename = file.filename
        path = os.path.join(source_folder, filename)
        file.save(path)
        # 生成 html
        gen()
        # 重置 shelve 数据
        ImportData.reload_data()

        return redirect(url_for('index'))
    return render_template('upload_post.html', title="上传文章")


@admin.route('/upload/page', methods=['GET', 'POST'])
@login_required
def upload_page():
    """
    支持用户上传 md 文件并生成 html
    :return:
    """
    source_folder = app.config['PAGE_PATH']
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        path = os.path.join(source_folder, filename)
        file.save(path)

        # 生成 html
        gen()
        # 重置 shelve 数据
        ImportData.reload_data()

        return redirect(url_for('index'))
    return render_template('upload_page.html', title="上传页面")

@admin.route('/upload/postAll', methods=['GET', 'POST'])
@login_required
def upload_postAll():
    """
    脚本生成的md，自动上传。手工发布全部
    :return:
    """
    source_folder = app.config['POST_PATH']
    Bak_Folder= app.config['POST_BAK_PATH']
    if request.method == 'POST':
        for root, dirs, files in os.walk(Bak_Folder):
            for name in files:
                if os.path.splitext(name)[1].lower() == '.md':
                    md = os.path.join(root, name)
                    # Bak_Md_File_Path = shutil.move(md, source_folder)
                    shutil.move(md, source_folder)

        # 生成 html
        gen()
        # 重置 shelve 数据
        ImportData.reload_data()

        return redirect(url_for('index'))
    return render_template('upload_postAll.html', title="发布所有缓存内容")



@admin.route('/upload/top5', methods=['GET', 'POST'])
@login_required
def upload_top5():
    """
    用户上传 top5信息
    :return:
    """
    source_folder = app.config['INSERT_PIC']
    if request.method == 'POST':
        imgAll = ['gif','GIF','jpg','JPG','JPEG','jpeg','png','PNG']
        imgfile = request.files['upimg']
        siteLocal = request.form.get('articlocal')
        articleLink = request.form.get('uplink')
        recode = re.findall(r"\d{14}_\d{12}", articleLink)
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

        try:
            artcleNum = recode[0]
        except:
            return render_template('upTOP5_ERROR.html',ERRORWORD = '文章链接格式有误，并非本站发布的文章')

        titleTemp = get_list(db, artcleNum)
        try:
            TitleT = titleTemp[0]['TitleT']
        except:
            return render_template('upTOP5_ERROR.html', ERRORWORD='本站没有这篇文章。')

        if imgfile.filename.split('.')[1] not in imgAll:
            return render_template('upTOP5_ERROR.html', ERRORWORD = '上传格式有误，请使用jpg、gif、png三种图片格式')
        word = imgfile.filename.split('.')[0].encode('utf-8').decode('utf-8')
        matchword = zh_pattern.search(word)
        if matchword:
            return render_template('upTOP5_ERROR.html', ERRORWORD='图片名称请不要使用中文字符')
        filename = artcleNum + '_' + siteLocal + '_' + str(random.randint(1000000000,9999999999))+ '_' + imgfile.filename
        path = os.path.join(source_folder, filename)
        imgfile.save(path)

        DictInput = {
            'siteLocal':siteLocal,
            'articleNum':artcleNum,
            'PicLocal':path,
            'articleLink':articleLink,
            'summy':request.form.get('summy'),
            'titleT':TitleT
        }
        into_TOP5_MYSQL(DictInput)
        gen()
        ImportData.reload_data()
        return render_template('upTOP5_ERROR.html', ERRORWORD='已经上传成功。请稍后刷新首页。')


    return render_template('upload_top5.html', title="上传top5文章")