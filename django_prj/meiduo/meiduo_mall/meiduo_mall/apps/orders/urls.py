from django.conf.urls import url

from orders import views

urlpatterns = [

    # 确认订单
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view()),
    # 保存订单
    url(r'^orders/$', views.SaveOrderView.as_view()),
]