from django.conf.urls import url

from carts import views

urlpatterns = [

    # 购物车增删改查
    url(r'^cart/$', views.CartView.as_view()),
    # 全选与全不选
    url(r'^cart/selection/$', views.CartSelectAllView.as_view()),

]


