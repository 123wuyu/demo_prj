from django_redis import get_redis_connection
from redis.client import StrictRedis
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from oauth.models import OAuthQQUser
from oauth.utils import check_encrypted_openid
from users.models import User


class QQUserSerializer(Serializer):
    """
    绑定openid和美多用户的序列化器
    作用: 校验四个请求参数, 没有用到序列化功能

    # 1. 获取请求参数: mobile, password, sms_code, openid
	# 2. 校验openid是否合法
	# 3. 校验短信验证码是否正确
	# 4. 判断要绑定的用户是否存在
	# 	- 用户不存在，则以手机号作为用户名，创建美多用户
	# 	- 用户存在，判断密码是否正确
	5. 绑定openid和美多用户（往映射表添加一条数据）
	  create() : 绑定逻辑实现
    """

    openid = serializers.CharField(label='openid', write_only=True)
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$', write_only=True)
    password = serializers.CharField(label='密码', max_length=20, min_length=8, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)

    def validate(self, attrs):
        # 1. 获取请求参数: mobile, password, sms_code, openid
        openid = attrs.get('openid')  # header.payload.singure
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        sms_code = attrs.get('sms_code')

        # 2. 校验openid是否合法
        openid = check_encrypted_openid(openid)  # 结果: 明文的字符串
        if openid is None:
            raise ValidationError({'message': 'openid不合法'})

        # 修改字典中的Openid为明文的openid
        attrs['openid'] = openid

        # 3. 校验短信验证码是否正确
        # todo: 校验短信验证码
        # 获取正确的短信验证码
        # strict_redis = get_redis_connection('sms_codes') # type: StrictRedis
        # real_sms_code = strict_redis.get('sms_%s' % mobile)  # bytes
        # if not real_sms_code:
        #     raise ValidationError({'message':'短信验证码无效'})
        # # 比较是否相等
        # if real_sms_code.decode() != sms_code:
        #     raise ValidationError({'message':'短信验证码不正确'})

        # 4. 判断要绑定的用户是否存在
        # 获取要绑定的美多用户
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 要绑定的美多用户不存在，则以手机号作为用户名，创建美多用户
            user = User.objects.create_user(username=mobile,
                                     mobile=mobile,
                                     password=password)
        else:
            # 要绑定的美多用户存在，判断密码是否正确
            if not user.check_password(password):
                raise ValidationError({'message':'要绑定用户的密码不正确'})

        # 往字典中新增一个属性, 以便后续绑定openid时使用
        attrs['user'] = user

        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')

        # 5. 绑定openid和美多用户（往映射表添加一条数据）
        qquser = OAuthQQUser.objects.create(
            openid=validated_data.get('openid'),
            user=user
        )
        return user  # 返回绑定的美多用户对象






















































