from time import sleep

from django.shortcuts import render
from django_redis import get_redis_connection
from redis.client import StrictRedis
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import logging

from celery_tasks.sms.tasks import send_sms_code
from meiduo_mall.libs.yuntongxun.sms import CCP

logger = logging.getLogger('django')


class SmsCodeView(APIView):
    # 发送短信验证码

    # /sms_codes/(?P<mobile>1[3-9]\d{9})/
    def get(self, request, mobile):

        # 4. 判断是否重复发送短信验证码
        strict_redis = get_redis_connection('sms_codes')  # type: StrictRedis
        send_flag = strict_redis.get('sms_flag_%s' % mobile)
        if send_flag:
            # return Response({'message': '禁止重复发送短信验证码'}, status=400)
            raise ValidationError({'message': '禁止重复发送短信验证码'})  # status=400

        # 1. 生成短信验证码   001234
        import random
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info('获取短信验证码: %s' % sms_code)

        # 2. 使用云通讯来发送短信验证码
        # [sms_code, 5]  [短信验证码， 有效期]   1表示id为1的短信测试模板，项目上线换成自己的模板id
        # print(CCP().send_template_sms(mobile, [sms_code, 5], 1))
        # sleep(5)

        # 使用delay发送短信: 保存函数名,函数参数,任务标识等redis中
        # send_sms_code(mobile, sms_code)
        send_sms_code.delay(mobile, sms_code)

        # 3. 保存短信验证码
        # sms_13600000001        111111      （验证码：5分钟过期）
        # sms_13600000002        222222      （验证码：5分钟过期）
        # send_flag_13600000001       1      （发送标识：1分钟过期）
        # send_flag_13600000002       1      （发送标识：1分钟过期）
        # strict_redis.setex('sms_%s' % mobile, 60*5, sms_code)
        # strict_redis.setex('sms_flag_%s' % mobile, 60, 1)
        pipeline = strict_redis.pipeline()
        pipeline.setex('sms_%s' % mobile, 60*5, sms_code)
        pipeline.setex('sms_flag_%s' % mobile, 60, 1)
        result = pipeline.execute()
        print(result)

        # 5. 响应数据
        return Response({'message': 'OK'})



























