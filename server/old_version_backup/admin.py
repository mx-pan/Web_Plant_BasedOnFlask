from flask import Flask
from flask_admin import Admin, BaseView, expose , AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel


""" 这是flask_admin的处理程序，可以实现数据库管理，文件管理 """

""" 这个模块仅仅提供代码参考 """

app = Flask(__name__,static_folder='../',static_url_path='/static')

# 国际化
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

# 初始化Flask app
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 导入SQLAlchemy ORM 数据库定义
from flask_sqlite import *
db.init_app(app)

# 自定义显示样式
#column_editable_list = ['USERNAME',]#显示弹出的修改窗口
# column_exclude_list = ['PASSWORD',]#不想显示某些字段

class _USERS(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    column_filters = USERS.Columns()#查找
    column_labels = USERS.Column_Translation()#自定义显示column

class _MAIN_MENU(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    column_filters = MAIN_MENU.Columns()#查找
    column_labels = MAIN_MENU.Column_Translation()#自定义显示column

class _SENSOR(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    column_filters = SENSOR.Columns()#查找
    column_labels = SENSOR.Column_Translation()#自定义显示column

class _TRANSPORT(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    column_filters = TRANSPORT.Columns()#查找
    column_labels = TRANSPORT.Column_Translation()#自定义显示column


class my_view(AdminIndexView):
    @expose('/')
    def index(self):
        arg1 = 'Hello'
        return self.render('index.html')

# 初始化 Flask_admin
admin = Admin(app,index_view=my_view(),name='管理后台',template_mode='bootstrap3')

# 初始化Flask Flask-SQLAlchemy Flask-Admin
admin.add_view(_USERS(USERS, db.session,name='用户管理',endpoint='USER', category='数据库管理'))
admin.add_view(_MAIN_MENU(MAIN_MENU, db.session,name='主菜单元素',endpoint='MAIN_MENU', category='数据库管理'))
admin.add_view(_SENSOR(SENSOR, db.session,name='设备与传感器',endpoint='SENSOR', category='数据库管理'))
admin.add_view(_TRANSPORT(TRANSPORT, db.session,name='物流状态',endpoint='TRANSPORT', category='数据库管理'))

# 初始化FileAdmin
admin.add_view(FileAdmin('..', '/static/', name='服务器文件管理',endpoint='file_admin'))

app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
