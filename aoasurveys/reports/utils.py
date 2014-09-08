import os

from django.core.urlresolvers import reverse
from django.conf import settings
from forms_builder.forms.models import Field
from forms_builder.forms import fields
from forms_builder.forms.utils import split_choices


def set_visible_fields(answer, form_visible_fields):
    answer.visible_fields = [answer.fields.get(field_id=field.id)
                             for field in form_visible_fields]


def set_url_value(field_entry):
    field = Field.objects.filter(pk=field_entry.field_id).first()
    if field and field.is_a(fields.FILE):
        field_entry.url = reverse('file_view', args=(field.id,))
        field_entry.value = os.path.split(field_entry.value)[1]


def get_ordered_fields(slugs):
    slugs = [s.strip() for s in slugs.split(settings.FIELDS_SEPARATOR)]
    fields = list(Field.objects.filter(slug__in=slugs))
    fields.sort(key=lambda x: slugs.index(x.slug))
    return fields


def filter_answers(answers, filter_query):
    for answer in answers:
        for field_id, filter_value in filter_query.iteritems():
            field_value = answer.fields.get(field_id=field_id).value
            if isinstance(filter_value, list):
                field_choices = split_choices(field_value)
                if not set(filter_value) & set(field_choices):
                    break
            else:
                if filter_value not in field_value:
                    break
        else:
            yield answer
