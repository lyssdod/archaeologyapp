from django.db import models
from picklefield import fields
from djchoices import DjangoChoices, ChoiceItem
from django.contrib.auth.models import User

# all possible Property value types
class ValueType(DjangoChoices):
    integer = ChoiceItem(1, "Integer")
    boolean = ChoiceItem(2, "Boolean")
    double = ChoiceItem(3, "Double")
    string = ChoiceItem(4, "String")

class ImageType(DjangoChoices):
    general = ChoiceItem(1, "General")
    plane = ChoiceItem(2, "Plane")
    photo = ChoiceItem(3, "Photo")
    found = ChoiceItem(4, "Found")

# generic Filter for Property referencing
class Filter(models.Model):
    name = models.CharField(max_length = 128)
    basic = models.BooleanField(default = False)
    hidden = models.BooleanField(default = False)
    parent = models.ForeignKey('self', null = True, blank = True, related_name = 'subfilters')
    oftype = models.IntegerField(default = 1, verbose_name = "Value type", choices = ValueType.choices)

    def __str__(self):
        return self.name

# User-defined Filter
class UserFilter(Filter):
    title = models.TextField(max_length = 128, default = "User-defined filter")
    query = fields.PickledObjectField()
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

# Property of a Site
class Property(models.Model):
    class Meta:
        verbose_name_plural = "properties"

    instance = models.ForeignKey(Filter, verbose_name = "Related filter", on_delete = models.CASCADE)
    boolean = models.BooleanField(default = False, verbose_name = "Boolean value")
    integer = models.IntegerField(default = 0, verbose_name = "Integer value")
    double = models.FloatField(default = 0.0, verbose_name = "Float value")
    string = models.TextField(max_length = 128, blank = True, verbose_name = "String value")


    def __str__(self):
        if self.instance.parent != None:
            # return parent filter name for use in select
            try:
                return str(Filter.objects.get(pk = self.integer))
            except Filter.DoesNotExist:
                return 'Broken parent link'
        if self.instance.oftype == ValueType.integer:
            return str(self.integer)
        elif self.instance.oftype == ValueType.boolean:
            return str(self.boolean)
        elif self.instance.oftype == ValueType.double:
            return str(self.double)
        elif self.instance.oftype == ValueType.string:
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
    def site_directory_path(instance, filename):
        print('site_{0}/{1}'.format(instance.site.id, filename))
        return 'uploads/{0}/site_{1}/{2}'.format(instance.site.user, instance.site.id, filename)
    
    site = models.ForeignKey(Site, on_delete = models.CASCADE)
    image = models.ImageField(max_length = 128, upload_to = site_directory_path)
    oftype = models.IntegerField(default = 1, verbose_name = "Image type", choices = ImageType.choices)
