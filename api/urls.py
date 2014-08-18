from django.conf.urls import patterns, include
from django.contrib.auth.decorators import login_required
from api import views

urlpatterns = patterns('',
	(r'^add_place$', login_required(views.add_place)),
	(r'^login$', views.login),
)
