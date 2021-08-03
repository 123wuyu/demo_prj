from time import sleep

from celery_tasks.main import celery_app
from celery_tasks.sms.yuntongxun.sms import CCP


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """发送短信验证码"""
    # print(CCP().send_template_sms(mobile, [sms_code, 5], 1))
    print('发送短信验证码: ', sms_code)
    sleep(5)
    return sms_code