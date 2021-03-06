from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from itsdangerous import TimedJSONWebSignatureSerializer

from meiduo_mall.utils.models import BaseModel


class User(AbstractUser):

    """用户模型类"""
    # mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    # 新增字段： 保存用户的默认地址
    default_address = models.ForeignKey('Address', related_name='users',
                                        null=True, blank=True, on_delete=models.SET_NULL,
                                        verbose_name='默认地址')

    def generate_verify_email_url(self):
        """生成激活邮箱的链接
        返回值: http://www.meiduo.site:8080/success_verify_email.html?token=xxx
        token包含两个参数: user_id=10&email=xxx@163.com
        """
        s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 60*60*24)  # 一天有效期
        token = s.dumps({'user_id': self.id, 'email': self.email}).decode()
        return 'http://www.meiduo.site:8080/success_verify_email.html?token='+ token


    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


# users/models.py
class Address(BaseModel):
    """
    用户收件地址表
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')

    # 应用名.类名
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT,
                                 related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT,
                             related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT,
                                 related_name='district_addresses', verbose_name='区')

    place = models.CharField(max_length=50, verbose_name='详细地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True,
                           default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True,
                             default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    # is_default = models.BooleanField(default=False, verbose_name='默认地址')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']  # 查询地址列表数据时的排序





















