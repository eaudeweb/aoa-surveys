from django import template
from forms_builder.forms.models import STATUS_PUBLISHED


register = template.Library()


@register.filter
def published(form_list):
    return [form for form in form_list if form.status == STATUS_PUBLISHED]
