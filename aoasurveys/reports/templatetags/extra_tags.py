from django import template
from forms_builder.forms.models import STATUS_PUBLISHED

from auth.views import is_admin


register = template.Library()


@register.assignment_tag(takes_context=True)
def check_is_admin(context):
    return is_admin(context['request'])


@register.filter
def published(form_list):
    return [form for form in form_list if form.status == STATUS_PUBLISHED]
