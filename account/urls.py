from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
    (r'^login/$', views.login),
    (r'^register/$', 'account.views.register'),
    (r'^logout/$', 'django.contrib.auth.views.logout',{'next_page':'/'}),
)
