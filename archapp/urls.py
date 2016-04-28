from django.conf.urls import url

from . import views

app_name='archapp'
urlpatterns = [
        url(r'^$', views.welcomePage, name='welcome'),
        url(r'^new/$', views.newSite, name='newsite'),
#        url(r'^(?P<pk>[0-9]+)/$', views.sitePage.as_view(), name='sitepage'),
        url(r'^(?P<site_id>[0-9]+)/edit/$', views.siteEdit, name='edit'),
        url(r'^(?P<site_id>[0-9]+)/delete/$', views.siteDelete, name='delete'),
        url(r'^all/$', views.allSites, name='all'),
        url(r'^sites/p/$', views.publicQueries, name='publq'),
        url(r'^search/$', views.search, name='sresults'),
        url(r'^login/$', views.login, name='login'),
        ]
