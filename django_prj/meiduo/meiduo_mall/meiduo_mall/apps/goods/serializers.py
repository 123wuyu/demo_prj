from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers

from goods.models import GoodsCategory, GoodsChannel, SKU


# 列表页导航使用到的序列化器
from goods.search_indexes import SKUIndex


class CategorySerializer(serializers.ModelSerializer):
    """ 类别序列化器 """
    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')


# 列表页导航使用到的序列化器
class ChannelSerializer(serializers.ModelSerializer):
    """ 频道序列化器 """
    category = CategorySerializer()

    class Meta:
        model = GoodsChannel
        fields = ('category', 'url')


# 商品列表数据显示序列化器
class SKUSerializer(serializers.ModelSerializer):
    """序列化器序输出商品SKU信息"""

    class Meta:
        model = SKU
        # 输出：序列化的字段
        fields = ('id', 'name', 'price', 'default_image_url', 'comments')


class SKUIndexSerializer(HaystackSerializer):
    """商品搜索的序列化器"""

    class Meta:
        # 关联的索引类
        index_classes = [SKUIndex]
        # 索引类中的字段
        fields = [
            "text", "id", "name", "price", "default_image_url","comments"
        ]