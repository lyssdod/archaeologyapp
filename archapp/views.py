from .models import Site, Filter, Image, Property, ValueType, ImageType
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from .forms import NewSiteForm, SignUpForm, SearchForm, EditForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader
from django.contrib.auth.mixins import LoginRequiredMixin
from hvad.utils import get_translation_aware_manager
from django.utils import translation
from django.conf import settings
from .geo import GeoCoder
import pickle
from .populatedb import Populate_from_xlsx, sheet  

# error handlers
def error404(request):
    print ('handler 404!')
    template = loader.get_template('archapp/error.html')
    context = Context({
        'message': 'All: %s' % request,
        })

    return HttpResponse(content = template.render(context), content_type = 'text/html; charset=utf-8', status = 404)

def error500(request):
    template = loader.get_template('archapp/error.html')
    context = Context({
        'message': 'All: %s' % request,
        })

    return HttpResponse(content = template.render(context), content_type = 'text/html; charset=utf-8', status = 500)

class WelcomePage(TemplateView):
    template_name = 'archapp/welcome.html'
    model = Site
    ### Uncomment to populate database with sites from excel
    #print(Populate_from_xlsx(sheet))

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
        geo = GeoCoder(GeoCoder.Type.google)
        siteuser = self.request.user
        sitename = form.cleaned_data['name']
        newsite = Site(name = sitename, user = siteuser)
        filters = Filter.objects.filter(basic = True)
        newsite.save()

        for instance in filters:
            prop = None
            args = {'instance': instance}
            name = instance.name.lower()
            data = form.cleaned_data[name]

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
                # let's remember missing translations...
                missing = []

                # we want these values to be explicitly translated
                if name in geo.filters():
                    for lang, etc in settings.LANGUAGES:
                        # try to get geo data in specified language
                        with translation.override(lang):
                            geocoded = geo.reverse(form.cleaned_data['latitude'], form.cleaned_data['longtitude'], lang, name)
                            geocoded = geocoded or translation.ugettext('Unknown') # maybe try another provider here?

                        #let's search for it
                        try:
                            prop = Property.objects.language(lang).get(instance = instance, string = geocoded)
                        except Property.DoesNotExist:
                            missing.append( (lang, geocoded) )
                else:
                    # for plain string properties just copy provided text to all translations
                    missing = [(code, args['string']) for code, full in settings.LANGUAGES]

                # if no translations available, create property without translation
                if prop is None:
                    prop = Property.objects.create(instance = instance)
                    prop.save(update_fields = ['instance'])

                # finally fill missing translations
                for lang, translated in missing:
                    prop.translate(lang)
                    prop.string = translated
                    prop.save()

            # create other property types
            else:
                prop = Property.objects.create(**args)

            # add this property to the site
            newsite.props.add(prop)

        # attach images
        for i, choice in ImageType.choices:
            img = choice.lower()
            pic = form.cleaned_data[img]

            if pic is not None:
                if i == ImageType.general:
                    # make array from single picture
                    pic = [pic]

                for each in pic:
                    tmp = Image.objects.create(site = newsite, oftype = i, image = each)
                    tmp.save()

        # delete data from temp_uploads
        form.delete_temporary_files()

        newsite.data = [{'Bibliography': form.cleaned_data['literature']}]
        newsite.save()

        return super(NewSite, self).form_valid(form)
    

class SitePage(LoginRequiredMixin, DetailView):
    manager = get_translation_aware_manager(Site)
    queryset = manager.language()
    template_name = 'archapp/site.html'
    
    def get_context_data(self, **kwargs):
          context = super(SitePage, self).get_context_data(**kwargs)
          context['sview'] = True
          return context

class SiteEdit(LoginRequiredMixin, DetailView):
    manager = get_translation_aware_manager(Site)
    queryset = manager.language()
    template_name = 'archapp/edit.html'

    def get_context_data(self, **kwargs):
        context= super(SiteEdit, self).get_context_data(**kwargs)
        context['form'] = EditForm 
        return context

class NewEdit(LoginRequiredMixin, UpdateView):
    model = Site
    manager = get_translation_aware_manager(Site)
    queryset = manager.language()
    form_class = EditForm
    template_name = 'archapp/edit.html'

class SiteEditForm(LoginRequiredMixin, FormView):
    form_class = EditForm
    success_url='/archapp/all'
    login_url = '/archapp/accounts/login/'
    redirect_field_name= 'redirect_to'
    
    def form_valid(self, form):
        geo = GeoCoder(GeoCoder.Type.google)
        siteuser = self.request.user
        site_id = form.cleaned_data['site_id']
        site_to_update = Site.objects.get(pk=site_id, user=siteuser)
        filters = Filter.objects.filter(basic = True)
        site_to_update.name = form.cleaned_data['name']
        site_to_update.save()
        for instance in filters:
            prop = None
            args = {'instance': instance}
            name = instance.name.lower()
            data = form.cleaned_data[name]

            # usually this means validation fail, but
            # let's override this for missing fields
            if data is None:
                data = False

            if instance.oftype == ValueType.integer:
               # args['integer'] = int(data)
               # return ValueError: invalid literal for int() with base 10: ''
               pass
            elif instance.oftype == ValueType.boolean:
                args['boolean'] = bool(data)
            elif instance.oftype == ValueType.double:
                args['double'] = float(data)
            elif instance.oftype == ValueType.string:
                args['string'] = data

            # search for string values first
            if instance.oftype == ValueType.string:
                # let's remember missing translations...
                missing = []

                # we want these values to be explicitly translated
                if name in geo.filters():
                    for lang, etc in settings.LANGUAGES:
                        # try to get geo data in specified language
                        with translation.override(lang):
                            geocoded = geo.reverse(form.cleaned_data['latitude'], form.cleaned_data['longtitude'], lang, name)
                            geocoded = geocoded or translation.ugettext('Unknown') # maybe try another provider here?

                        #let's search for it
                        try:
                            prop = Property.objects.language(lang).get(instance = instance, string = geocoded)
                        except Property.DoesNotExist:
                            missing.append( (lang, geocoded) )
                else:
                    # for plain string properties just copy provided text to all translations
                    missing = [(code, args['string']) for code, full in settings.LANGUAGES]

                # if no translations available, create property without translation
                if prop is None:
                    prop = Property.objects.create(instance = instance)
                    prop.save(update_fields = ['instance'])

                # finally fill missing translations
                for lang, translated in missing:
                    prop.translate(lang)
                    prop.string = translated
                    prop.save()

            # create other property types
            else:
                prop = Property.objects.create(**args)

            # add this property to the site
            print(prop)
            old_prop = site_to_update.props.all().get(instance=instance)
            site_to_update.props.remove(old_prop)
            site_to_update.props.add(prop)

        # attach images
        for i, choice in ImageType.choices:
            img = choice.lower()
            pic = form.cleaned_data[img]

            if pic is not None:
                if i == ImageType.general:
                    # make array from single picture
                    pic = [pic]

                for each in pic:
                    tmp = Image.objects.create(site = site_to_update, oftype = i, image = each)
                    tmp.save()

        # delete data from temp_uploads
        form.delete_temporary_files()

        # delete unnecessary images
        imgs_del_data = form.cleaned_data['imgs_to_del']
        print(imgs_del_data)
        trash_images = imgs_del_data.split(',')
        for img_id in trash_images:
            img_id = int(img_id)
            try:
                img_to_delete = site_to_update.image_set.all().get(id=img_id)
                img_to_delete.delete()
            except:
                pass

        site_to_update.data[0]['Bibliography'] = form.cleaned_data['literature']
        
        site_to_update.save()

        return super(SiteEditForm, self).form_valid(form)

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



