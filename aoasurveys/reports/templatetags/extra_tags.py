from django import template
from forms_builder.forms.models import STATUS_PUBLISHED
from aoasurveys.reports.utils import get_translation

register = template.Library()


@register.filter
def published(form_list):
    return [form for form in form_list if form.status == STATUS_PUBLISHED]


@register.filter
def translate(value, language):
    return get_translation(value, language)


@register.filter
def get_choices_list(field_entry, language):
    if not field_entry.value:
        return []
    try:
        choice_ids = [int(c.strip()) for c in field_entry.value.split(',')]
    except ValueError:
        return field_entry.value

    choices = dict(field_entry.field.get_choices())
    return [get_translation(choices.get(id), language) for id in choice_ids]


def get_choices_list_field(field, value, language):
    if not value:
        return []
    try:
        choice_ids = [int(c.strip()) for c in value.split(',')]
    except ValueError:
        return value

    choices = dict(field.get_choices())
    return [get_translation(choices.get(id), language) for id in choice_ids]


@register.filter
def get_choices(field_entry, language):
    return ', '.join(get_choices_list(field_entry, language))
