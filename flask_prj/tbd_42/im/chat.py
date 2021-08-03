from server import sio
import time


# @sio.on('connect')
# def on_connect(sid, environ):
#     """
#     与客户端建立好连接后被执行
#     :param sid: string sid是socketio为当前连接客户端生成的识别id
#     :param environ: dict 在连接握手时客户端发送的握手数据(HTTP报文解析之后的字典)
#     """
#     # 向客户端推送一条问候消息数据
#     # 与前端约定的数据格式
#     # {
#     #     "msg": 聊天内容,
#     #     "timestamp":  发送的时间戳
#     # }
#
#     msg_data = {
#         "msg": "hello",
#         "timestmap": round(time.time() * 1000)
#     }
#
#     sio.emit('message', msg_data, room=sid)
#     # sio.send(msg_data, room=sid)


@sio.on('message')
def on_message(sid, data):
    """
    聊天的事件处理，message事件 是我们自定的与前端达成的约定
    :param sid:
    :param data: 是客户端传来的数据
    :return:
    """
    # data
    # {
    #     "msg": 聊天内容,
    #     "timestamp":  发送的时间戳
    # }

    # 客户端发送的聊天内容
    msg = data.get('msg')

    # TODO 通过rpc调用聊天机器人子系统 获取回复内容

    resp_msg = {
        "msg": 'I have received your msg: {}'.format(msg),
        "timestamp": round(time.time() * 1000)
    }
    # sio.emit('message', resp_msg, room=sid)
    sio.send(resp_msg, room=sid)

