from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.welcomePage, name='Welcome'),
        url(r'^new/$', views.newSite, name='New Site'),
        url(r'^(?P<site_id>[0-9]+)/$', views.sitePage, name='Site Page'),
        url(r'^(?P<site_id>[0-9]+)/edit/$', views.siteEdit, name='Edit Page'),
        url(r'^(?P<site_id>[0-9]+)/delete/$', views.siteDelete, name='Delete Page'),
        url(r'^all/$', views.allSites, name='All Sites'),
        url(r'^sites/p/$', views.publicQueries, name='Public Queries'),
        url(r'^search/$', views.search, name='Search Results'),

        ]
