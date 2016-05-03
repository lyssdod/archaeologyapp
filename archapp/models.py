from django.db import models
from picklefield import fields
from djchoices import DjangoChoices, ChoiceItem
from django.contrib.auth.models import User

# generic Filter for Property referencing
class Filter(models.Model):
    name = models.CharField(max_length = 128)

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

    class Type(DjangoChoices):
        integer = ChoiceItem(0, "Integer")
        boolean = ChoiceItem(1, "Boolean")
        double = ChoiceItem(2, "Double")
        string = ChoiceItem(3, "String")

    instance = models.ForeignKey(Filter, verbose_name = "Related filter", on_delete = models.CASCADE)
    boolean = models.BooleanField(default = False, verbose_name = "Boolean value")
    integer = models.IntegerField(default = 0, verbose_name = "Integer value")
    double = models.FloatField(default = 0.0, verbose_name = "Float value")
    string = models.TextField(max_length = 128, blank = True, verbose_name = "String value")

    oftype = models.IntegerField(default = 0, verbose_name = "Value type", choices = Type.choices)
    linked = models.BooleanField(default = False, verbose_name = "Use as a subfilter")
    # for example, we have a subfiltered property. In that case, this field
    # will be used to link some site's propery to this subfilter and avoid
    # property duplication
    usedby = models.IntegerField(default = None)

    def __str__(self):
        if self.oftype == Property.Type.integer:
            return str(self.integer)
        elif self.oftype == Property.Type.boolean:
            return str(self.boolean)
        elif self.oftype == Property.Type.double:
            return str(self.double)
        elif self.oftype == Property.Type.string:
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
