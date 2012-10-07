from django.conf.urls import patterns, include, url
from poscore.views import TowerListView, TowerDetailView

urlpatterns = patterns('',
    url(r'^tower/$', TowerListView.as_view(), name='tower-list'),
    url(r'^tower/(?P<pk>\d+)/$', TowerDetailView.as_view(), name='tower-detail'),
)