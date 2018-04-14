# -*- coding: utf-8 -*-
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView

# 初始化数据库
db = SQLAlchemy()


def Get_List_From_Query(query):
    """ 若请求返回了多个结果，将多个结果转换成一个list """
    _list = []
    for row in query:
        _list.append(row.get_dict())
    return _list


class Table_Common():
    """ 所有数据表类的公共父类 """

    def get_dict(self):
        value_dict = {}
        for x in self.__dict__:
            if isinstance(self.__dict__[x], str):
                value_dict[x] = self.__dict__[x]
        return value_dict


class USERS(db.Model, UserMixin, Table_Common):
    """ 添加数据表,每个数据表都是一个Python类,应类似的形式 """
    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key=True)
    USERNAME = db.Column(db.Text, unique=True, nullable=False)
    PASSWORD = db.Column(db.Text, nullable=False)
    GROUP = db.Column(db.Text, nullable=False)
    AUTHORITY = db.Column(db.Text, nullable=False)
    REAL_NAME = db.Column(db.Text, nullable=False)
    EMPLOYEE_NUMBER = db.Column(db.Text, nullable=False)
    DEPARTMENT = db.Column(db.Text, nullable=False)
    COMMON_DEPARTMENT = db.Column(db.Text, nullable=False)
    TYPE_OF_ALARM = db.Column(db.Text, nullable=False)
    PHONE = db.Column(db.Text)

    Form_Choices = {
        'GROUP': [('管理员', '管理员'), ('站点人员', '站点人员'), ('维护人员', '维护人员')],
        'DEPARTMENT': [('管理处', '管理处'), ('护士站', '护士站'), ('工程部', '工程部')]}
    Columns = ['USERNAME', 'PASSWORD', 'GROUP', 'AUTHORITY', 'REAL_NAME',
               'EMPLOYEE_NUMBER', 'DEPARTMENT', 'COMMON_DEPARTMENT', 'TYPE_OF_ALARM', 'PHONE']
    Translation = {
        'USERNAME': '用户名',
        'PASSWORD': '密码',
        'GROUP': '用户组',
        'AUTHORITY': '权限',
        'REAL_NAME': '真实姓名',
        'EMPLOYEE_NUMBER': '工号',
        'DEPARTMENT': '科室',
        'COMMON_DEPARTMENT': '常用站点设置 ',
        'TYPE_OF_ALARM': '报警方式',
        'PHONE': '电话'}

    def __init__(self, USERNAME='', PASSWORD='', GROUP='', AUTHORITY='', REAL_NAME='',
                 EMPLOYEE_NUMBER='', DEPARTMENT='', COMMON_DEPARTMENT='', TYPE_OF_ALARM='', PHONE=''):
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.GROUP = GROUP
        self.AUTHORITY = AUTHORITY
        self.REAL_NAME = REAL_NAME
        self.EMPLOYEE_NUMBER = EMPLOYEE_NUMBER
        self.DEPARTMENT = DEPARTMENT
        self.COMMON_DEPARTMENT = COMMON_DEPARTMENT
        self.TYPE_OF_ALARM = TYPE_OF_ALARM
        self.PHONE = PHONE

    def __repr__(self):
        return '<USERNAME: %r>' % self.USERNAME


class MAIN_MENU(db.Model, Table_Common):
    """ 添加数据表,每个数据表都是一个Python类,使用类似的形式 """
    __tablename__ = 'MAIN_MENU'
    id = db.Column(db.Integer, primary_key=True)
    TITLE = db.Column(db.Text, nullable=False)
    TARGET = db.Column(db.Text, nullable=False)
    SUBTITLE = db.Column(db.Text, nullable=False)
    COLOR = db.Column(db.Text, nullable=False)
    ICON = db.Column(db.Text, nullable=False)
    AUTHORITY = db.Column(db.Text, nullable=False)
    BADGE = db.Column(db.Text, nullable=False)

    Columns = ['TITLE', 'TARGET', 'SUBTITLE',
               'COLOR', 'ICON', 'AUTHORITY', 'BADGE']
    Translation = {'TITLE': '标题',
                   'TARGET': '目标页面',
                   'SUBTITLE': '副标题',
                   'COLOR': '颜色',
                   'ICON': '图标',
                   'AUTHORITY': '权限',
                   'BADGE': '徽章'}

    def __init__(self, TITLE='', TARGET='', SUBTITLE='', COLOR='', ICON='', AUTHORITY='', BADGE=''):
        self.TITLE = TITLE
        self.TARGET = TARGET
        self.SUBTITLE = SUBTITLE
        self.COLOR = COLOR
        self.ICON = ICON
        self.AUTHORITY = AUTHORITY
        self.BADGE = BADGE

    def __repr__(self):
        return '<TITLE: %r>' % self.TITLE


class SENSOR(db.Model, Table_Common):  # 传感器信息
    """ 添加数据表,每个数据表都是一个Python类,应类似的形式 """
    __tablename__ = 'SENSOR'
    id = db.Column(db.Integer, primary_key=True)
    SENSOR_NAME = db.Column(db.Text, nullable=False)
    SENSOR_TYPE = db.Column(db.Text, nullable=False)
    NODE_LOCATION = db.Column(db.Text, nullable=False)
    NODE_ID = db.Column(db.Text, nullable=False)
    SENSOR_ID = db.Column(db.Text, nullable=False)
    IMAGE = db.Column(db.Text, nullable=False)
    STATUS = db.Column(db.Text, nullable=False)
    CAUSE = db.Column(db.Text)
    COLOR = db.Column(db.Text, nullable=False)
    SENSOR_IP = db.Column(db.Text)
    SENSOR_PORT = db.Column(db.Text)

    Columns = ['SENSOR_NAME', 'SENSOR_TYPE', 'NODE_LOCATION', 'NODE_ID', 'SENSOR_ID',
               'IMAGE', 'STATUS', 'CAUSE', 'COLOR', 'SENSOR_IP', 'SENSOR_PORT']
    Translation = {'SENSOR_NAME': '名字',
                   'SENSOR_TYPE': '类型',
                   'NODE_LOCATION': '节点位置描述',
                   'NODE_ID': '节点编码',
                   'SENSOR_ID': '传感器编号',
                   'IMAGE': '缩略图',
                   'STATUS': '状态',
                   'CAUSE': '故障原因',
                   'IMAGE': '缩略图',
                   'COLOR': '颜色',
                   'SENSOR_IP': 'IP地址',
                   'SENSOR_PORT': '端口号'}

    def __init__(self, SENSOR_NAME='', SENSOR_TYPE='', NODE_LOCATION='', NODE_ID='', SENSOR_ID='', IMAGE='', STATUS='',
                 CAUSE='', COLOR='', SENSOR_IP='', SENSOR_PORT=''):
        self.SENSOR_NAME = SENSOR_NAME
        self.SENSOR_TYPE = SENSOR_TYPE
        self.NODE_LOCATION = NODE_LOCATION
        self.NODE_ID = NODE_ID
        self.SENSOR_ID = SENSOR_ID
        self.IMAGE = IMAGE
        self.STATUS = STATUS
        self.CAUSE = CAUSE
        self.COLOR = COLOR
        self.SENSOR_IP = SENSOR_IP
        self.SENSOR_PORT = SENSOR_PORT

    def __repr__(self):
        return '<NAME: %r>' % self.NAME


class TRANSPORT(db.Model, Table_Common):  # 运输单元信息
    """ 添加数据表,每个数据表都是一个Python类,应类似的形式 """

    __tablename__ = 'TRANSPORT'
    id = db.Column(db.Integer, primary_key=True)
    TRANSPORT_NAME = db.Column(db.Text, nullable=False)
    TRANSPORT_TYPE = db.Column(db.Text, nullable=False)
    TRANSPORT_CODE = db.Column(db.Text, nullable=False)
    TRANSPORT_RFID = db.Column(db.Text, nullable=False)
    IMAGE = db.Column(db.Text, nullable=False)
    STATUS = db.Column(db.Text, nullable=False)
    CAUSE = db.Column(db.Text)
    COLOR = db.Column(db.Text, nullable=False)
    TRANSPORT_IP = db.Column(db.Text)
    TRANSPORT_PORT = db.Column(db.Text)

    Columns = ['TRANSPORT_NAME', 'TRANSPORT_TYPE', 'TRANSPORT_CODE', 'TRANSPORT_RFID',
               'IMAGE', 'STATUS', 'CAUSE', 'COLOR', 'TRANSPORT_IP', 'TRANSPORT_PORT']
    Translation = {'TRANSPORT_NAME': '名称',
                   'TRANSPORT_TYPE': '类型 ',
                   'TRANSPORT_CODE': '条码',
                   'TRANSPORT_RFID': 'RFID',
                   'IMAGE': '缩略图',
                   'STATUS': '状态',
                   'CAUSE': '故障原因',
                   'COLOR': '颜色',
                   'TRANSPORT_IP': 'IP地址',
                   'TRANSPORT_PORT': '端口号'}

    def __init__(self, TRANSPORT_NAME='', TRANSPORT_TYPE='', TRANSPORT_CODE='',  TRANSPORT_RFID='', IMAGE='',
                 STATUS='', CAUSE='', COLOR='', TRANSPORT_IP='', TRANSPORT_PORT=''):
        self.TRANSPORT_NAME = TRANSPORT_NAME
        self.TRANSPORT_TYPE = TRANSPORT_TYPE
        self.TRANSPORT_CODE = TRANSPORT_CODE
        self.TRANSPORT_RFID = TRANSPORT_RFID
        self.IMAGE = IMAGE
        self.STATUS = STATUS
        self.CAUSE = CAUSE
        self.COLOR = COLOR
        self.TRANSPORT_IP = TRANSPORT_IP
        self.TRANSPORT_PORT = TRANSPORT_PORT

    def __repr__(self):
        return '<NAME: %r>' % self.NAME


class TASK(db.Model, Table_Common):
    """ 添加数据表,每个数据表都是一个Python类,应类似的形式 """

    __tablename__ = 'TASK'
    id = db.Column(db.Integer, primary_key=True)
    START_TIME = db.Column(db.Text)
    RECEIVE_TIME = db.Column(db.Text)
    TASK_MUM = db.Column(db.Text)
    TRANSPORT_CODE = db.Column(db.Text)
    TRANSPORT_RFID = db.Column(db.Text)
    START_LOCATION = db.Column(db.Text)
    RECEIVE_LOCATION = db.Column(db.Text)
    SENDER_USERNAME = db.Column(db.Text)
    SENDER_REAL_NAME = db.Column(db.Text)
    START_DEPARTMENT = db.Column(db.Text)
    RECEIVE_DEPARTMENT = db.Column(db.Text)
    SEND_DETAIL = db.Column(db.Text)
    SENSOR_LAST = db.Column(db.Text)
    SENSOR_LAST_TIME = db.Column(db.Text)
    STATUS = db.Column(db.Text)
    CAUSE = db.Column(db.Text)
    COLOR = db.Column(db.Text)
    IMAGE = db.Column(db.Text)
    PATH = db.Column(db.Text)

    Columns = ['START_TIME', 'RECEIVE_TIME', 'TASK_MUM', 'TRANSPORT_CODE', 'TRANSPORT_RFID', 'START_LOCATION',
               'RECEIVE_LOCATION', 'SENDER_USERNAME', 'SENDER_REAL_NAME', 'START_DEPARTMENT', 'RECEIVE_DEPARTMENT',
               'SEND_DETAIL', 'SENSOR_LAST', 'SENSOR_LAST_TIME', 'STATUS', 'CAUSE', 'COLOR', 'IMAGE', 'PATH']
    Translation = {'START_TIME': '开始时间',
                   'RECEIVE_TIME': '结束时间',
                   'TASK_MUM': '任务编号',
                   'TRANSPORT_CODE': '箱体条码',
                   'TRANSPORT_RFID': '箱体RFID',
                   'START_LOCATION': '起始科室编码',
                   'RECEIVE_LOCATION': '目标科室编码',
                   'SENDER_USERNAME': '发送者用户名',
                   'SENDER_REAL_NAME': '发送者姓名',
                   'START_DEPARTMENT': '发送科室',
                   'RECEIVE_DEPARTMENT': '接收科室',
                   'SEND_DETAIL': '备注',
                   'SENSOR_LAST': '最近一次经过的节点',
                   'SENSOR_LAST_TIME': '最近一次被检测的时间',
                   'STATUS': '状态',
                   'CAUSE': '故障原因',
                   'COLOR': '颜色',
                   'IMAGE': '图标',
                   'PATH': '规划路径'}

    def __init__(self, START_TIME='', RECEIVE_TIME='', TASK_MUM='', TRANSPORT_CODE='', TRANSPORT_RFID='', START_LOCATION='',
                 RECEIVE_LOCATION='', SENDER_USERNAME='', SENDER_REAL_NAME='', START_DEPARTMENT='', RECEIVE_DEPARTMENT='',
                 SEND_DETAIL='', SENSOR_LAST='', SENSOR_LAST_TIME='', STATUS='', CAUSE='', COLOR='', IMAGE='', PATH=''):
        self.START_TIME = START_TIME
        self.RECEIVE_TIME = RECEIVE_TIME
        self.TASK_MUM = TASK_MUM
        self.TRANSPORT_CODE = TRANSPORT_CODE
        self.TRANSPORT_RFID = TRANSPORT_RFID
        self.START_LOCATION = START_LOCATION
        self.RECEIVE_LOCATION = RECEIVE_LOCATION
        self.SENDER_USERNAME = SENDER_USERNAME
        self.SENDER_REAL_NAME = SENDER_REAL_NAME
        self.START_DEPARTMENT = START_DEPARTMENT
        self.RECEIVE_DEPARTMENT = RECEIVE_DEPARTMENT
        self.SEND_DETAIL = SEND_DETAIL
        self.SENSOR_LAST = SENSOR_LAST
        self.SENSOR_LAST_TIME = SENSOR_LAST_TIME
        self.STATUS = STATUS
        self.CAUSE = CAUSE
        self.COLOR = COLOR
        self.IMAGE = IMAGE
        self.PATH = PATH

    def __repr__(self):
        return '<NAME: %r>' % self.NAME


class DEPARTMENT(db.Model, Table_Common):
    """ 添加数据表,每个数据表都是一个Python类,应类似的形式 """

    __tablename__ = 'DEPARTMENT'
    id = db.Column(db.Integer, primary_key=True)
    DEPARTMENT_NAME = db.Column(db.Text)
    DEPARTMENT_CODE = db.Column(db.Text)
    DEPARTMENT_LOCATION = db.Column(db.Text)

    Columns = ['DEPARTMENT_NAME', 'DEPARTMENT_CODE', 'DEPARTMENT_LOCATION']
    Translation = {'DEPARTMENT_NAME': '站点（科室）名称',
                   'DEPARTMENT_CODE': '站点（科室）编号',
                   'DEPARTMENT_LOCATION': '站点（科室）位置'}

    def __init__(self, DEPARTMENT_NAME='', DEPARTMENT_CODE='', DEPARTMENT_LOCATION=''):
        self.DEPARTMENT_NAME = DEPARTMENT_NAME
        self.DEPARTMENT_CODE = DEPARTMENT_CODE
        self.DEPARTMENT_LOCATION = DEPARTMENT_LOCATION

    def __repr__(self):
        return '<NAME: %r>' % self.NAME
