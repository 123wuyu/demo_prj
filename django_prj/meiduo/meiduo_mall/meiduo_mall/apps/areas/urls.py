from django.conf.urls import url

from areas import views

urlpatterns = [

    # 获取所有的省份
    url(r'^areas/$', views.AreaProvinceView.as_view()),
    # 获取城市或区县(查询一条区域数据)
    url(r'^areas/(?P<pk>\d+)/$', views.SubAreaView.as_view()),


]
