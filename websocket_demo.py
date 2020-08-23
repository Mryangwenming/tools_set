"""
在一个flask项目中使用websocket服务，来做后台消息向前台的推送，可以在manany.py文件里面使用一下的代码，主要逻辑就是使用一个子进程去启动websocket服务，
然后每个连接websocket服务的客户端进来，都会生成一个子线程来进行消息的监听，并且将客户端的websocket对象存储到一个列表的全局变量中，当queue对列中有消息时，
遍历全局变量的列表，如果websocket断开连接了，那么直接在列表中移除，正常的向前段推送消息
"""



from flask_sockets import Sockets
from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi

sockets = Sockets(app)
WS = []

import json
from app.infiltrate.api_v1.admin.operation import msg
from threading import Thread
from geventwebsocket import WebSocketError
from flask import request

@sockets.route('/')
def tell_notice(ws):
    global WS
    _msg = None
    WS.append(ws)
    ws.send("{}已连接".format(ws))
    remote = request.environ.get("REMOTE_ADDR")
    import logging
    logging.info("{}已连接".format(remote))
    logging.info(WS)
    b = Thread(target=send_msg)
    b.setDaemon(True)
    b.start()
    ws.receive()



def send_msg():
    global WS
    while True:
        _msg = msg.get()
        for _ws in WS:

            try:
                _ws.send(json.dumps(_msg))
            except WebSocketError:
                WS.remove(_ws)

def socket_server(app):
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 8888), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()

from multiprocessing import Process

a = Process(target=socket_server, args=(app, ))
a.start()
