

from rest_framework.response import Response
from rest_framework.views import exception_handler

import logging
logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    # 调用DRF的函数处理异常，如果处理成功，会返回一个`Response`类型的对象
    response = exception_handler(exc, context)

    if response is None:
        # response为None表示项目运行出错了，但DRF框架没有处理，
        # 则我们可以自己处理异常： 获取异常信息并保存到日志文件中，并响应出错信息
        view = context['view']     # 出错视图
        error = '服务器内部错误： %s，%s' % (view, exc)

        logger.error(error)  # 保存出错信息到日志文件中

        return Response({'message': error}, status=500)

    return response

