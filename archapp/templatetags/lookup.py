from django import template
from archapp.models import Filter
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter
def lookup(obj, args):
    z = None

    names = [arg.strip() for arg in args.split(',')]

    for x in obj:
        if x.instance.name.lower() == names[0].lower():
            z = x

            if len(names) > 1:
                # TODO: optimize
                p = Filter.objects.filter(name = names[1]).get()
                z = p.subfilters.filter(pk = x.integer).get()

            return _(str(z))
