from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

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
        url(r'^signup/$', views.SignUp.as_view(), name='signup'),
        url(r'^accounts/login/$', auth_views.login, {'template_name': 'archapp/login.html'} , name='login'),
        url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'archapp/logout.html'} , name='logout'),
        url(r'user/(?P<slug>[\w.@+-]+)/$', views.UserUpdate.as_view(), name='user-update'),
        url(r'user/(?P<slug>[\w.@+-]+)/delete/$', views.UserDelete.as_view(), name='user-delete'),
        #url(r'^404/$', views.error404, ),
        ]

#handler404 = "views.error404"
#handler500 = "views.error500"
