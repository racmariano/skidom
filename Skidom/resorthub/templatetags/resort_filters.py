from django import template

register = template.Library()

@register.filter
def use_index(sequence, position):
    return sequence[position]
