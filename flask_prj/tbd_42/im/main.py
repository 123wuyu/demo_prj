import eventlet
eventlet.monkey_patch()  # 协程库的函数替换

import eventlet.wsgi
import socketio
import sys
from server import app
import chat
import notify

# sys.argv  存放了启动命令的命令行参数
# python main.py 8080
# sys.argv -> 列表
# sys.argv -> ['main.py', '8080']

if len(sys.argv) < 2:
    print('Usage: python server.py [port].')
    exit(1)

port = int(sys.argv[1])


SERVER_ADDRESS = ('0.0.0.0', port)
listen_sock = eventlet.listen(SERVER_ADDRESS)
eventlet.wsgi.server(listen_sock, app)
