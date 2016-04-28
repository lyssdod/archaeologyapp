from django.contrib import admin

from .models import User, Site

# Register your models here.
admin.site.register(Site)
admin.site.register(User)
