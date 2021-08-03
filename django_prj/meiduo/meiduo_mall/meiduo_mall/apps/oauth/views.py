from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.utils import merge_cart_cookie_to_redis
from oauth.models import OAuthQQUser
from oauth.serializers import QQUserSerializer
from oauth.utils import generate_encrypted_openid


class QQURLView(APIView):

    # /oauth/qq/authorization/?next=xxx
    def get(self, request):
        # 获取QQ登录界面的url地址

        # next = request.GET.get()
        next = request.query_params.get('next')

        # 创建第三方sdk OAuthQQ对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)  # 登录成功进入的界面地址，比如： /index.html

        # QQ登录界面的url地址
        login_url = oauth.get_qq_url()

        return Response({
            'login_url':login_url
        })


class QQUserView(APIView):

    # GET /oauth/qq/user/?code=xxx
    def get(self, request):
        """QQ认证接口"""

        # 1. 获取请求参数：code
        # code = request.GET.get('code')
        code = request.query_params.get('code')
        # 2. 校验 code 参数
        if not code:
            return Response({'message': 'code不能为空'}, status=400)

        # 创建第三方sdk OAuthQQ对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)  # 登录成功进入的界面地址，比如： /index.html
        try:
            # 3. 使用QQ登录sdk， 通过 code 获取 access_token
            access_token = oauth.get_access_token(code)

            # 4. 使用QQ登录sdk， 通过 access_token 获取 openid
            openid = oauth.get_open_id(access_token)
        except:
            return Response({'message': 'QQ服务器出错'}, status=500)

        # 5. 根据openid，从映射表中查询绑定的美多用户对象
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # - 查询不到美多用户，说明是第一次使用QQ登录，则返回openid, 等待后续用户的绑定操作
            # 使用itdangerous签名openid后,再响应给客户端
            openid = generate_encrypted_openid(openid)
            return Response({'openid': openid})
        else:
            # - 能查询到美多用户，则生成并响应：jwt，user_id, username，完成QQ登录流程
            user = qquser.user     # 绑定openid绑定的美多用户对象

            # 生成jwt
            from rest_framework_jwt.settings import api_settings
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 生payload部分的方法(函数)
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 生成jwt的方法(函数)

            payload = jwt_payload_handler(user)  # 生成payload, 得到字典
            token = jwt_encode_handler(payload)  # 生成jwt字符串

            # 响应数据
            context = {
                'token': token,
                'user_id': user.id,
                'username': user.username
            }

            response = Response(context)
            # 合并购物车商品
            merge_cart_cookie_to_redis(request, response, user)
            return response

    # POST /oauth/qq/user/
    def post(self, request):

        # 1. 创建序列化器
        s = QQUserSerializer(data=request.data)
        # 2. 校验请求参数是否合法: serializer.is_valid()
        s.is_valid(raise_exception=True)
        # 3. 绑定openid与美多用户:  serializer.save()   -> serializer.create()
        user = s.save()   # 返回绑定的美多用户对象
        # 4. 生成并响应 jwt, user_id, username，完成QQ登录

        # 生成jwt
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 生payload部分的方法(函数)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 生成jwt的方法(函数)

        payload = jwt_payload_handler(user)  # 生成payload, 得到字典
        token = jwt_encode_handler(payload)  # 生成jwt字符串

        # 响应数据
        context = {
            'token': token,
            'user_id': user.id,
            'username': user.username
        }

        response = Response(context)
        # 合并购物车商品
        merge_cart_cookie_to_redis(request, response, user)
        return response




















