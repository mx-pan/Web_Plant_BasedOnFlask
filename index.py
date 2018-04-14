#-*- coding:utf-8 -*-
from __future__ import print_function
import os
import sys
import getopt


""" 导入 flask app 对象实例 """
from server.Server import Get_App
app = Get_App()

Host = '0.0.0.0'
Port = 80
Debug_mode = False
try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["host=", "port=", "debug"])
except getopt.GetoptError:
    print('index.py --host <Host> --port <Port> --debug')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('Usage: index.py --host <Host> --port <Port> --debug')
        sys.exit()
    elif opt in ("--host"):
        Host = arg
    elif opt in ("--port"):
        Port = int(arg)
    elif opt in ("--debug"):
        Debug_mode = True
app.run(host=Host, port=Port, threaded=True, debug=Debug_mode)


"""if(os.getcwd().startswith("/home/bae")):
    # 程序运行在BAE容器中
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(app)
else:
    # 程序运行在本地
    # 将用户输入的参数列表除了第一项之外传给参数处理函数
    Local_Server(sys.argv[1:])"""
