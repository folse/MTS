from django.conf.urls import patterns, url

from website import views

urlpatterns = patterns('',
    (r'^$', views.place_list),
    (r'^add/$', views.place_add),
)
