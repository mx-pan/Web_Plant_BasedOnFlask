#-*- coding:utf-8 -*-
from __future__ import print_function
import time
import os
import platform
import traceback
import sqlite3
import re
import sys
import datetime
import tablib
from flask import Flask, safe_join, send_file, make_response, jsonify, escape, request, redirect, url_for  # ,session
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from flask_socketio import SocketIO, emit

from .flask_sqlite_view import *        # 导入数据库视图的显示
from .flask_sqlite import *             # 导入数据库定义
from .image_generate import *           # 导入图像生成函数



""" 为支持 Python2 而使用的代码 
# if(platform.python_version().startswith('2.')):
#   reload(sys)
#   sys.setdefaultencoding('utf-8')
"""



def make_json(state, log, msg, data=''):
    """发送通用反馈给UI前端\n
    `state` 是这次请求是否成功？ 接受 `True` 或 `False`.\n
    `log` 显示在浏览器 `Console` 里的调试信息\n
    `msg` 显示给用户的一个提示信息，如果为空则不弹出.\n
    `data` 是请求的结果；如果发生错误，则为错误信息，可为空.\n
    `examples:`\n
        make_json(True, 'action successful', '某操作成功')
        make_json(False, 'action fail', '某操作失败' ,'详细原因') """
    if(state):
        state_str = 'SUCC'
    else:
        state_str = 'FAIL'
    return jsonify({'state': state_str, 'data': data, 'msg': msg, 'log': log})


def base64_convert(data):
    """ 获取任意数据的base64编码 """
    return base64.encodestring(data)


# 初始化Flask app
app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 国际化设置，将语言设置为中文
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

#初始化socketio by SP
socketio = SocketIO(app)

# 初始化数据库
db.init_app(app)

# 初始化 Login Manager
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.init_app(app)


# 用户登录时调用的回调函数，返回一个USERS类的实例
# 注意，必须使用db.session.query(USERS)进行查找，不能使用 USERS.query
@login_manager.user_loader
def load_user(username):
    return db.session.query(USERS).filter_by(id=username).first()


# 用户未登录时的处理
@login_manager.unauthorized_handler
def unauthorized():
    return make_json(False, 'Action unauthorized', '需要登录', 'LOGIN')


# 初始化 Flask_admin 的视图显示功能
class my_view(AdminIndexView):
    @expose('/')
    def index(self):
        arg1 = 'Hello'
        return self.render('index.html')

    def is_accessible(self):
        """ 只有已经登录而且用户权限为管理员的用户才能查看或编辑数据库 """
        return current_user.is_authenticated


# 初始化 Flask_admin
admin = Admin(app, index_view=my_view(), name='管理后台',
              template_mode='bootstrap3')


# 将显示功能添加到页面中
admin.add_view(USERS_view(USERS, db.session, name='用户管理', endpoint='USER'))
admin.add_view(PLANTS_view(PLANTS, db.session, name='植物信息管理',
                           endpoint='PLANTS'))


@app.errorhandler(404)
def page_not_found(error):
    """重定义404页面"""
    return make_json(False, '404 by error handler', '页面没有找到', {"dir": os.getcwd()})


@app.route('/', methods=['GET'])
def root_redirect():
    """如果用户访问了根页面，则重定向用户到首页"""
    return redirect("/file/index.html")


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    """如果用户请求了网页图标，则给用户发送图标"""
    return any_file('Images/Favicon/favicon.ico')


@app.route('/file/<path:filename>', methods=['GET'])
def any_file(filename):
    """将用户想要的任意文件发送给用户"""
    # 获取需要发送文件的详细地址
    full_path = safe_join(os.getcwd() + '/www/', filename)
    try:
        # 将文件发送给用户
        return send_file(full_path, attachment_filename=full_path, conditional=True)
    except:
        # 出现错误，反馈错误的详细信息
        cause = {"full_path": full_path, "traceback": traceback.format_exc()}
        return make_json(False, "404 by file router", '页面未找到', cause)


@app.route('/api/login/<username>/<password>', methods=['GET'])
def api_login(username, password):
    """ 处理用户登陆 """
    # 清除请求中除了 a-zA-Z0-9_- 之外所有字符
    username = re.sub('[^a-zA-Z0-9]', '', username)
    try:
        # 查询指定的用户
        user = USERS.query.filter_by(USERNAME=username).first()
        # 如果查找到了这个用户
        if(user != None):
            # 且密码正确
            if(user.PASSWORD == password):
                # 登录这个用户
                login_user(user, True)
                return make_json(True, 'Login Success ', '登录成功，欢迎您')
            else:
                return make_json(False, 'Username or password error', '用户名或密码错误')
        else:
            return make_json(False, 'Username not exist', '用户名不存在')
    except:
        return make_json(False, 'Server internal error [api_login()]', '服务器内部错误 ', traceback.format_exc())


@app.route('/api/logout', methods=['GET'])
@login_required
def api_logout():
    logout_user()
    return make_json(True, 'Logout Sucessful', '登出成功')


@app.route('/api/check', methods=['GET'])
@login_required
def api_check():
    return make_json(True, 'Already logged in', "您已登录")


@app.route('/api/user', methods=['GET'])
@login_required
def api_user():
    user = USERS.query.filter_by(USERNAME=current_user.USERNAME).first()
    data = {
        'USERNAME': user.USERNAME,
        'REAL_NAME': user.REAL_NAME,
        'USER_GROUP': user.GROUP
    }
    return make_json(True, 'User successful', '', data)

@app.route('/api/plants', methods=['GET'])
@login_required
def api_plants():
    query = PLANTS.query.all()
    return make_json(True, 'PLANTS successful', '', Get_List_From_Query(query))


@app.route('/api/server', methods=['GET'])
@login_required
def api_server():
    status_dict = []
    status_dict.append(['cwd', os.getcwd()])
    status_dict.append(['platform', platform.platform()])
    status_dict.append(['version', platform.version()])
    status_dict.append(['architecture', platform.architecture().__str__()])
    status_dict.append(['machine', platform.machine()])
    status_dict.append(['node', platform.node()])
    status_dict.append(['processor', platform.processor()])
    status_dict.append(['system', platform.system()])
    status_dict.append(['python_build', platform.python_build().__str__()])
    status_dict.append(['python_compiler', platform.python_compiler()])
    status_dict.append(['python_version', platform.python_version()])
    return make_json(True, 'Server status successful', '载入服务器状态成功', status_dict)


@app.route('/api/db_user', methods=['GET'])
@login_required
def api_db_user():
    query = USERS.query.all()
    return make_json(True, 'Db_user info successful', '载入用户数据成功', Get_List_From_Query(query))

#ggg
# return make_json(False, '[{0}] Unknown API'.format(action), '请求的API不存在', {"action": action})
# return make_json(False, '[{0}] Error occored when deal api'.format(action), '处理请求中遇到了错误', {"action": action, "traceback": traceback.format_exc()})

def Get_App():
    return app
