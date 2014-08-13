from django.conf.urls import patterns, url

from website import views

urlpatterns = patterns('',
    (r'^$', views.list),
    (r'^add/$', views.add_place),
)
