from server import sio
from werkzeug.wrappers import Request
import jwt
import time


JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :return: dict: payload
    """

    try:
        payload = jwt.decode(token, secret, algorithm=['HS256'])
    except jwt.PyJWTError:
        payload = None

    return payload


@sio.on('connect')
def on_connect(sid, environ):
    """
    与客户端建立好连接后被执行
    :param sid: string sid是socketio为当前连接客户端生成的识别id
    :param environ: dict 在连接握手时客户端发送的握手数据(HTTP报文解析之后的字典)
    """
    msg_data = {
        "msg": "hello",
        "timestmap": round(time.time() * 1000)
    }

    sio.emit('message', msg_data, room=sid)
    # sio.send(msg_data, room=sid)

    # 从客户端连接的请求中取出用户携带的 jwt token
    # socketio将用户连接的请求中携带的http数据都解析之后存到了environ中
    # 借助werkzeug 帮助我们解读这个字典， 转换成类似于flask中提供的request对象
    request = Request(environ)

    # 用户携带的token在查询字符串中
    token = request.args.get('token')

    if token:
        # 验证token的有效性
        payload = verify_jwt(token, JWT_SECRET)

        # 如果token 有效 取出与用户的user_id  将用户客户端添加到专属房间room中
        if payload is not None:
            user_id = payload.get('user_id')

            sio.enter_room(sid, str(user_id))


@sio.on('disconnect')
def on_disconnect(sid):
    """
    客户端断开连接之后执行
    :return:
    """
    # 查询sid所在的房间
    rooms = sio.rooms(sid)

    # 将当前客户端 清理其房间
    for room in rooms:
        sio.leave_room(sid, room)











