from django.conf.urls import url

from oauth import views

urlpatterns = [

    # 获取qq登录的url地址
    url(r'^qq/authorization/$', views.QQURLView.as_view()),

    # qq认证接口
    url(r'^qq/user/$', views.QQUserView.as_view()),
]