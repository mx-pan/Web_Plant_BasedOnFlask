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
    db.session.add(USERS('pmx', 'pmx', '管理员', 'ALL',  '潘淼鑫', '1120151488', '开发部门',
                         '管理中心', '01', '18801234567'))
    db.session.add(USERS('qyt', 'qyt', '管理员', 'ALL',  '瞿云涛', '1120151481', '开发部门',
                         '管理中心', '01', '18801234567'))
    db.session.add(USERS('mzl', 'mzl', '管理员', 'ALL',  '马占林', '1120151487', '开发部门',
                         '管理中心', '01', '18801234567'))
    db.session.add(USERS('lmn', 'lmn', '管理员', 'ALL',  '李曼妮', '1120151506', '开发部门',
                         '管理中心', '01', '18801234567'))
    db.session.add(USERS('cjc', 'cjc', '管理员', 'ALL',  '陈嘉诚', '1120151500', '开发部门',
                         '管理中心', '01', '18801234567'))
    db.session.add(USERS('user1', 'test', '养护人员', 'STATION',  '张三', '1120141234', '养护站',
                         '养护站', '01', '13901234567'))
    db.session.add(USERS('user2', 'test', '养护人员', 'STATION',  '李四', '1120151234', '养护站',
                         '养护站', '01', '13901234567'))
    db.session.add(USERS('user3', 'test', '养护人员', 'MAINTAINER', '王五', '1120161234',
                         '养护站', '养护站', '02', '13901234567'))

#    db.session.add(MAIN_MENU('设备状态', 'StatusPage', "网关及传感器状态",
#                             "mycolor1", "medkit", '[ALL], [STATION]', 'NONE'))
#    db.session.add(MAIN_MENU('xxxx', 'xxxx', "xxxx",
#                             "mycolor2", "xxxx", '[ALL], [STATION]', '1'))
#    db.session.add(MAIN_MENU('xxxx', 'xxxx', "xxxx",
#                             "mycolor3", "xxxx", '[ALL], [STATION]', '2'))
#    db.session.add(MAIN_MENU('系统控制', 'xxxx', "xxxx",
#                             "mycolor4", "xxxx", 'ALL', 'NONE'))
#    db.session.add(MAIN_MENU('我', 'UserPage', "用户信息管理", "mycolor5",
#                             "person", '[ALL], [STATION],[MAINTAINER]', 'NONE'))
#    db.session.add(MAIN_MENU('设置', 'SettingsPage', "系统设置",
#                             "mycolor6", "hammer", 'ALL', 'NONE'))
#    db.session.add(MAIN_MENU('文档&帮助', 'DocumentPage', "系统介绍,操作指南",
#                             "mycolor1", "document", 'ALL', 'NONE'))
#    db.session.add(MAIN_MENU('数据库管理', 'DbManagerPage',
#                             "仅限工程人员使用", "mycolor2", "analytics", 'ALL', '新'))
#    db.session.add(MAIN_MENU('服务器管理', 'ServerManagerPage',
#                             "仅限工程人员使用", "mycolor3", "outlet", 'ALL', 'NONE'))

#    db.session.add(SENSOR('空气温度传感器', '01', "这个节点位于XXXX", '05-001',"20180419-01-001", "/file/assets/imgs/agv.png", '故障', '', "danger", '127.0.0.12', '8080'))
#    db.session.add(SENSOR('土壤湿度传感器', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))

    db.session.add(PLANTS('紫荆', '裸枝树，紫珠', "豆科", '紫荆属',"紫荆-001", "/file/assets/imgs/agv.png", '良好', '暖带树种，较耐寒。喜光，稍耐阴。喜肥沃、排水良好的土壤，不耐湿。', "??", '127.0.0.12', '8080'))
    db.session.add(PLANTS('樱花','东京樱花，日本樱花','蔷薇科','樱属',"樱花-001", "/file/assets/imgs/agv.png", '良好', '性喜阳光和温暖湿润的气候条件，有一定耐寒及抗旱能力，但对烟及风抗力弱。不耐酸碱土，根系较浅，忌积水洼地', "??", '127.0.0.12', '8080'))
    db.session.add(PLANTS('西府海棠','无','蔷薇科','苹果属',"海棠-001", "/file/assets/imgs/agv.png", '良好', '喜光，耐寒，忌水涝，忌空气过湿，较耐旱', "??", '127.0.0.12', '8080'))
    db.session.add(PLANTS('海棠花','无','蔷薇科','苹果属',"海棠-002", "/file/assets/imgs/agv.png", '良好', '性喜阳光，不耐阴，忌水湿，极为耐寒', "??", '127.0.0.12', '8080'))

    db.session.add(ZONE('01', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('02', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('03', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('04', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('05', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('06', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('07', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('08', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('09', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('10', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('11', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('12', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('13', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('14', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('15', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('16', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('17', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('18', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('19', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('20', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))
    db.session.add(ZONE('21', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '127.0.0.13', '8080'))

    db.session.add(SENSOR('01', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('02', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('03', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('04', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('05', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('06', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('07', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('08', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('09', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('10', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('11', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '27', '60'))
    db.session.add(SENSOR('12', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '22', '60'))
    db.session.add(SENSOR('13', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '22', '60'))
    db.session.add(SENSOR('14', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '22', '30'))
    db.session.add(SENSOR('15', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '22', '30'))
    db.session.add(SENSOR('16', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '22', '30'))
    db.session.add(SENSOR('17', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '22', '30'))
    db.session.add(SENSOR('18', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '22', '30'))
    db.session.add(SENSOR('19', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '22', '30'))
    db.session.add(SENSOR('20', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '22', '30'))
    db.session.add(SENSOR('21', '02', "这个节点位于XXXX", '05-001',"20180419-02-001", "/file/assets/imgs/agv.png", '正常', "", "secondary", '22', '30'))

    db.session.commit()


db.drop_all()
db.create_all()
add_data()