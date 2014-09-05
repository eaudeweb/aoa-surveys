import os

from django.core.urlresolvers import reverse
from django.conf import settings
from forms_builder.forms.models import Field
from forms_builder.forms import fields


def set_visible_fields(answer, form_visible_fields):
    answer.visible_fields = [answer.fields.get(field_id=field.id)
                             for field in form_visible_fields]


def set_url_value(field_entry):
    field = Field.objects.filter(pk=field_entry.field_id).first()
    if field and field.is_a(fields.FILE):
        field_entry.url = reverse('file_view', args=(field.id,))
        field_entry.value = os.path.split(field.value)[1]


def get_ordered_fields(slugs):
        slugs = [s.strip() for s in slugs.split(settings.FIELDS_SEPARATOR)]
        fields = list(Field.objects.filter(slug__in=slugs))
        fields.sort(key=lambda x: slugs.index(x.slug))
        return fields
