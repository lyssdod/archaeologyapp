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
        mapping = { ValueType.integer : forms.IntegerField(),
                    ValueType.string  : forms.CharField(),
                    ValueType.double  : forms.FloatField()
                  }

        for flt in filters:
            self.fields[flt.name.lower()] = mapping[flt.oftype]

    # get child filters
    def getsubdata(self, key):
        if type(key) is int:
            return Filter.objects.filter(subfilters__pk = key)
        else:
            return Filter.objects.filter(subfilters__name = key)

def render_form_field(fieldtype = None):
    if fieldtype == 'text':
        return forms.CharField()
    elif fieldtype == 'number':
        return forms.IntegerField()
    elif fieldtype == 'checkbox':
        return forms.BooleanField()

# pickled data
data = Site().data

# let's assume each data item is a following dict:
# item['name'] = 'Aux Field name 1', item['fielddtype'] = 'number'

class AuxForm(forms.Form):
    for item in data:
        setattr(this, item['name'], item['fieldtype'])

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

#class NewSiteForm(forms.ModelForm):
#    class Meta:
#        model = Site
#        fields = ['name']

class SearchForm(FilterForm):

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.create_filter_fields()


class NewSiteForm(FilterForm):

    def __init__(self, *args, **kwargs):
        super(NewSiteForm, self).__init__(*args, **kwargs)

        self.create_filter_fields()

        self.fields['name'] = forms.CharField(max_length = 128)
        self.fields['image'] = forms.ImageField(max_length = 128)
#class PropertiesForm(ModelForm):
#    model = Property
#    fields = ['__all__']

#class FilterForm(ProperitesForm):
#    model = Filter 
