from .models import Site
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from .forms import NewSiteForm, SignUpForm, SearchForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

class WelcomePage(TemplateView):
    template_name = 'archapp/welcome.html'
    
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

class NewSite(FormView):
    template_name = 'archapp/newsite.html'
    form_class = NewSiteForm
    success_url='/archapp/'
    def form_valid(self, form):
        name = form.cleaned_data['name']
        user = User.objects.get(pk=1)
        newsite = Site(name = name, user = user)
        newsite.save()
        return super(NewSite, self).form_valid(form)

    #def valid_form(NewSiteForm):
    #    if form.is_valid():
    #        name = form.cleaned_data['name']
    #    return HttpResponseRedirect('archapp/all.html')

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
    form_class = SearchForm
    template_name = 'archapp/all.html'

    def form_valid(self, form):
        return super(SearchForm, self).form_valid(form)
#class PublicQueries(TemplateView):
#    template_name = 'archapp/all.html'


class Search(ListView):
    model = Site
    template_name = 'archapp/search.html'

class Login(TemplateView):
    template_name = 'archapp/login.html'





