from django.conf.urls import url, include

from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^index/$',RedirectView.as_view(url='^$')),
    url(r'^$',views.index,name='index'),
    url(r'^sing_up/$',views.sing_up,name='sing_up'),
    url(r'^log_in/$',views.log_in,name='log_in'),
    url(r'^log_out/$',views.log_out,name='log_out'),
    url(r'^profile/(?P<id>\d+)/$', views.profile,name='profile'),
    url(r'^add_product/$',views.add_product,name='profile')
]
