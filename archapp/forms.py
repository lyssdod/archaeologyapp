from .models import Filter, Image, UserFilter, Property, Site, ValueType
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Site, ValueType
from django.db import models

import pprint

class FilterForm(forms.Form):

    # creates fields for basic filters
    def create_filter_fields(self):
        filters = Filter.objects.filter(basic = True)
        mapping = { ValueType.integer : forms.IntegerField(required=False),
                    ValueType.string  : forms.CharField(required=False),
                    ValueType.double  : forms.FloatField(required=False)
                  }
        TOPOGRAPHY_TYPES = (
                ('Valley', 'Valley'),
                ('1st Terrace','1st Terrace'),
                ('2d Terrace', '2d Terrace'),
                ('High Terrace', 'High Terrace'),
                ('Riverbank', 'Riverbank')
                )
        GEOMORPHOLOGY_TYPES = (
                ('Dune', 'Dune'),
                ('Cape', 'Cape'),
                ('Plateau', 'Plateau')
                )
        for flt in filters:
            if flt.name == 'Topography':
                self.fields[flt.name.lower()] = forms.ChoiceField(
                    required=False,
                    widget=forms.Select,
                    choices=TOPOGRAPHY_TYPES, 
                    )
            elif flt.name == 'Geomorphology':
                self.fields[flt.name.lower()] = forms.ChoiceField(
                    required=False,
                    widget=forms.Select,
                    choices=GEOMORPHOLOGY_TYPES, 
                    )
            else:
                self.fields[flt.name.lower()] = mapping[flt.oftype]

    # get child filters
    def getsubdata(self, key):
        if type(key) is int:
            return Filter.objects.filter(subfilters__pk = key)
        else:
            return Filter.objects.filter(subfilters__name = key)

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

    def __init__(self, *args, **kwargs):
        super(NewSiteForm, self).__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(max_length = 128)
        self.fields['settlement'] = forms.CharField(max_length = 128, required = False)
        self.fields['height'] = forms.IntegerField(required=False)
        self.fields['width'] = forms.IntegerField(required=False)
        self.fields['calculated_area'] = forms.IntegerField(required=False, label = 'Calculated area')
        self.fields['undefined_date'] = forms.BooleanField(required = False, label = 'Undefined date')
        self.fields['literature'] = forms.CharField(required=False, 
                widget=forms.Textarea, max_length = 512)
        self.create_filter_fields()

        self.fields['general'] = forms.ImageField(required=False, max_length = 128)
        self.fields['plane'] = forms.ImageField(required=False, max_length = 128)
        self.fields['photo'] = forms.ImageField(required=False, max_length = 128)
        self.fields['found'] = forms.ImageField(required=False, max_length = 128)
