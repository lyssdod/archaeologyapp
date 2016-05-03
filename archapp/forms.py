from django.forms import ModelForm, CharField, PasswordInput
from .models import Filter, UserFilter, Property, Site 
from django.contrib.auth.models import User

class SignUpForm(ModelForm):
#    password = CharField(widget=PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name'] 

class NewSiteForm(ModelForm):
    class Meta:
        model = Site
        fields = ['name']

#class PropertiesForm(ModelForm):
#    model = Property
#    fields = ['__all__']

#class FilterForm(ProperitesForm):
#    model = Filter 
