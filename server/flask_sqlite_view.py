import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
# 导入数据库结构
from .flask_sqlite import *

# 导出数据的格式选择
EXPORT_TYPES = ['xls', 'yaml', 'csv', 'json']

# 初始化 Flask_admin 的数据库显示编辑功能

class USERS_view(ModelView):
    can_delete = True               # 是否允许用户删除数据
    can_edit = True                 # 是否允许用户编辑数据
    can_create = True               # 是否允许用户新增数据
    can_view_details = True         # 能否查看数据的详细信息
    export_max_rows = 0             # 导出数据的限制数量
    can_export = True               # 是否允许数据导出
    export_types = EXPORT_TYPES     # 导出数据的格式选择
    form_choices = USERS.Form_Choices   # 下拉菜单选择的内容
    column_filters = USERS.Columns      # 查找功能
    column_labels = USERS.Translation   # 自定义显示column
    create_modal = True                # 新建窗口是否是以弹出对话框的方式显示
    edit_modal = True                  # 编辑窗口是否是以弹出对话框的方式显示
    def is_accessible(self):
        return current_user.is_authenticated


class MAIN_MENU_view(ModelView):
    can_delete = True   # 是否允许用户删除数据
    can_edit = True     # 是否允许用户编辑数据
    can_create = True   # 是否允许用户新增数据
    can_view_details = True # 能否查看数据的详细信息
    export_max_rows = 0     # 导出数据的限制数量
    can_export = True       # 是否允许数据导出
    export_types = EXPORT_TYPES# 导出数据的格式选择
    column_filters = MAIN_MENU.Columns      # 查找功能
    column_labels = MAIN_MENU.Translation   # 自定义显示column
    create_modal = True                 # 新建窗口是否是以弹出对话框的方式显示
    edit_modal = True                   # 编辑窗口是否是以弹出对话框的方式显示

class SENSOR_view(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    can_view_details = True
    export_max_rows = 0
    can_export = True
    export_types = EXPORT_TYPES
    column_filters = SENSOR.Columns  # 查找功能
    column_labels = SENSOR.Translation  # 自定义显示column
    create_modal = True                # 新建窗口是否是以弹出对话框的方式显示
    edit_modal = True                  # 编辑窗口是否是以弹出对话框的方式显示


class TRANSPORT_view(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    can_view_details = True
    export_max_rows = 0
    can_export = True
    export_types = EXPORT_TYPES
    column_filters = TRANSPORT.Columns  # 查找
    column_labels = TRANSPORT.Translation  # 自定义显示column
    create_modal = True                # 新建窗口是否是以弹出对话框的方式显示
    edit_modal = True                  # 编辑窗口是否是以弹出对话框的方式显示


class TASK_view(ModelView):
    can_delete = True
    can_edit = False
    can_create = False
    can_view_details = True
    export_max_rows = 0
    can_export = True
    export_types = EXPORT_TYPES
    column_filters = TASK.Columns  # 查找
    column_labels = TASK.Translation  # 自定义显示column
    create_modal = True                # 新建窗口是否是以弹出对话框的方式显示
    edit_modal = True                  # 编辑窗口是否是以弹出对话框的方式显示

class DEPARTMENT_view(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    can_view_details = True
    export_max_rows = 0
    can_export = True
    export_types = EXPORT_TYPES
    column_filters = DEPARTMENT.Columns  # 查找
    column_labels = DEPARTMENT.Translation  # 自定义显示column
    create_modal = True                # 新建窗口是否是以弹出对话框的方式显示
    edit_modal = True                  # 编辑窗口是否是以弹出对话框的方式显示