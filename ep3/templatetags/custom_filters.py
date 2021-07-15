from django import template

register = template.Library()


@register.filter()
def remove_last_char(value):
    return value[:len(value)-1]
