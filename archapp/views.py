from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.core.urlresolvers import reverse
from .models import Site
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .forms import NewSiteForm, SignUpForm
from django.contrib.auth.models import User

class WelcomePage(TemplateView):
    template_name = 'archapp/welcome.html'
    users = User.objects.all()
    print(users)
    
class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'archapp/signup.html'
    success_url='/archapp/'

    def form_valid(self, form):
        return super(SignUp, self).form_valid(form)

class UserUpdate(UpdateView):
    template_name = 'archapp/userupdate.html'
    model = User
    slug_field = "username"
    fields = ['username']

class UserDelete(DeleteView):
    model = User
    slug_field = "username"
    success_url = '/signup/'

class NewSite(CreateView):
    form_class = NewSiteForm
    template_name = 'archapp/newsite.html'

class SitePage(DetailView):
    model = Site
    template_name = 'archapp/site.html'
#
class SiteEdit(UpdateView):
    model = Site
    fields = ['name']
    template_name = 'archapp/edit.html'

class SiteDelete(DeleteView):
    model = Site
    success_url = '/archapp/all/' 
    template_name = 'archapp/delete.html'

class AllSites(ListView):
    model = Site
    template_name = 'archapp/all.html'

#class PublicQueries(TemplateView):
#    template_name = 'archapp/all.html'


class Search(ListView):
    model = Site
    template_name = 'archapp/search.html'

class Login(TemplateView):
    template_name = 'archapp/login.html'





