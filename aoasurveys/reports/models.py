from django.db.models import Model, OneToOneField, CharField
from django.conf import settings
from forms_builder.forms.models import Field, Form


class FormExtra(Model):
    form = OneToOneField(Form, related_name='extra')
    selected_fields_ids = CharField(max_length=255)

    @property
    def selected_fields(self):
        fields_ids = self.selected_fields_ids.split(
            settings.FORM_EXTRA_SEPARATOR)
        return [Field.objects.get(slug=id) for id in fields_ids]
