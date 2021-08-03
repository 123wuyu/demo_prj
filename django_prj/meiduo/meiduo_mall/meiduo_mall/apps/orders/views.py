from django.shortcuts import render

from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from orders.serializers import CartSKUSerializer2, SaveOrderSerializer


class OrderSettlementView(APIView):

    """订单结算"""
    permission_classes = [IsAuthenticated]

    # url: /orders/settlement/
    def get(self, request):
        """ 获取订单商品信息 """
        # 获取当前用户对象
        user = request.user
        # 获取操作redis数据库的StrictRedis对象
        redis_conn = get_redis_connection('carts')
        # 获取购物车数据（字典）： cart_1 = {1：2， 2：2}
        redis_cart = redis_conn.hgetall('cart_%s' % user.id)
        # 获取购物车商品选中状态（列表）： cart_selected_1 = {1, 2}
        cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)

        # 过滤出勾选的商品字典数据： {1：2, 2: 2}
        cart = {}
        for sku_id in cart_selected:
            cart[int(sku_id)] = int(redis_cart[sku_id])

        # 查询商品信息
        skus = SKU.objects.filter(id__in=cart.keys())
        # 给每一个商品sku对象补充上 count 数量
        for sku in skus:
            sku.count = cart[sku.id]

        # 手动响应的字典数据
        context = {
            'freight': 10.0,     # 运费
            'skus': CartSKUSerializer2(skus, many=True).data
        }
        # 响应数据
        return Response(context)


class SaveOrderView(CreateAPIView):
    """保存订单"""
    permission_classes = [IsAuthenticated]
    serializer_class = SaveOrderSerializer