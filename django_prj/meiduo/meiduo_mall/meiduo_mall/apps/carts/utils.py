import base64
import pickle

from django_redis import get_redis_connection
from redis import StrictRedis


def merge_cart_cookie_to_redis(request,  response,  user):
    """
    合并cookie中的购物车数据到redis中
    :param request: 请求对象, 用于获取cookie
    :param response: 响应对象,用于清除cookie
    :param user: 登录用户, 用于获取用户id
    :return:
    """
    # 1. 获取cookie数据(base64字符串)
    cart_cookie = request.COOKIES.get('cart')

    # 2. 如果cookie数据为空，则return返回值无需合并购物车数据
    if not cart_cookie:
        return response

    # 3. base64字符串 --> 字典
    # {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
    cart = pickle.loads(base64.b64decode(cart_cookie.encode()))

    # 4. 获取操作Redis数据库的StrictRedis对象
    strict_redis = get_redis_connection('carts')  # type: StrictRedis

    # 5. 遍历字典，获取: sku_id, count, selected
    for sku_id, count_selected_dict in cart.items():
        count = count_selected_dict.get('count')
        selected = count_selected_dict.get('selected')

        # 合并操作：以cookie中的商品数量覆盖redis中的数量
        strict_redis.hset('cart_%s' % user.id, sku_id, count)

        # 修改商品勾选状态：操作redis的集合，添加或删除商品id
        if selected:
            strict_redis.sadd('cart_selected_%s' % user.id, sku_id)
        else:
            strict_redis.srem('cart_selected_%s' % user.id, sku_id)

    # 6. 清除cookie数据
    response.delete_cookie('cart')

    # 7. 返回响应
    return response

























