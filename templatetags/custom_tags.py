from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def current_page_title(page_name=''):
    return f'{page_name} | {settings.APP_NAME}' if page_name else settings.APP_NAME
