# 导入g对象
from flask import g,request

from .jwt_util import verify_jwt
# 需求：在每次请求前校验用户身份
def jwt_authentication():
    """
    利用before_request请求钩子，在进入所有视图前先尝试判断用户身份
    :return:
    """
    # 此处利用鉴权机制（如cookie、session、jwt等）鉴别用户身份信息
    # if 已登录用户，用户有身份信息
    # g.user_id = 123
    # else 未登录用户，用户无身份信息
    g.user_id = None
    g.is_refresh = False
    # =====================================
    # 步骤：
    # 1.使用request对象，获取请求头中的Authorization
    auth = request.headers.get('Authorization')
    # 2.提取token值，切片
    if auth is not None and auth.startswith('Bearer '):
        # Bearer
        token = auth[7:]
        # 3.调用verify_jwt函数，校验token
        payload = verify_jwt(token)
        # 4.判断是否有payload
        if payload is not None:
            # 5.提取user_id
            g.user_id = payload.get("user_id")
            g.is_refresh = payload.get('is_refresh')
