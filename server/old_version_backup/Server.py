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
from flask import Flask, safe_join, send_file, make_response, jsonify, escape, request, session, redirect, url_for
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from server.james_sqlite import DB_Sqlite

""" 这个模块已经废弃 """

""" 这是旧版本的服务器，使用SQLAlchemy来管理数据库 """

# Only in Python 2
# if(platform.python_version().startswith('2.')):
#   reload(sys)
#   sys.setdefaultencoding('utf-8')

# app = flask.Flask(__name__, static_folder='./static',static_url_path='/static')

app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

db = DB_Sqlite('./server/SYSTEM.DB')


def make_json(state, data, msg):
    return jsonify({'state': state, 'data': data, 'msg': msg})


@app.errorhandler(404)
def page_not_found(error):
    return make_json('FAIL', {"dir": os.getcwd()}, '404 by error handler')


@app.route('/', methods=['GET'])
def root_redirect():
    return redirect("/index.html")


@app.route('/<path:filename>', methods=['GET'])
def any_file(filename):
    full_path = safe_join(os.getcwd() + '/www/', filename)
    try:
        return send_file(full_path, attachment_filename=full_path, conditional=True)
    except:
        return make_json('FAIL', {'requre': filename, "dir": os.getcwd(), "full_path": full_path, "traceback": traceback.format_exc()}, "404 by router")


@app.route('/api/login/<username>/<password>', methods=['GET'])
def api_login(username, password):
    username = re.sub('[^a-zA-Z0-9]', '', username)
    password = re.sub('[^a-zA-Z0-9]', '', password)
    sql_ext = "WHERE USERNAME='{0}' AND PASSWORD='{1}'".format(
        username, password)
    state, result = db.Select(
        'USER_INFO', ['USERNAME', 'REAL_NAME', 'USER_GROUP'], sql_ext)
    if(state):
        if(len(result) != 0):
            session.permanent = True
            app.permanent_session_lifetime = datetime.timedelta(minutes=5)
            session['USERNAME'] = result[0]['USERNAME']
            session['REAL_NAME'] = result[0]['REAL_NAME']
            session['USER_GROUP'] = result[0]['USER_GROUP']
            return make_json('SUCC', '', '登录成功。欢迎你，'+result[0]['REAL_NAME'])
        else:
            return make_json('FAIL', '', '用户名或密码错误')
    else:
        return make_json('FAIL', '', '服务器内部错误')


@app.route('/api/data/<api_raw>', methods=['GET'])
def api_data(api_raw):
    kind = re.sub('[^a-zA-Z0-9_-]', '', api_raw)
    if 'USERNAME' not in session:
        return make_json('FAIL', 'LOGIN', "未登录")

    if kind == 'check':
        return make_json('SUCC', '', "您已登录")
    elif kind == 'sensor':
        state, result = db.Select(
            'SENSOR_INFO', ['NAME', 'IMG_SRC', 'STATUS', 'COLOR', 'CAUSE', 'DETAIL'])
        if(state):
            return make_json('SUCC', result, '状态数据载入成功')
        else:
            return make_json('FAIL', '', '载入失败，内部错误')
    elif kind == 'transport':
        state, result = db.Select(
            'TRANSPORT_INFO', ['NAME', 'IMG_SRC', 'STATUS', 'COLOR', 'CAUSE', 'DETAIL'])
        if(state):
            return make_json('SUCC', result, '物流数据载入成功')
        else:
            return make_json('FAIL', '', '载入失败，内部错误')
    elif kind == 'main_menu':
        state, result = db.Select(
            'MAIN_MENU_INFO', ['TITLE', 'TARGET', 'SUBTITLE', 'COLOR', 'ICON', 'AUTHORITY'])
        if(state):
            return make_json('SUCC', result, '首页数据载入成功')
        else:
            return make_json('FAIL', '', "载入失败，内部错误")
    elif kind == 'user':
        GROUP = {'DOC': '医护人员', 'MAN': '管理人员', 'ENG': '工程人员', 'SU': '超级用户'}
        if session['USER_GROUP'] in GROUP:
            user_group = GROUP[session['USER_GROUP']]
        else:
            user_group = 'unknown'
        result = {'USERNAME': session['USERNAME'],
                  'REAL_NAME': session['REAL_NAME'], 'USER_GROUP': user_group}
        return make_json('SUCC', result, '获取用户信息成功')
    elif kind == 'logout':
        session.pop('USERNAME')
        return make_json('SUCC', '', '登出成功')
    elif kind == 'server':
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
    elif kind == 'db-user':
        state, result = db.Select(
            'USER_INFO', ['USERNAME', 'REAL_NAME', 'USER_GROUP'])
        if(state):
            return make_json('SUCC', result, '载入服务器状态成功')
        else:
            return make_json('FAIL', '', '数据库错误')
    else:
        return make_json('FAIL', '', '未知API')


def Get_App():
    return app
