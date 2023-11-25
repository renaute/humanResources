from django import template

register = template.Library()

@register.filter
def get_item(dictionery,key):
    return dictionery.get(key)