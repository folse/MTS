from django.conf.urls import patterns, include
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.decorators import login_required
from website import views

urlpatterns = patterns('',
    # Examples:
    #(r'^static/(?P<path>.*)$','django.views.static.serve',),
    # url(r'^$', 'mts.views.home', name='home'),
    #(r'^admin/', include(admin.site.urls)),
    (r'^$', login_required(views.PlaceListView.as_view())),
    (r'^api/', include('api.urls')),
    (r'^website/', include('website.urls')),
    (r'^account/', include('account.urls')),
)
