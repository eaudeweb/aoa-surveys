from django.db.models import Model, OneToOneField, CharField
from forms_builder.forms.models import Form

from aoasurveys.reports.utils import get_ordered_fields


class FormExtra(Model):
    form = OneToOneField(Form, related_name='extra')
    visible_fields_slugs = CharField(max_length=255)
    filtering_fields_slugs = CharField(max_length=255)

    @property
    def visible_fields(self):
        return get_ordered_fields(self.visible_fields_slugs)

    @property
    def filtering_fields(self):
        return get_ordered_fields(self.filtering_fields_slugs)
