from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),  # This line has changed!
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^to_wish_plans$', views.to_wish_plans),
    url(r'^to_add_wish_plan$', views.to_add_wish_plan),
    url(r'add_plan/(?P<id>\d+)$', views.add_plan),
    url(r'^to_dashboard$', views.to_dashboard),
    url(r'^join/(?P<id>\d+)/(?P<idt>\d+)$', views.join),
    url(r'^to_wish/(?P<idt>\d+)/(?P<id>\d+)$', views.to_wish),
    url(r'^logout$', views.logout),
    url(r'^remove/(?P<id>\d+)/(?P<idt>\d+)$', views.remove),
]