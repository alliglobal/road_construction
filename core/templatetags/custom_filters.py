from django import template
register = template.Library()

@register.filter
def dict_get(d, key):
    item = d.get(key)
    return item.quantity_done if item else ''

@register.filter
def dict_get_note(d, key):
    item = d.get(key)
    return item.note if item else ''
