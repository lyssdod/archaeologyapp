from .models import Site, Filter, Property
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from .forms import NewSiteForm, SignUpForm, SearchForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

class WelcomePage(TemplateView):
    template_name = 'archapp/welcome.html'
    #x = Site.objects.get(name='Pobeda')
    #print(x.props.all())

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'archapp/signup.html'
    success_url='/archapp/accounts/login'
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

class NewSite(LoginRequiredMixin, FormView):
    template_name = 'archapp/newsite.html'
    form_class = NewSiteForm
    #form_class = SearchForm
    success_url='/archapp/all'
    login_url = '/archapp/accounts/login/'
    redirect_field_name= 'redirect_to'
        
    def form_valid(self, form):
        name = form.cleaned_data['name']
        user = self.request.user
        newsite = Site(name = name, user = user)
        newsite.save()

        filters = ['Country', 'Region', 'District', 'Area', 'Altitude']
        for e in filters:
            instance = Filter.objects.get(name=e)
            data = e.lower()
            x = form.cleaned_data['%s' %  data] 
            if type(x) is str:
                oftype = 4
                string = x
                try:
                    prop = Property.objects.get(string = string)
                    newsite.props.add(prop)
                except Property.DoesNotExist:
                    prop = Property.objects.create(instance=instance, 
                            oftype=oftype, 
                            string=string)
                    newsite.props.add(prop)
            elif type(x) is int:
                oftype = 1
                integer = x
                try:
                    prop = Property.objects.get(integer = integer)
                    newsite.props.add(prop)
                except Property.DoesNotExist:
                    prop = Property.objects.create(instance=instance, 
                            oftype=oftype, 
                            integer=integer)
                    newsite.props.add(prop)

            elif type(x) is bool:
                oftype = 2
                boolean = x
                try:
                    prop = Property.objects.get(boolean = boolean)
                    newsite.props.add(prop)
                except Property.DoesNotExist:
                    prop = Property.objects.create(instance=instance, 
                            oftype=oftype, 
                            boolean=boolean)
                    newsite.props.add(prop)

            elif type(x) is float:
                oftype = 3
                double = x
                try:
                    prop = Property.objects.get(double = double)
                    newsite.props.add(prop)
                except Property.DoesNotExist:
                    prop = Property.objects.create(instance=instance, 
                            oftype=oftype, 
                            double=double)
                    newsite.props.add(prop)


                #flds = ['country', 'region', 'district']
        #for e in flds:
        #    e = form.cleaned_data['%s' % e]

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

class AllSites(LoginRequiredMixin, ListView):
    model = Site
    form_class = SearchForm
    template_name = 'archapp/all.html'
    success_url='/archapp/'
    login_url = '/archapp/accounts/login/'

    def form_valid(self, form):
        return super(SearchForm, self).form_valid(form)
#class PublicQueries(TemplateView):
#    template_name = 'archapp/all.html'


class Search(ListView):
    model = Site
    template_name = 'archapp/search.html'

