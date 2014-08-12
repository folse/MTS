from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mts.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #(r'^admin/', include(admin.site.urls)),
    #(r'^/', include('website.urls')),
    (r'^account/', include('account.urls')),
)
