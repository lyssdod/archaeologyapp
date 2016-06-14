from django import template
from archapp.models import ImageType
from django.conf import settings
#from easy_thumbnails.files import get_thumbnailer
register = template.Library()

@register.filter
def pick(obj, args):
    z = None

    oftype, size = args.split(',')

    for i in obj:
        if i.oftype == getattr(ImageType, oftype.lower()):
            return settings.MEDIA_URL + '/' + str(i.image)#.image#get_thumbnailer(obj.image)[size].url
