from django.forms import ModelForm, CharField 
from .models import Filter, UserFilter, Property, Site 
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

class NewSiteForm(forms.Form):
    name = forms.CharField(max_length = 128)
#    image = forms.ImageField(max_length = 128)

#class PropertiesForm(ModelForm):
#    model = Property
#    fields = ['__all__']

#class FilterForm(ProperitesForm):
#    model = Filter 
