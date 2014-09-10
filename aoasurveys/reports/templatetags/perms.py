from django import template

from auth.views import is_admin


register = template.Library()


@register.assignment_tag(takes_context=True)
def check_is_admin(context):
    return is_admin(context['request'])
