from django.db import models
from picklefield import fields
from djchoices import DjangoChoices, ChoiceItem
from django.contrib.auth.models import User

# all possible Property value types
class ValueType(DjangoChoices):
    #enum    = ChoiceItem(0, "Enum")
    integer = ChoiceItem(1, "Integer")
    boolean = ChoiceItem(2, "Boolean")
    double = ChoiceItem(3, "Double")
    string = ChoiceItem(4, "String")

# generic Filter for Property referencing
class Filter(models.Model):
    name = models.CharField(max_length = 128)
    basic = models.BooleanField(default = False)
    parent = models.ForeignKey('self', null = True, blank = True, related_name = 'subfilters')
    oftype = models.IntegerField(default = 0, verbose_name = "Value type", choices = ValueType.choices)

    def __str__(self):
        return self.name

# User-defined Filter
class UserFilter(Filter):
    query = fields.PickledObjectField()
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

# Property of a Site
class Property(models.Model):
    class Meta:
        verbose_name_plural = "properties"

    instance = models.ForeignKey(Filter, verbose_name = "Related filter", on_delete = models.CASCADE)
    # kind of overkill here
    oftype = models.IntegerField(default = 0, verbose_name = "Value type", choices = ValueType.choices)


    boolean = models.BooleanField(default = False, verbose_name = "Boolean value")
    integer = models.IntegerField(default = 0, verbose_name = "Integer value")
    double = models.FloatField(default = 0.0, verbose_name = "Float value")
    string = models.TextField(max_length = 128, blank = True, verbose_name = "String value")


    def __str__(self):
        if self.oftype == ValueType.integer:
            return str(self.integer)
        elif self.oftype == ValueType.boolean:
            return str(self.boolean)
        elif self.oftype == ValueType.double:
            return str(self.double)
        elif self.oftype == ValueType.string:
            return self.string

# archaeology Site
class Site(models.Model):
    name = models.CharField(max_length = 128)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    props = models.ManyToManyField(Property)
    data = fields.PickledObjectField()

    def __str__(self):
        return self.name

# Site photos
class Image(models.Model):
    class Type:
        general = 1
        plane = 2
        photo = 3
        found = 4

    site = models.ForeignKey(Site, on_delete = models.CASCADE)
    image = models.ImageField(max_length = 128, upload_to = 'uploads/')
    oftype = models.IntegerField(default = 0)
