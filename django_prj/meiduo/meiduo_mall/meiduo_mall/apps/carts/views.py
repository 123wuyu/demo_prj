import base64
import pickle

from django.shortcuts import render
from django_redis import get_redis_connection
from redis.client import StrictRedis
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.serializers import CartSerializer, CartSKUSerializer, CartDeleteSerializer, CartSelectAllSerializer
from goods.models import SKU


class CartView(APIView):

    # 重写父类的认证的方法
    def perform_authentication(self, request):
        """
        drf框架在视图执行前会调用此方法进行身份认证(jwt认证)
        如果认证不通过,则会抛异常返回401状态码
        问题: 抛异常会导致视图无法执行
        解决: 捕获异常即可
        """
        try:  # jwt不正确会抛异常， 返回401状态码, 会导致get, post, delete等方法不执行
            super().perform_authentication(request)
        except Exception as e:
            print('perform_authentication', e)

    def post(self, request):

        """添加商品到购物车"""

        # 创建序列化器，校验请求参数是否合法
        s = CartSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        # 获取校验后的3个参数： sku_id, count, selected
        # sku_id = request.data.get('sku_id')
        # count = request.data.get('count')
        # selected = request.data.get('selected')

        sku_id = s.validated_data.get('sku_id')
        count = s.validated_data.get('count')
        selected = s.validated_data.get('selected')

        # 获取用户对象: AnnomousUser
        user = request.user

        # 判断是否已经登录
        if user.is_authenticated():  # 已登录
            # cart_1 = {1: 2, 2: 2}
            # cart_selected_1 = {1,  2}
            # 用户已登录，获取操作Redis的StrictRedis对象， Pileline
            strict_redis = get_redis_connection('carts')  # type: StrictRedis
            # 增加购物车商品数量
            strict_redis.hincrby('cart_%s' % user.id, sku_id, count)
            # 保存商品勾选状态
            if selected:
                strict_redis.sadd('cart_selected_%s' % user.id, sku_id)
            # 响应序列化数据
            return Response(s.data, status=status.HTTP_201_CREATED)
        # 未登录: 操作cookie
        else:
            # 1. 从cookie中获取购物车信息
            cart_cookie = request.COOKIES.get('cart')

            # 2. base64字符串 -> 字典
            #   cart = {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
            if cart_cookie is None:
                cart = {}
            else:
                cart = pickle.loads(base64.b64decode(cart_cookie.encode()))

            print('cookie', cart)

            # 3. 新增字典中对应的商品数量
            sku = cart.get(sku_id)
            if sku: # 新的数量 = 原有数量 + 新增数量
                count = sku.get('count') + count
            cart[sku_id] = {
                'count': count,
                'selected': selected
            }

            # 4. 字典 --> base64字符串
            cart_cookie = base64.b64encode(pickle.dumps(cart)).decode()

            # 5. 通过cookie保存购物车数据（base64字符串）: response.set_cookie()
            response = Response(s.data, status=201)
            response.set_cookie('cart', cart_cookie, 60*60*24*365)  # 有效期: 1年

            # 6. 响应序列化数据
            return response

    def get(self, request):
        """查询购物车中的商品"""

        # 获取用户对象
        user = request.user
        # 判断是否已经登录
        if user.is_authenticated():
            # cart_1 = {1: 2, 2: 2}
            # cart_selected_1 = {1,  2}
            # 用户已登录，获取操作Redis的StrictRedis对象
            strict_redis = get_redis_connection('carts')  # type: StrictRedis

            # 读取购物车的商品数据，得到一个字典
            cart_dict = strict_redis.hgetall('cart_%s' % user.id)  # 字典: bytes
            # 读取商品勾选状态，得到一个列表
            cart_selected_list = strict_redis.smembers('cart_selected_%s' % user.id)  # 列表: bytes
            cart = {}
            for sku_id, count in cart_dict.items():
                '''
                cart[1] = {
                    'count': 1,
                    'selected': True
                }
                '''
                cart[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_selected_list
                }
            # 拼接得到类似如下字典 ：
            # {1:{'count':2, 'selected':False}, 2:{'count':2, 'selected':False}}
        else: # 未登录
            # 从cookie中获取购物车信息
            cart = request.COOKIES.get('cart')

            # base64字符串 -> 字典: cookie_cart.keys()   -> [1,2]
            # {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
            if cart is None:
                cart = {}
            else:
                cart = pickle.loads(base64.b64decode(cart.encode()))
            print('cookie', cart)

        # 查询的所有的商品对象: SKU.objects.filter(id__in=[1,2])
        skus = SKU.objects.filter(id__in=cart.keys())
        # 给商品对象新增count和selected属性
        for sku in skus:
            sku.count = cart[sku.id].get('count')
            sku.selected = cart[sku.id].get('selected')

        # 序列化商品对象并响应数据
        s = CartSKUSerializer(instance=skus, many=True)
        return Response(s.data)


    def put(self, request):
        """修改购物车中的商品"""

        # 创建序列化器，校验请求参数是否合法
        s = CartSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        # 获取校验后的3个参数： sku_id, count, selected
        sku_id = s.validated_data.get('sku_id')
        count = s.validated_data.get('count')
        selected = s.validated_data.get('selected')

        # 获取用户对象: AnnomousUser
        user = request.user

        # 判断是否已经登录
        if user.is_authenticated():  # 已登录
            # cart_1 = {1: 2, 2: 2}
            # cart_selected_1 = {1,  2}  # set
            # 用户已登录，获取操作Redis的StrictRedis对象
            strict_redis = get_redis_connection('carts')  # type: StrictRedis
            pipeline = strict_redis.pipeline()
            # 修改商品数量
            pipeline.hset('cart_%s' % user.id, sku_id, count)
            # 修改商品的勾选状态
            if selected: # 往set中添加成员
                pipeline.sadd('cart_selected_%s' % user.id, sku_id)
            else:  # 从set中删除成员
                pipeline.srem('cart_selected_%s' % user.id, sku_id)
            pipeline.execute()

            # 响应序列化数据
            return Response(s.data)
        else: # 未登录
            # 1. 从cookie中获取购物车信息
            cart = request.COOKIES.get('cart')

            # 2. base64字符串 -> 字典
            #    {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
            if cart is None:
                cart = {}
            else:
                cart = pickle.loads(base64.b64decode(cart.encode()))

            # 3. 修改字典中对应的商品数量和选中状态
            cart[sku_id] = {
                'count': count,
                'selected': selected,
            }

            # 4. 字典 --> base64字符串
            cart_cookie = base64.b64encode(pickle.dumps(cart)).decode()

            # 5. 通过cookie保存购物车数据（base64字符串）: response.set_cookie()
            response = Response(s.data)
            response.set_cookie('cart', cart_cookie,  60 * 60 * 24 * 365)  # 有效期: 1年
            # 6. 响应序列化数据
            return response

    def delete(self, request):
        """删除购物车中的商品"""

        # 创建序列化器，校验sku_id是否合法
        s = CartDeleteSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        # 获取校验后的sku_id,
        sku_id = s.validated_data.get('sku_id')

        # 获取用户对象
        user = request.user

        # 判断是否已经登录
        if user.is_authenticated():
            # cart_1 = {1: 2, 2: 2}
            # cart_selected_1 = {1, 2}
            # 用户已登录，获取操作Redis的StrictRedis对象
            strict_redis = get_redis_connection('carts')  # type: StrictRedis
            # 删除商品  hdel cart_1 1
            strict_redis.hdel('cart_%s' % user.id, sku_id)
            # 删除商品勾选状态 srem cart_selected_1 1
            strict_redis.srem('cart_selected_%s' % user.id, sku_id)
            # 响应数据
            return Response(status=204)
        else:   # 未登录
            # 从cookie中获取购物车信息（base64字符串）
            cart = request.COOKIES.get('cart')

            # base64字符串 -> 字典
            # {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
            if cart is None:
                cart = {}
            else:
                cart = pickle.loads(base64.b64decode(cart.encode()))

            print('cookie',  cart)

            response = Response(status=204)

            # del cart_data[3]  删除字典中的键值时，需要判断key是否存在
            if sku_id in cart:
                # 如果商品在字典中，删除字典中对应的商品
                del cart[sku_id]
                # 字典  -> base64字符串
                cart_cookie = base64.b64encode(pickle.dumps(cart)).decode()
                # 5. 通过cookie保存购物车数据（base64字符串）: response.set_cookie()
                response.set_cookie('cart', cart_cookie, 60 * 60 * 24 * 365)  # 有效期: 1年


            # 6. 响应序列化数据
            return response


class CartSelectAllView(APIView):
    """
    购物车全选和全不选
    """
    def perform_authentication(self, request):
        """
        drf框架在视图执行前会调用此方法进行身份认证(jwt认证)
        如果认证不通过,则会抛异常返回401状态码
        问题: 抛异常会导致视图无法执行
        解决: 捕获异常即可
        """
        try:
            super().perform_authentication(request)
        except Exception:
            pass

    def put(self, request):
        """全选或全不选"""
        # selected = request.data.get('selected')

        # 创建序列化器，校验selected是否合法
        s = CartSelectAllSerializer(data=request.data)
        # 获取校验后的selected,
        s.is_valid(raise_exception=True)
        # 获取用户对象
        selected = s.validated_data.get('selected')

        user = request.user

        if user.is_authenticated():  #  断是否已经登录
            # cart_1 = {1: 2, 2: 2}
            # cart_selected_1 = {1, 2}
            # 用户已登录，获取操作Redis的StrictRedis对象
            strict_redis = get_redis_connection('carts')  # type: StrictRedis
            # 从redis的hash中取出用户所有的商品id： hkeys cart_1    (1, 2)
            sku_ids = strict_redis.hkeys('cart_%s' % user.id)
            if selected:
                # 如果全选，添加商品id到redis的：  		sadd cart_selected_1 1 2
                strict_redis.sadd('cart_selected_%s' % user.id, *sku_ids)
            else:
                # 如果全不选，则从set中删除所有商品id	srem cart_selected_1 1 2
                strict_redis.srem('cart_selected_%s' % user.id, *sku_ids)
                # 响应数据
            return Response({'message': 'OK'})
        else: # 未登录
            # 从cookie中获取购物车信息
            cart = request.COOKIES.get('cart')
            # 如果cookie不为空，则base64字符串 -> 字典
            if cart is not None:
                # {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
                cart = pickle.loads(base64.b64decode(cart.encode()))
                print('cookie', cart)

                # 遍历字典中所有商品，修改商品的选中状态
                for sku_id in cart:
                    cart[sku_id]['selected'] = selected

                # 字典 --> base64字符串
                cart_cookie = base64.b64encode(pickle.dumps(cart)).decode()

                # 通过cookie保存购物车数据（base64字符串）: response.set_cookie()
                response = Response({'message': 'ok'})
                response.set_cookie('cart', cart_cookie, 60 * 60 * 24 * 365)  # 有效期: 1年

                # 响应序列化数据
                return response


































