from .models import Filter, Image, UserFilter, Property, Site, ValueType, ImageType
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from form_utils import forms as betterforms
from django.db import models
from django.utils.translation import ugettext_lazy as _

class FilterForm(betterforms.BetterForm):

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

                field = forms.ChoiceField()

            # render plain field otherwise
            else:
                if flt.hidden:
                    args['widget'] = forms.widgets.HiddenInput()

                field = mapping[flt.oftype]

            # implicit reconstruction with needed params
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

class SearchForm(FilterForm):

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.create_filter_fields()


class NewSiteForm(FilterForm):

    class Meta:
        fieldsets = [('1', {'description': _('Basic data'), 'legend': 'maintab', 'fields':
                    ['name', 'country', 'region', 'district', 'settlement']}),
                     ('2', {'description': _('Description'), 'legend': 'desctab', 'fields':
                    ['area', 'areawidth', 'areaheight', 'calculated_area', 'topography', 'geomorphology', 'altitude', 'valleyaltitude', 'datingfrom', 'datingto', 'dating', 'undefined']}),
                     ('3', {'description': _('Attachments'), 'legend': 'mediatab', 'fields': ['general', 'plane', 'photo', 'found']}),
                     ('4', {'description': _('References'), 'legend': 'refstab', 'fields': ['literature']})]

    def __init__(self, *args, **kwargs):
        super(NewSiteForm, self).__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(max_length = 128)
        self.fields['calculated_area'] = forms.IntegerField(required=False, label = _('Calculated area'))
        self.fields['undefined'] = forms.BooleanField(required = False, label = _('Dating is undefined'))
        self.fields['literature'] = forms.CharField(required=False, 
                widget=forms.Textarea, max_length = 512)
        self.create_filter_fields()

        self.fields['general'] = forms.ImageField(required=False, max_length = 128)
        self.fields['plane'] = forms.ImageField(required=False, max_length = 128)
        self.fields['photo'] = forms.ImageField(required=False, max_length = 128)
        self.fields['found'] = forms.ImageField(required=False, max_length = 128)

