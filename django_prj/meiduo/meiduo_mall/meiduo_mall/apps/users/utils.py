from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义登录成功响应的数据,补充user_id和username
    """
    return {
        'user_id': user.id,
        'username': user.username,
        'token': token,
    }


class UsernameMobileAuthBackend(ModelBackend):
    """自定义的认证后台: 支持使用手机号登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        判断用户名(手机号)或者密码是否正确，返回对应的用户对象。
        username: 账号 或 手机号
        """
        query_set = User.objects.filter(Q(username=username) | Q(mobile=username))
        try:
            if query_set.exists():
                user = query_set.get()  # 取出唯一的一条数据（取不到或者有多条数据都会出错）
                if user.check_password(password):  # 进入一步判断密码是否正确
                    return user
        except:
            return None

