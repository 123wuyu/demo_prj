from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from goods import views
from goods.views import SKUSearchViewSet

urlpatterns = [

    # 列表界面导航接口
    url(r'^categories/(?P<pk>\d+)/$', views.CategoryView.as_view()),
    # 查询商品列表数据
    url(r'^skus/$', views.SKUListView.as_view()),

]

# http://api.meiduo.site:8000/skus/search/          查多条数据
# http://api.meiduo.site:8000/skus/search/1/        查一条数据

# 商品搜索的路由
router = DefaultRouter()
router.register("skus/search", SKUSearchViewSet, base_name="skus-search")
urlpatterns += router.urls