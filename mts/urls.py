from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #(r'^static/(?P<path>.*)$','django.views.static.serve',),
    # url(r'^$', 'mts.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #(r'^admin/', include(admin.site.urls)),
    (r'^website/', include('website.urls')),
    (r'^account/', include('account.urls')),
)
