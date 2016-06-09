from django import template
from archapp.models import ImageType
from django.conf import settings
register = template.Library()

@register.filter
def pick(obj, args):
    z = None

    oftype, size = args.split(',')

    for i in obj:
        if i['oftype'] == getattr(ImageType, oftype.lower()):
            if size in settings.MEDIA_SIZES:
                return settings.MEDIA_URL + i[size]
