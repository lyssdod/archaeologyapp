from .models import Filter, UserFilter, Property, Site, ValueType
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Site

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

#class NewSiteForm(forms.Form):
#    name = forms.CharField(max_length = 128)
#    image = forms.ImageField(max_length = 128)

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
