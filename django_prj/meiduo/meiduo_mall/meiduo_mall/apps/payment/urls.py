from django.conf.urls import url

from payment import views

urlpatterns = [

    # 支付接口
    url(r'^orders/(?P<order_id>\d+)/payment/$', views.PaymentView.as_view()),
    # 处理支付结果接口
    url(r'^payment/status/$', views.PaymentStatusView.as_view()),
]