from django.conf.urls import url, include

from . import views

urlpatterns = [

    url(r'^$',views.index,name='index'),
    url(r'^sing_up/$',views.sing_up,name='sing_up'),
    url(r'^log_in/$',views.log_in,name='log_in')
]
