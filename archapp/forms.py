from .models import Filter, UserFilter, Property, Site, ValueType
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Site
from django.db import models

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

class SearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        filters = ['Country', 'Region', 'District', 'Area', 'Topography', 'Altitude', 'ValleyAltitude', 'Geomorphology', 'Dating']
        for name in filters:
            flt = Filter.objects.get(name = name)
            fld = None
            print(flt.oftype)
            if flt.oftype == 1:
                fld = forms.IntegerField()
            elif flt.oftype == 4:
                #fld = forms.ChoiceField(('Please select', -1))
                fld = forms.CharField()
            elif flt.oftype == 3:
                fld = forms.FloatField()

            self.fields[name.lower()] = fld

    def getsubdata(self, key):
        if type(key) is int:
            return Filter.objects.filter(subfilters__pk = key)
        else:
            return Filter.objects.filter(subfilters__name = key)

class NewSiteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(NewSiteForm, self).__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(max_length = 128)
        self.fields['image'] = forms.ImageField(max_length = 128)

        filters = Filter.objects.all()
        for flt in filters:
            fld = None
            if flt.oftype == 1:
                fld = forms.IntegerField()
            elif flt.oftype == 4:
                fld = forms.CharField()
            elif flt.oftype == 3:
                fld = forms.FloatField()

            self.fields[flt.name.lower()] = fld

    def getsubdata(self, key):
        if type(key) is int:
            return Filter.objects.filter(subfilters__pk = key)
        else:
            return Filter.objects.filter(subfilters__name = key)

#class PropertiesForm(ModelForm):
#    model = Property
#    fields = ['__all__']

#class FilterForm(ProperitesForm):
#    model = Filter 
