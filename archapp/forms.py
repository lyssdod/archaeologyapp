from .models import Filter, UserFilter, Property, Site, ValueType
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

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

class NewSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name']

class SearchForm(forms.Form):
    filters = ['Country', 'Region', 'District', 'Area', 'AreaWidth', 'AreaHeight', 'Topography', 'Geomorphology', 'Dating']

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for name in filters:
            flt = Filter.objects.filter(name = name)
            fld = None

            if flt.oftype == models.ValueType.integer:
                fld = forms.IntegerField()
            elif flt.oftype == models.ValueType.string:
                fld = forms.ChoiceField(('Please select', -1))
            elif flt.oftype == models.ValueType.double:
                fld = forms.FloatField()

            self.fields[name.lower()] = fld

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
