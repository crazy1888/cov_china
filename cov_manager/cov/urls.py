from django.conf.urls import url, include
from .views import index,main,hello,time_get,get_c1,get_c2,get_r1,get_r2,get_l1,get_l2

urlpatterns = [
    url(r'^index/$', index),
    url(r'^test_ajax/$',hello),
    url(r'^$',main), #默认打开主页面
    url(r'^time/$',time_get),
    url(r'^c1/$', get_c1),
    url(r'^c2/$',get_c2),
    url(r'^r1/$',get_r1),
    url(r'^l1/$',get_l1),
    url(r'^r2/$',get_r2),
    url(r'^l2/$',get_l2),
]
