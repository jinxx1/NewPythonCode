from flask import Flask,url_for
from flask_login import LoginManager
from flask import render_template,flash,redirect,url_for
from generate import Generate


app = Flask(__name__, template_folder='templates',static_folder='static',static_url_path='/static')
app.config.from_object('config')

lm = LoginManager(app)
lm.login_view = 'admin.login'
lm.login_message = '请登录管理员权限'

gen = Generate()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

def render_top5update(date):
    return render_template('TOP5.html')



from . import main, api, admin
from .api import api
from .admin import admin

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/admin')
