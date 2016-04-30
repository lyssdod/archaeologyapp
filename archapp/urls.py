from django.conf.urls import url

from . import views

app_name='archapp'
urlpatterns = [
        url(r'^$', views.WelcomePage.as_view(), name='welcome'),
        url(r'^new/$', views.NewSite.as_view(), name='newsite'),
        url(r'^(?P<pk>[0-9]+)/$', views.SitePage.as_view(), name='sitepage'),
        url(r'^(?P<pk>[0-9]+)/edit/$', views.SiteEdit.as_view(), name='edit'),
        url(r'^(?P<pk>[0-9]+)/delete/$', views.SiteDelete.as_view(), name='delete'),
        url(r'^all/$', views.AllSites.as_view(), name='all'),
#        url(r'^sites/p/$', views.PublicQueries.as_view(), name='publq'),
        url(r'^search/$', views.Search.as_view(), name='sresults'),
        url(r'^login/$', views.Login.as_view(), name='login'),
        ]
