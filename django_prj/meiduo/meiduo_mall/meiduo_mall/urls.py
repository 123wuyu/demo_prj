"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'xadmin/', include(xadmin.site.urls)),         # 第三方的xadmin


    url(r'^ckeditor/', include('ckeditor_uploader.urls')),          # 第三方富文本编辑器的路由配置

    url(r'^', include('meiduo_mall.apps.users.urls')),
    url(r'^', include('meiduo_mall.apps.verifications.urls')),
    url(r'^', include('meiduo_mall.apps.areas.urls')),
    url(r'^', include('meiduo_mall.apps.goods.urls')),          # 商品
    url(r'^', include('meiduo_mall.apps.contents.urls')),       # 首页广告
    url(r'^', include('meiduo_mall.apps.carts.urls')),          # 购物车
    url(r'^', include('meiduo_mall.apps.orders.urls')),         # 购物车
    url(r'^', include('meiduo_mall.apps.payment.urls')),        # 支付应用
    url(r'^oauth/', include('meiduo_mall.apps.oauth.urls')),
]









