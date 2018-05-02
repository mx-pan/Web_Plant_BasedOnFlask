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


class PLANTS(db.Model, Table_Common):  # 植物信息
    """ 添加数据表,每个数据表都是一个Python类,应类似的形式 """
    __tablename__ = 'PLANTS'
    id = db.Column(db.Integer, primary_key=True)
    PLANTS_NAME = db.Column(db.Text, nullable=False)
    PLANTS_ALIAS = db.Column(db.Text, nullable=False)
    PLANTS_FAMILY = db.Column(db.Text, nullable=False)
    PLANTS_GENUS = db.Column(db.Text, nullable=False)
    PLANTS_ID = db.Column(db.Text, nullable=False)
    IMAGE = db.Column(db.Text, nullable=False)
    STATUS = db.Column(db.Text, nullable=False)
    PLANTS_HABIT = db.Column(db.Text)
    COLOR = db.Column(db.Text, nullable=False)
    PLANTS_IP = db.Column(db.Text)
    PLANTS_PORT = db.Column(db.Text)

    Columns = ['PLANTS_NAME', 'PLANTS_ALIAS', 'PLANTS_FAMILY', 'PLANTS_GENUS', 'PLANTS_ID',
               'IMAGE', 'STATUS', 'PLANTS_HABIT', 'COLOR', 'PLANTS_IP', 'PLANTS_PORT']
    Translation = {'PLANTS_NAME': '名称',
                   'PLANTS_ALIAS': '别名',
                   'PLANTS_FAMILY': '科名',
                   'PLANTS_GENUS': '属名',
                   'PLANTS_ID': '植株编号',
                   'IMAGE': '缩略图',
                   'STATUS': '状态',
                   'PLANTS_HABIT': '习性',
                   'IMAGE': '缩略图',
                   'COLOR': '颜色',
                   'PLANTS_IP': 'IP地址',
                   'PLANTS_PORT': '端口号'}

    def __init__(self, PLANTS_NAME='', PLANTS_ALIAS='', PLANTS_FAMILY='', PLANTS_GENUS='', PLANTS_ID='', IMAGE='', STATUS='',
                 PLANTS_HABIT='', COLOR='', PLANTS_IP='', PLANTS_PORT=''):
        self.PLANTS_NAME = PLANTS_NAME
        self.PLANTS_ALIAS = PLANTS_ALIAS
        self.PLANTS_FAMILY = PLANTS_FAMILY
        self.PLANTS_GENUS = PLANTS_GENUS
        self.PLANTS_ID = PLANTS_ID
        self.IMAGE = IMAGE
        self.STATUS = STATUS
        self.PLANTS_HABIT = PLANTS_HABIT
        self.COLOR = COLOR
        self.PLANTS_IP = PLANTS_IP
        self.PLANTS_PORT = PLANTS_PORT

    def __repr__(self):
        return '<NAME: %r>' % self.NAME


        
class ZONE(db.Model, Table_Common):  # 区域信息
    """ 添加数据表,每个数据表都是一个Python类,应类似的形式 """
    __tablename__ = 'ZONE'
    id = db.Column(db.Integer, primary_key=True)
    ZONE_NAME = db.Column(db.Text, nullable=False)
    ZONE_TYPE = db.Column(db.Text, nullable=False)
    NODE_LOCATION = db.Column(db.Text, nullable=False)
    NODE_ID = db.Column(db.Text, nullable=False)
    ZONE_ID = db.Column(db.Text, nullable=False)
    IMAGE = db.Column(db.Text, nullable=False)
    STATUS = db.Column(db.Text, nullable=False)
    CAUSE = db.Column(db.Text)
    COLOR = db.Column(db.Text, nullable=False)
    ZONE_IP = db.Column(db.Text)
    ZONE_PORT = db.Column(db.Text)

    Columns = ['ZONE_NAME', 'ZONE_TYPE', 'NODE_LOCATION', 'NODE_ID', 'ZONE_ID',
               'IMAGE', 'STATUS', 'CAUSE', 'COLOR', 'ZONE_IP', 'ZONE_PORT']
    Translation = {'ZONE_NAME': '名字',
                   'ZONE_TYPE': '类型',
                   'NODE_LOCATION': '节点位置描述',
                   'NODE_ID': '节点编码',
                   'ZONE_ID': '传感器编号',
                   'IMAGE': '缩略图',
                   'STATUS': '状态',
                   'CAUSE': '故障原因',
                   'IMAGE': '缩略图',
                   'COLOR': '颜色',
                   'ZONE_IP': 'IP地址',
                   'ZONE_PORT': '端口号'}

    def __init__(self, ZONE_NAME='', ZONE_TYPE='', NODE_LOCATION='', NODE_ID='', ZONE_ID='', IMAGE='', STATUS='',
                 CAUSE='', COLOR='', ZONE_IP='', ZONE_PORT=''):
        self.ZONE_NAME = ZONE_NAME
        self.ZONE_TYPE = ZONE_TYPE
        self.NODE_LOCATION = NODE_LOCATION
        self.NODE_ID = NODE_ID
        self.ZONE_ID = ZONE_ID
        self.IMAGE = IMAGE
        self.STATUS = STATUS
        self.CAUSE = CAUSE
        self.COLOR = COLOR
        self.ZONE_IP = ZONE_IP
        self.ZONE_PORT = ZONE_PORT

    def __repr__(self):
        return '<NAME: %r>' % self.NAME