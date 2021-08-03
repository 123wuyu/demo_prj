from rest_framework import serializers

from goods.models import SKU


class CartSerializer(serializers.Serializer):

    """
    购物车数据序列化器
    """
    sku_id = serializers.IntegerField(label='sku id ', min_value=1)
    count = serializers.IntegerField(label='数量', min_value=1)
    selected = serializers.BooleanField(label='是否勾选', default=True)

    def validate(self, attrs):  # attrs: 字典类型
        try:
            sku = SKU.objects.get(id=attrs.get('sku_id'))
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return attrs


class CartSKUSerializer(serializers.ModelSerializer):
    """
    购物车商品数据显示序列化器
    """
    count = serializers.IntegerField(label='数量')
    selected = serializers.BooleanField(label='是否勾选')

    class Meta:
        model = SKU
        fields = ('id', 'name', 'default_image_url', 'price', 'count', 'selected')


class CartDeleteSerializer(serializers.Serializer):
    """
    删除购物车数据序列化器
    """
    sku_id = serializers.IntegerField(label='商品id', min_value=1)

    def validate_sku_id(self, value):
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return value


class CartSelectAllSerializer(serializers.Serializer):
    """
    购物车全选
    """
    selected = serializers.BooleanField(label='全选')








