from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
    (r'^login/$', views.login),
    (r'^register/$', views.register),
    (r'^profile/$', 'account.views.profile'),
    (r'^logout/$', 'django.contrib.auth.views.logout',{'next_page':'/account/login'}),
)
