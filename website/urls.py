from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from website import views

urlpatterns = patterns('',
    (r'^$', login_required(views.PlaceListView.as_view())),
    (r'^add/$', views.place_add),
    (r'^edit/(.+)/$', views.place_edit),
)
