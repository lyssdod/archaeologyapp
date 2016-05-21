from .models import Filter, Image, UserFilter, Property, Site, ValueType
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models


class FilterForm(forms.Form):

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
            args  = {'required': False}

            # if this filter have children, use select for them
            if subs.count():
                args['widget']  = forms.Select()
                args['choices'] = [(s.id, s.name) for s in subs]

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

    def create_tab(self, *args, **kwargs):
        return [self.fields[f] for f in args]

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


        self.tablist = {"basictab": "Basic data", "description": "Description", "attachments": "Attachments", "references": "References"}

        self.basictab = self.create_tab('name', 'country', 'region', 'district', 'settlement')
        #self.desctab = [self.fields[]]
