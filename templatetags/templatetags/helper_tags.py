from django import template
register = template.Library()

@register.filter
def split(str):
    if not str: return []
    return filter(lambda x: x,str.split('\n'))
