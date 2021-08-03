import socketio


# 为socketio服务器添加manager对象，帮助从rabbitmq取推送任务
RABBITMQ = 'amqp://python:rabbitmqpwd@localhost:5672/toutiao'
mgr = socketio.KombuManager(RABBITMQ)

# 创建协程服务器 运行socketio
sio = socketio.Server(async_mode='eventlet', client_manager=mgr)
app = socketio.Middleware(sio)

