#Django
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def BASE_URL():
    return settings.BASE_URL
