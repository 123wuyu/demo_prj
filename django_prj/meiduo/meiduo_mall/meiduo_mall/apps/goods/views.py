from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from goods.models import GoodsCategory, SKU
from goods.serializers import ChannelSerializer, CategorySerializer, SKUSerializer, SKUIndexSerializer


class CategoryView(GenericAPIView):
    """
    商品列表页面包屑导航
    """
    queryset = GoodsCategory.objects.all()

    # GET /categories/1/
    def get(self, request, pk=None):
        ret = {
            'cat1': '',
            'cat2': '',
            'cat3': '',
        }
        category = self.get_object()
        if category.parent is None:
            # 当前类别为一级类别
            # 通过 频道 查询 类别：  category.goodschannel_set.all()[0]
            ret['cat1'] = ChannelSerializer(category.goodschannel_set.all()[0]).data
        elif category.goodscategory_set.count() == 0:
            # 当前类别为三级
            ret['cat3'] = CategorySerializer(category).data
            cat2 = category.parent
            ret['cat2'] = CategorySerializer(cat2).data
            ret['cat1'] = ChannelSerializer(
            	cat2.parent.goodschannel_set.all()[0]).data
        else:
            # 当前类别为二级
            ret['cat2'] = CategorySerializer(category).data
            ret['cat1'] = ChannelSerializer(
            	category.parent.goodschannel_set.all()[0]).data
        return Response(ret)


class SKUListView(ListAPIView):

    queryset = SKU.objects.all()
    serializer_class = SKUSerializer

    # 需要指定排序和过滤的管理类
    # OrderingFilter : drf框架的类
    # DjangoFilterBackend : django_filters第三方的类
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    # 指定可以根据哪此字段进行排序
    ordering_fields = ('create_time', 'price', 'sales')
    # 指定可以根据哪些字段进行列表数据的过滤
    filter_fields = ('category_id',)


# http://api.meiduo.site:8000/departments/
# http://api.meiduo.site:8000/departments/1/

# http://api.meiduo.site:8000/skus/search/?text=wifi
# http://api.meiduo.site:8000/skus/search/          查多条数据
# http://api.meiduo.site:8000/skus/search/1/        查一条数据

class SKUSearchViewSet(HaystackViewSet):
    """HaystackViewSet: 搜索一条数据, 搜索多条数据"""

    # 关联的模型类
    index_models = [SKU]
    serializer_class = SKUIndexSerializer

























