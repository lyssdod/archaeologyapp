from django.db import models
from djchoices import DjangoChoices, ChoiceItem

# generic Filter model with many FilterValues
class Filter(models.Model):
    class Type(DjangoChoices):
        integer = ChoiceItem(0)
        boolean = ChoiceItem(1)
        double = ChoiceItem(2)
        string = ChoiceItem(3)

    name = models.CharField(max_length = 64)
    data = models.ForeignKey('FilterValue', on_delete = models.CASCADE, null = True)
    group = models.ForeignKey('FilterGroup', on_delete = models.DO_NOTHING, null = True) # preserve entire group from deletion
    oftype = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

# combine filters into groups
class FilterGroup(models.Model):
    name = models.CharField(max_length = 32)
    data = models.ForeignKey(Filter, on_delete = models.CASCADE, null = True)

# FilterValue of a Filter, can have multiple types
class FilterValue(models.Model):
    instance = models.ForeignKey(Filter)
    boolean = models.BooleanField(default = False)
    integer = models.IntegerField(default = 0)
    double  = models.FloatField(default = 0.0)
    string  = models.TextField(max_length = 128)

# User model
class User(models.Model):
    email = models.EmailField(max_length = 128)
    nickname = models.CharField(max_length = 64)
    password = models.CharField(max_length = 64)

    # User can define custom Filters
    filters = models.ForeignKey(FilterGroup, on_delete = models.CASCADE)

    def __str__(self):
        return self.email

# Site photos
class Image(models.Model):
    image = models.ImageField(max_length = 128, upload_to = 'uploads/')

# archaeology Site
class Site(models.Model):
    name = models.CharField(max_length = 128)

    # it LOTS of Filters
    filters = models.ForeignKey(FilterGroup, on_delete = models.DO_NOTHING) # don't delete existing Filter when deleting the Site

    # someone has created it
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING) # don't delete User when deleting it's Site

    # it also has images
    images = models.ForeignKey(Image, on_delete = models.CASCADE) # wipe out all previously stored photos

    # aux data (serialized)
    data = models.CharField(max_length = 16384)

    def __str__(self):
        return self.name
