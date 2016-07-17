from archapp.models import Site, Filter, Image, Property, ValueType, ImageType
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from archapp.forms import NewSiteForm, SignUpForm, ListSearchForm, EditSiteForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from hvad.utils import get_translation_aware_manager
from django.core.urlresolvers import reverse
from django.utils import translation
from django.conf import settings
from archapp.geo import GeoCoder
import pickle


class SiteProcessingView(object):
    # update or create new filter values
    def process_filters_and_pics(self, site, form, editing = False):
        geo = GeoCoder(GeoCoder.Type.google)
        values = form.cleaned_data
        filters = Filter.objects.filter(basic = True)

        for instance in filters:
            prop = None
            args = {'instance': instance}
            name = instance.name.lower()
            data = values[name]

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
                            geocoded = geo.reverse(values['latitude'], values['longtitude'], lang, name)
                            geocoded = geocoded or translation.ugettext('Unknown') # maybe try another provider here?

                        # let's search for it
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

                    try:
                        prop.save()
                    except: # translation already exists
                        pass

            # process other property types
            else:
                if editing:
                    pass
                else:
                    prop = Property.objects.create(**args)

                # save to database
                if editing:
                    site.props.filter(instance = instance).update(**args)
                else:
                    site.props.add(prop)

        # attach images
        for i, choice in ImageType.choices:
            img = choice.lower()
            pic = values[img]

            if pic is not None:
                if i == ImageType.general:
                    # make array from single picture
                    pic = [pic]

                for each in pic:
                    tmp = Image.objects.create(site = site, oftype = i, image = each)
                    tmp.save()

        # delete data from temp_uploads
        form.delete_temporary_files()

        if editing:
            imgs_del_data = form.cleaned_data['imgs_to_del']
            trash_images = imgs_del_data.split(',')
            for img_id in trash_images:
                img_id = int(img_id)
                try:
                    img_to_delete = site_to_update.image_set.all().get(id=img_id)
                    img_to_delete.delete()
                except:
                    pass

class SiteCreate(LoginRequiredMixin, FormView, SiteProcessingView):
    template_name = 'archapp/newsite.html'
    form_class = NewSiteForm
    success_url='/archapp/all'
    login_url = '/archapp/accounts/login/'
    redirect_field_name= 'redirect_to'

    def form_valid(self, form):
        siteuser = self.request.user
        sitename = form.cleaned_data['name']
        newsite = Site(name = sitename, user = siteuser)
        newsite.save()

        # process all filters and images
        self.process_filters_and_pics(site = newsite, form = form, editing = False)

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

class SiteEdit(LoginRequiredMixin, FormMixin, DetailView, SiteProcessingView):
    manager = get_translation_aware_manager(Site)
    queryset = manager.language()
    form_class = EditSiteForm
    model = Site
    template_name = 'archapp/edit.html'
    login_url = '/archapp/accounts/login/'
    redirect_field_name= 'redirect_to'

    def get_success_url(self):
        return reverse('allsites')

    def get_context_data(self, **kwargs):
        context = super(SiteEdit, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # obtain current site
        site = Site.objects.get(pk = form.cleaned_data['site_id'], user = self.request.user)

        # update its name
        site.name = form.cleaned_data['name']

        # save
        site.save()

        # update all filters and images
        self.process_filters_and_pics(site = site, form = form, editing = True)


        site.data[0]['Bibliography'] = form.cleaned_data['literature']
        site.save()

        return super(SiteEdit, self).form_valid(form)

class SiteDelete(LoginRequiredMixin, DeleteView):
    model = Site
    success_url = '/archapp/all/' 
    template_name = 'archapp/delete.html'


class AllSites(LoginRequiredMixin, ListView):
    model = Site
    template_name = 'archapp/all.html'
    success_url='/archapp/'
    login_url = '/archapp/accounts/login/'

    def form_valid(self, form):
        queryset = super(AllSites, self).form_valid(form)

        # Handle specific fields of the custom ListForm
        # Others are automatically handled by FilteredListView.

        #if form.cleaned_data['is_active'] == 'yes':
        #    queryset = queryset.filter(is_active=True)

        return queryset

    # render form explicitly
    def get_context_data(self, **kwargs):
        context= super(AllSites, self).get_context_data(**kwargs)
        context['form'] = ListSearchForm
        return context

class Search(LoginRequiredMixin, ListView):
    model = Site
    template_name = 'archapp/search.html'



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
