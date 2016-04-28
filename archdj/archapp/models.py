from django.db import models

# generic Filter for Property referencing
class Filter(models.Model):

    # descriptive name
    name = models.CharField(max_length = 64)

    def __str__(self):
        return self.name

# Property of a Site
class Property(models.Model):
    class Type:
        integer = 0
        boolean = 1
        double = 2
        string = 3

    instance = models.ForeignKey(Filter, on_delete = models.CASCADE)
    boolean = models.BooleanField(default = False)
    integer = models.IntegerField(default = 0)
    double = models.FloatField(default = 0.0)
    string = models.TextField(max_length = 128)

    oftype = models.IntegerField(default = 0)
    linked = models.BooleanField(default = False)

    def __str__(self):
        if self.oftype == Type.integer:
            return str(self.integer)
        elif self.oftype == Type.boolean:
            return str(self.boolean)
        elif self.oftype == Type.double:
            return str(self.double)
        elif self.oftype == Type.string:
            return self.string

# User model
class User(models.Model):
    email = models.EmailField(max_length = 128)
    nickname = models.CharField(max_length = 64)
    password = models.CharField(max_length = 64)

    # User can define custom Filters
    #filters = models.ForeignKey(FilterGroup, on_delete = models.CASCADE)

    def __str__(self):
        return self.email


# archaeology Site
class Site(models.Model):
    name = models.CharField(max_length = 128)

    # someone has created it
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    # it has many properties
    props = models.ManyToManyField('Property')

    # aux data (serialized)
    data = models.CharField(max_length = 4096)

    def __str__(self):
        return self.name

# Site photos
class Image(models.Model):
    class Type:
        general = 1
        plane = 2
        photo = 3
        found = 4

    site = models.ForeignKey(Site, on_delete = models.CASCADE, null = True)
    image = models.ImageField(max_length = 128, upload_to = 'uploads/')
    oftype = models.IntegerField(default = 0)
