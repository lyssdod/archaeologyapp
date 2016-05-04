from django.forms import ModelForm, CharField 
from .models import Filter, UserFilter, Property, Site 
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

class NewSiteForm(ModelForm):
    class Meta:
        model = Site
        fields = ['name']

#class PropertiesForm(ModelForm):
#    model = Property
#    fields = ['__all__']

#class FilterForm(ProperitesForm):
#    model = Filter 
