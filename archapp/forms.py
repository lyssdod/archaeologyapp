from .models import Filter, Image, UserFilter, Property, Site, ValueType, ImageType
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from form_utils import forms as betterforms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_file_form.forms import FileFormMixin, UploadedFileField, MultipleUploadedFileField



class FilterForm(betterforms.BetterForm):
    def __init__(self, *args, **kwargs):
        #self.selected = kwargs['selected'] if 'selected' in kwargs else None
        super(FilterForm, self).__init__(*args, **kwargs)

    # creates fields for basic filters
    def create_filter_fields(self, query = {'basic': True}):
        filters = Filter.objects.filter(**query)
        mapping = { ValueType.integer : forms.IntegerField(),
                    ValueType.string  : forms.CharField(),
                    ValueType.double  : forms.FloatField(),
                    ValueType.boolean : forms.BooleanField()
                  }

        for flt in filters:
            field = None
            subs  = self.getsubdata(flt)
            args  = {'required': False, 'label': _(flt.name)}

            # if this filter have children, use select for them
            if subs.count():
                args['widget']  = forms.Select()
                args['choices'] = [(s.id, _(s.name)) for s in subs]
                #args['initial'] = self.selected[flt] if self.selected is not None else subs[0].id

                field = forms.ChoiceField()

            # render plain field otherwise
            else:
                if flt.hidden:
                    args['widget'] = forms.widgets.HiddenInput()

                field = mapping[flt.oftype]

            # implicit reconstruction with needed params
            f = type(field)(**args) 
            self.fields[flt.name.lower()] = type(field)(**args)


    # get child filters
    def getsubdata(self, obj):
        return obj.subfilters.all().exclude(pk = models.F('parent'))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name'] 
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ListSearchForm(FilterForm):

    def __init__(self, *args, **kwargs):
        super(ListSearchForm, self).__init__(*args, **kwargs)

        self.create_filter_fields()

class SearchForm(FilterForm):

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.create_filter_fields()



class NewSiteForm(FileFormMixin, FilterForm):

    class Meta:
        fieldsets = [('1', {'description': _('Basic data'), 'legend': 'maintab', 'fields':
                    ['name', 'country', 'region', 'district', 'settlement', 'latitude', 'longtitude','placeid']}),
                     ('2', {'description': _('Description'), 'legend': 'desctab', 'fields':
                    ['riversystem', 'area', 'areawidth', 'areaheight', 'topography', 'geomorphology', 'altitude', 'valleyaltitude', 'datingfrom', 'datingto', 'dating', 'undefined']}),
                     ('3', {'description': _('Attachments'), 'legend': 'mediatab', 'fields': ['general', 'plane', 'photo', 'found'] + ['form_id', 'upload_url', 'delete_url']}),
                     ('4', {'description': _('References'), 'legend': 'refstab', 'fields': ['literature']})]

    def __init__(self, *args, **kwargs):
        super(NewSiteForm, self).__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(max_length = 128)
        self.fields['undefined'] = forms.BooleanField(required = False, label = _('Dating is undefined'))
        self.fields['literature'] = forms.CharField(required = False, widget=forms.Textarea, max_length = 2048, label = _('Literature'))
        self.create_filter_fields()

        # create image fields
        for i, choice in ImageType.choices:
            field = None

            # limit site profile picture to one
            if i == ImageType.general:
                field = UploadedFileField(required = False, label = _(choice))
            else:
                field = MultipleUploadedFileField(required = False, label = _(choice))
            self.fields[choice.lower()] = field

#class EditForm(#forms.ModelForm): #FileFormMixin, FilterForm):

class EditForm(NewSiteForm):
    #class Meta:
    #    model = Site
    #    fields = ['name']
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['site_id'] = forms.IntegerField()
        self.fields['imgs_to_del'] = forms.CharField()
        #self.create_filter_fields()
