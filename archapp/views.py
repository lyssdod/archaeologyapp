from .models import Site, Filter, Image, Property, ValueType, ImageType
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from .forms import NewSiteForm, SignUpForm, SearchForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
import pickle

class WelcomePage(TemplateView):
    template_name = 'archapp/welcome.html'

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'archapp/signup.html'
    success_url='/archapp/accounts/login'
    def form_valid(self, form):
        return super(SignUp, self).form_valid(form)

class UserUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'archapp/userupdate.html'
    model = User
    slug_field = "username"
    fields = ['username']

class UserDelete(LoginRequiredMixin, DeleteView):
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
        newsite.save()
        filters = Filter.objects.filter(basic = True)

        for instance in filters:
            prop = None
            args = {'instance': instance}
            data = form.cleaned_data[instance.name.lower()]
            print('filter: {}, data: {}'.format(instance.name, data))

            # usually this means validation fail, but
            # let's override this for missing fields
            if data is None:
                data = False

            if instance.oftype == ValueType.integer:
                args['integer'] = int(data)
            elif instance.oftype == ValueType.boolean:
                args['boolean'] = bool(data)
            elif instance.oftype == ValueType.double:
                args['double'] = float(data)
            elif instance.oftype == ValueType.string:
                args['string'] = data

            # search for string values first
            if instance.oftype == ValueType.string:
                try:
                    prop = Property.objects.get(instance = instance, string = args['string'])
                except Property.DoesNotExist:
                    prop = Property.objects.create(instance = instance, string = args['string'])
            else:
                prop = Property.objects.create(**args)

            newsite.props.add(prop)

        images = [ImageType.general, ImageType.plane, ImageType.photo, ImageType.found]

        for img in images:
            if str(img).lower() in form.cleaned_data:
                tmp = Image.objects.create(site = newsite, oftype = img, image = form.cleaned_data[str(img).lower()])

        newsite.data = [{'Bibliography': form.cleaned_data['literature']}]
        newsite.save()
        print (newsite.data)

        return super(NewSite, self).form_valid(form)


class SitePage(LoginRequiredMixin, DetailView):
    model = Site
    template_name = 'archapp/site.html'
    def get_context_data(self, **kwargs):
        context = super(SitePage, self).get_context_data(**kwargs)
        context['title'] = "Site Page" 
        return context

class SiteEdit(LoginRequiredMixin, UpdateView):
    model = Site
    fields = ['name']
    template_name = 'archapp/edit.html'

class SiteDelete(LoginRequiredMixin, DeleteView):
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


class Search(LoginRequiredMixin, ListView):
    model = Site
    template_name = 'archapp/search.html'

