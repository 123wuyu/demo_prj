from django.shortcuts import render
from rest_framework import mixins
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin, RetrieveCacheResponseMixin

from areas.models import Area
from areas.serializers import AreaSerializer, SubAreaSerializer
from users.serializers import UserAddressSerializer


class AreaProvinceView(ListCacheResponseMixin, ListAPIView):                # 查询所有的省份
    queryset = Area.objects.filter(parent=None)     # 所有的省份
    serializer_class = AreaSerializer

    # 禁用分页功能
    pagination_class = None


class SubAreaView(RetrieveCacheResponseMixin, RetrieveAPIView):              # 查询一个区域（城市和区县）
    queryset = Area.objects.all()
    serializer_class = SubAreaSerializer


class AddressViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):

    """ 用户地址管理
    1. 用户地址的增删改查处理
    2. 设置默认地址: put
    3. 设置地址标题: put
    """
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """会调用此方法新增一个用户地址"""

        count = request.user.addresses.count()
        if count >= 10:  # 每个用户最多不能超过2个地址
            return Response({'message': '地址个数已达到上限'}, status=400)

        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """ 用户地址列表数据 """
        queryset = self.get_queryset()  # 当前登录用户的所有地址
        serializer = self.get_serializer(queryset, many=True)  # serializer.data 列表
        return Response({
            'user_id': request.user.id,
            'default_address_id': request.user.default_address_id,
            'limit': 10,
            'addresses': serializer.data
        })

    # query_set = Address.objects.all()
    # query_set = Address.objects.filter(user=self.request.user, is_deleted=False)

    def get_queryset(self):
        # 获取当前登录用户的地址
        # return Address.objects.filter(user=self.request.user, is_deleted=False)
        return self.request.user.addresses.filter(is_deleted=False)