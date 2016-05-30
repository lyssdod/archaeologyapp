from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter
def lookup(obj, name):
    for x in obj:
        if x.instance.name.lower() == name.lower():
            return _(str(x))
