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
from flask import Flask, safe_join, send_file, make_response, jsonify, escape, request, redirect, url_for#,session
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from flask_login import current_user ,login_user, logout_user, LoginManager,login_required

""" 这是项目Flask 服务器主程序的地址 """

""" 为支持Python2 不同编码模式而使用的代码 """
# if(platform.python_version().startswith('2.')):
#   reload(sys)
#   sys.setdefaultencoding('utf-8')


# 初始化Flask app
app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 导入SQLAlchemy ORM 数据库定义
from server.flask_sqlite import *
db.init_app(app)

# 国际化设置，将语言设置为中文
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

# 处理 Flask_admin 的登录问题
login_manager = LoginManager()
login_manager.session_protection='basic'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    print(db.session.query(USERS).filter_by(id=username).first())
    return db.session.query(USERS).filter_by(id=username).first()
    #return USERS.query.get(username)

# 初始化 Flask_admin 的数据库显示编辑功能
class _USERS(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    column_filters = USERS.Columns() # 查找功能
    column_labels = USERS.Column_Translation() # 自定义显示column

class _MAIN_MENU(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    column_filters = MAIN_MENU.Columns() # 查找功能
    column_labels = MAIN_MENU.Column_Translation() # 自定义显示column

class _SENSOR(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    column_filters = SENSOR.Columns() # 查找功能
    column_labels = SENSOR.Column_Translation() # 自定义显示column

class _TRANSPORT(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    column_filters = TRANSPORT.Columns()#查找
    column_labels = TRANSPORT.Column_Translation()#自定义显示column

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
admin = Admin(app,index_view=my_view(),name='管理后台',template_mode='bootstrap3')

# 将试图显示功能添加到页面中
admin.add_view(_USERS(USERS, db.session,name='用户管理',endpoint='USER', category='数据库管理'))
admin.add_view(_MAIN_MENU(MAIN_MENU, db.session,name='主菜单元素',endpoint='MAIN_MENU', category='数据库管理'))
admin.add_view(_SENSOR(SENSOR, db.session,name='设备与传感器',endpoint='SENSOR', category='数据库管理'))
admin.add_view(_TRANSPORT(TRANSPORT, db.session,name='物流状态',endpoint='TRANSPORT', category='数据库管理'))


def make_json(state, data, msg):
    """发送通用反馈给前端 

    `state` 是这次请求的结果，只有SUCC FAIL两个值
    `data` 是请求的结果或错误信息，可为空
    `msg` 是显示给用户的一个提示信息"""
    return jsonify({'state': state, 'data': data, 'msg': msg})


@app.errorhandler(404)
def page_not_found(error):
    """重定义404页面"""
    return make_json('FAIL', {"dir": os.getcwd()}, '404 by error handler')


@app.route('/', methods=['GET'])
def root_redirect():
    """如果用户访问了根页面，则重定向用户到首页"""
    return redirect("/file/index.html")


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    """如果用户请求了网页图标，则给用户发送图标"""
    return any_file('assets/icon/favicon.png')


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
        cause={'requre': filename, "dir": os.getcwd(), "full_path": full_path, "traceback": traceback.format_exc()}
        return make_json('FAIL',cause , "404 by router")


@app.route('/api/login/<username>/<password>', methods=['GET'])
def api_login(username, password):
    """ 处理用户登陆 """
    # 清除请求中除了 a-zA-Z0-9_- 之外所有字符
    username = re.sub('[^a-zA-Z0-9]', '', username)
    password = re.sub('[^a-zA-Z0-9]', '', password)

    try:
        # 查询指定的用户
        user = USERS.query.filter_by(USERNAME=username).first()

        # 如果查找到了这个用户
        if(user != None):
            # 且密码正确
            if(user.PASSWORD == password):
                # 登录这个用户
                login_user(user,True)
                #session.permanent = True
                #app.permanent_session_lifetime = datetime.timedelta(minutes=60)
                #session['USERNAME'] = user.USERNAME
                return make_json('SUCC', '', 'Login Success : '+user.USERNAME)
            else:
                return make_json('FAIL', '', 'Username or password error')
        else:
            return make_json('FAIL', '', 'Username not exist')
    except:
        return make_json('FAIL', traceback.format_exc(), 'Server internal error')


@app.route('/api/data/<api_raw>', methods=['GET'])
@login_required
def api_data(api_raw):
    """ 处理api """
    # 清除请求中除了 a-zA-Z0-9_- 之外所有字符
    action = re.sub('[^a-zA-Z0-9_-]', '', api_raw)

    # 如果用户没有登录，则强制用户登录
    #if 'USERNAME' not in session:return make_json('FAIL', 'LOGIN', "Login required")

    # 开始处理请求
    try:
        if action == 'check':
            return make_json('SUCC', '', "您已登录")

        elif action == 'sensor':
            query = SENSOR.query.all()
            return make_json('SUCC', Get_List_From_Query(query), '状态数据载入成功')

        elif action == 'transport':
            query = TRANSPORT.query.all()
            return make_json('SUCC', Get_List_From_Query(query), '物流数据载入成功')

        elif action == 'main_menu':
            query = MAIN_MENU.query.all()
            return make_json('SUCC', Get_List_From_Query(query), '首页数据载入成功')

        elif action == 'user':
            user = USERS.query.filter_by(USERNAME=session['USERNAME']).first()
            GROUP = {'admin': '管理员', 'station': '站点人员', 'maintain': '维护人员'}
            Group_Friendly = GROUP[user.GROUP]
            result = {'USERNAME': user.USERNAME,'REAL_NAME': session['REAL_NAME'], 'USER_GROUP': Group_Friendly}
            return make_json('SUCC', result, '获取用户信息成功')

        elif action == 'logout':
            #session.pop('USERNAME')
            logout_user()
            return make_json('SUCC', '', '登出成功')

        elif action == 'server':
            # 下面获取服务器的各项信息
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
            return make_json('SUCC', status_dict, '载入服务器状态成功')

        elif action == 'db-user':
            query = USERS.query.all()
            return make_json('SUCC', Get_List_From_Query(query), '载入用户数据成功')

        else:
            # 请求的API不存在
            return make_json('FAIL', {"action":action}, 'Unknown API')
    except:
        # 处理请求中遇到了错误，把错误信息返回
        return make_json('FAIL', {"action":action,"traceback":traceback.format_exc()}, 'Server internal error')

def Get_App():
    return app
