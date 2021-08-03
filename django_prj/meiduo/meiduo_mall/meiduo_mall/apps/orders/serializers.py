from time import sleep

from django.db import transaction
from django.utils.timezone import now
from django_redis import get_redis_connection
from redis.client import StrictRedis
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods



class CartSKUSerializer2(serializers.ModelSerializer):
    """
    购物车商品数据序列化器
    """
    count = serializers.IntegerField(label='数量')

    class Meta:
        model = SKU
        fields = ('id', 'name', 'default_image_url', 'price', 'count')


class SaveOrderSerializer(ModelSerializer):
    """保存订单序列化器"""

    def create(self, validated_data):
        """保存一个订单"""

        # 获取下单用户及请求参数: 地址，支付方式
        user = self.context.get('request').user
        address = validated_data.get('address')
        pay_method = validated_data.get('pay_method')

        # 生成订单编号 20180704174607000000001  now(): datetime类型
        order_id = now().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)

        with transaction.atomic():  # 开启一个事务
            save_id = transaction.savepoint()     # 创建一个保存点
            try:
                # 订单信息表: 保存订单基本信息（新增一条订单数据）
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    address=address,
                    pay_method=pay_method,
                    user=user,
                    total_count=0,
                    total_amount=0,
                    freight=10,  # 运费
                    # 三元表达式: a if xxx else b
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']  # 未支付: 待付款
                    if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY']
                    else OrderInfo.ORDER_STATUS_ENUM['UNSEND']  # 货到付款：待发货
                )

                # 从Redis中查询购物车商品
                # cart_1 = {1: 2, 2: 2}
                # cart_selected_1 = {1, 2}
                strict_redis = get_redis_connection('carts')  # type: StrictRedis
                cart_dict = strict_redis.hgetall('cart_%s' % user.id)  # {1: 2, 2: 2}  bytes
                selected_sku_ids = strict_redis.smembers('cart_selected_%s' % user.id)  # [1, 2]  bytes

                # 过滤出勾选的商品id和数量，得到字典：{1: 2, 2: 2}  int
                cart = {}  # {1: 2, 2: 2}
                for sku_id in cart_dict:
                    if sku_id in selected_sku_ids:
                        cart[int(sku_id)] = int(cart_dict.get(sku_id))
                print('buy goods', cart)

                # 遍历勾选的商品id
                for sku_id in cart:
                    while True:
                        # 查询sku对象
                        sku = SKU.objects.get(id=sku_id)
                        # sku = SKU.objects.select_for_update().get(id=sku_id)  # 方式1: 悲观锁

                        # 记录原始的库存和销量
                        origin_stock = sku.stock
                        origin_sales = sku.sales

                        # 判断库存
                        sku_count = cart.get(sku_id)  # 要购买的数量
                        if sku_count > sku.stock:
                            raise ValidationError('库存不足')  # ok
                            # return Response('库存不足', status=400)   # error

                        # sleep(5)

                        # 修改sku表： 减少库存，增加销量
                        # sku.stock -= sku_count
                        # sku.sales += sku_count
                        # sku.save()  # 修改商品sku表的字段

                        # 方式2: 使用乐观锁修改库存和销量
                        new_stock = origin_stock - sku_count
                        new_sales = origin_sales + sku_count
                        count = SKU.objects.filter(id=sku.id, stock=origin_stock) \
                            .update(stock=new_stock, sales=new_sales)

                        if count == 0:  # 表示当前用户库存修改失败, 因为有其他用户并发下单,修改了库存
                            # 处理: 重新查询、判断、修改商品库存, 直到成功或因库存不足退出
                            print('---重新查询、判断、修改商品库存--', origin_stock)
                            continue

                        # 修改spu表： 修改SPU销量 sales
                        sku.goods.sales += sku_count
                        sku.goods.save()

                        # 订单商品表: 保存订单商品信息（新增多条数据）
                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            price=sku.price,
                            count=sku_count)

                        # 累加订单商品总数量和总金额
                        order.total_count += sku_count
                        order.total_amount += sku.price * sku_count  # 一个商品的小计金额: 单价*数量

                        # 表示一个订单商品保存成功, 需要跳出while死循环， 继续保存下一个订单商品
                        break

                # 修改订单信息表: 总数量和总金额
                order.total_amount += order.freight  # 运费为: 10
                order.save()

            except Exception as e:
                print(e)
                # 回滚事务
                transaction.savepoint_rollback(save_id)
                raise e

            # 提交事务
            transaction.savepoint_commit(save_id)

            # 清除购物车中已结算的商品
            strict_redis.hdel('cart_%s' % user.id, *selected_sku_ids)
            strict_redis.srem('cart_selected_%s' % user.id, *selected_sku_ids)

            # 返回新创建的订单对象 order
            return order

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'address', 'pay_method')

        read_only_fields = ('order_id',)  # 默认为可读可写
        extra_kwargs = {
            'address': {
                'write_only': True,
                'required': True,
            },
            'pay_method': {
                'write_only': True,
                'required': True
            }
        }

