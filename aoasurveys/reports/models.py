import os
from django.db.models import Model, OneToOneField, CharField
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from forms_builder.forms.signals import form_valid
from forms_builder.forms.models import FieldEntry, Field, Form
from forms_builder.forms import fields


class FormExtra(Model):
    form = OneToOneField(Form, related_name='extra')
    selected_fields_ids = CharField(max_length=255)

    @property
    def selected_fields(self):
        fields_ids = self.selected_fields_ids.split(
            settings.FORM_EXTRA_SEPARATOR)
        return [Field.objects.get(slug=id) for id in fields_ids]


class FieldEntryExtra(Model):
    field_entry = OneToOneField(FieldEntry, related_name='extra')

    def is_file(self):
        field = get_object_or_404(Field, pk=self.field_entry.field_id)
        return field.is_a(fields.FILE)

    @property
    def file_properties(self):
        props = {}
        if self.is_file():
            props['url'] = reverse('file_view', args=(self.field_entry.id,))
            props['value'] = os.path.split(self.field_entry.value)[1]
        return props


@receiver(form_valid)
def set_extras(sender, form, entry, **kwargs):
    for field in entry.form.fields.all():
        field_entry, _ = entry.fields.get_or_create(field_id=field.id)
        extra = FieldEntryExtra(field_entry=field_entry)
        extra.save()
