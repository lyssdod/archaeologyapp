from .models import Site, Filter, Image, Property, ValueType
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from .forms import NewSiteForm, SignUpForm, SearchForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
import pickle

class WelcomePage(TemplateView):
    template_name = 'archapp/welcome.html'
#    x = Site.objects.get(name='Lynove')
#    print(x.props.all()[0])

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
    success_url='/archapp/all'
    login_url = '/archapp/accounts/login/'
    redirect_field_name= 'redirect_to'
        
    def form_valid(self, form):
        user = self.request.user
        name = form.cleaned_data['name']
        newsite = Site(name = name, user = user)
        # ?
        newsite.data = [{'settlement': form.cleaned_data['settlement']}, {'heigth': form.cleaned_data['height']}, {'width': form.cleaned_data['width']} , {'calculated area': form.cleaned_data['calculated_area']} , {'undefined_date': form.cleaned_data['height']} , {'heigth': form.cleaned_data['height']}] 
        newsite.save()
        filters = Filter.objects.filter(basic = True)

        for instance in filters:
            prop = None
            data = form.cleaned_data[instance.name.lower()]

            double = 0.0
            string = ''
            boolean = False
            integer = 0

            if instance.oftype == ValueType.integer:
                integer = int(data)
            elif instance.oftype == ValueType.boolean:
                boolean = bool(data)
            elif instance.oftype == ValueType.double:
                double = float(data)
            elif instance.oftype == ValueType.string:
                string = data

            # search for string values first
            if instance.oftype == ValueType.string:
                try:
                    prop = Property.objects.get(instance = instance, string = string)
                except Property.DoesNotExist:
                    prop = Property.objects.create(instance = instance, string = string)
            else:
                prop = Property.objects.create(instance = instance, integer = integer, boolean = boolean, double = double, string = string)

            newsite.props.add(prop)

        general = Image.objects.create(site = newsite, oftype = Image.Type.general, image = form.cleaned_data['general'])
        plane = Image.objects.create(site = newsite,   oftype = Image.Type.plane,   image = form.cleaned_data['plane'])
        photo = Image.objects.create(site = newsite,   oftype = Image.Type.photo,   image = form.cleaned_data['photo'])
        found = Image.objects.create(site = newsite,   oftype = Image.Type.found,   image = form.cleaned_data['found'])

        return super(NewSite, self).form_valid(form)


class SitePage(DetailView):
    model = Site
    template_name = 'archapp/site.html'

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

