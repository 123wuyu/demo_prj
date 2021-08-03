from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from areas.views import AddressViewSet
from meiduo_mall.apps.users import views
# from users import views
from users.views import MyObtainJSONWebToken, BrowseHistoryView

urlpatterns = [

    url(r'^test/$', views.TestView.as_view()),
    url(r'^test2/$', views.TestView2.as_view()),

    # 注册用户
    url(r'^users/$', views.CreateUserView.as_view()),
    # 查询用户详情信息
    url(r'^user/$', views.UserDetailView.as_view()),
    # 修改用户(邮箱)
    url(r'^email/$', views.EmailView.as_view()),
    # 激活邮箱
    url(r'^email/verification/$', views.VerifyEmailView.as_view()),

    # 登录接口(djangorestframework-jwt使用第三方包的视图)
    # url(r'^login/', obtain_jwt_token),
    # url(r'^authorizations/', obtain_jwt_token),
    url(r'^authorizations/', MyObtainJSONWebToken.as_view()),

    # 判断用户名是否存在
    url(r'^usernames/(?P<username>\w{5,20})/count/$',
        views.UsernameCountView.as_view()),

    # 用户浏览历史记录 browse_histories
    url(r'^browse_histories/', BrowseHistoryView.as_view()),
]

# POST /addresses/
# GET  /addresses/

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, base_name='addresses')
urlpatterns += router.urls





















