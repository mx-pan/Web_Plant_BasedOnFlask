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
from flask_sqlalchemy import SQLAlchemy


""" 数据库初始化程序 """
""" 运行这个程序将清除数据库中所有数据，运行之前请先备份原有数据 """

app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from flask_sqlite import *
db.init_app(app)
app.app_context().push()

def add_data():
    db.session.add(USERS('user1', 'test', '管理员', 'ALL',  '张三', '1120141234', '管理部门',
                         '管理中心', '01', '13901234567'))
    db.session.add(USERS('user2', 'test', '养护人员', 'STATION',  '李四', '1120151234', '养护站',
                         '养护站', '01', '13901234567'))
    db.session.add(USERS('user3', 'test', '养护人员', 'MAINTAINER', '王五', '1120161234',
                         '养护站', '养护站', '02', '13901234567'))

    db.session.add(MAIN_MENU('设备状态', 'StatusPage', "AGV及传感器状态",
                             "mycolor1", "medkit", '[ALL], [STATION]', 'NONE'))
    db.session.add(MAIN_MENU('物流状态', 'TansportPage', "物流传输状态",
                             "mycolor2", "stats", '[ALL], [STATION]', '1'))
    db.session.add(MAIN_MENU('收发物品', 'TansmitPage', "确认接收或发送物品",
                             "mycolor3", "medical", '[ALL], [STATION]', '2'))
    db.session.add(MAIN_MENU('系统控制', 'ControlPage', "AGV及物流控制",
                             "mycolor4", "construct", 'ALL', 'NONE'))
    db.session.add(MAIN_MENU('我', 'UserPage', "用户信息管理", "mycolor5",
                             "person", '[ALL], [STATION],[MAINTAINER]', 'NONE'))
    db.session.add(MAIN_MENU('设置', 'SettingsPage', "系统设置",
                             "mycolor6", "hammer", 'ALL', 'NONE'))
    db.session.add(MAIN_MENU('文档&帮助', 'DocumentPage', "系统介绍,操作指南",
                             "mycolor1", "document", 'ALL', 'NONE'))
    db.session.add(MAIN_MENU('数据库管理', 'DbManagerPage',
                             "仅限工程人员使用。", "mycolor2", "analytics", 'ALL', '新'))
    db.session.add(MAIN_MENU('服务器管理', 'ServerManagerPage',
                             "仅限工程人员使用", "mycolor3", "outlet", 'ALL', 'NONE'))

    db.session.add(SENSOR('AGV1条码扫描仪1', '01', "这个节点位于XXXX", '05-001',"20180317-01-001", "/file/assets/imgs/agv.png", '故障', '', "danger", '127.0.0.12', '8080'))
    db.session.add(SENSOR('REID扫描仪1', '02', "这个节点位于XXXX", '05-001',"20180317-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))

    db.session.add(PLANTS('紫荆', '裸枝树，紫珠', "豆科", '紫荆属',"紫荆-001", "/file/assets/imgs/agv.png", '良好', '暖带树种，较耐寒。喜光，稍耐阴。喜肥沃、排水良好的土壤，不耐湿。', "??", '127.0.0.12', '8080'))
 
    db.session.commit()


db.drop_all()
db.create_all()
add_data()