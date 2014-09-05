from django.db.models import Model, OneToOneField, CharField
from django.conf import settings
from forms_builder.forms.models import Field, Form


class FormExtra(Model):
    form = OneToOneField(Form, related_name='extra')
    visible_fields_slugs = CharField(max_length=255)

    @property
    def visible_fields(self):
        slugs = [slug.strip() for slug in
                 self.visible_fields_slugs.split(settings.FIELDS_SEPARATOR)]
        visible_fields = list(Field.objects.filter(slug__in=slugs))
        visible_fields.sort(key=lambda x: slugs.index(x.slug))
        return visible_fields
