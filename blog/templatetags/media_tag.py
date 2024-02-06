from django import template
from config.settings import MEDIA_URL

register = template.Library()


@register.simple_tag
def media_tag(value):
    return MEDIA_URL + str(value)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
