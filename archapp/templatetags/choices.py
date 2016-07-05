from django import template
from django import forms

register = template.Library()

@register.filter
def default_choice(field, choice):
    for e in field.field.choices:
        if e[1] == choice:
            choice_id = e[0]

    field.field.initial = choice_id
    return field
