from django.contrib import admin
from django.db.models import CharField, ForeignKey, IntegerField
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from forms_builder.forms import fields as forms_builder_fields
from forms_builder.forms.models import (
    AbstractForm, AbstractFormEntry, AbstractField, AbstractFieldEntry,
)


class Form(AbstractForm):
    visible_fields_slugs = CharField(max_length=255)
    filtering_fields_slugs = CharField(max_length=255)

    def get_ordered_fields(self, slugs):
        slugs = [s.strip() for s in slugs.split(settings.FIELDS_SEPARATOR)]
        fields = list(self.fields.filter(slug__in=slugs))
        fields.sort(key=lambda x: slugs.index(x.slug))
        return fields

    @property
    def visible_fields(self):
        return self.get_ordered_fields(self.visible_fields_slugs)

    @property
    def filtering_fields(self):
        return self.get_ordered_fields(self.filtering_fields_slugs)


class FormEntry(AbstractFormEntry):
    form = ForeignKey("Form", related_name="entries")

    @property
    def visible_fields(self):
        return [self.fields.filter(field_id=field.id).first()
                for field in self.form.visible_fields]


class Field(AbstractField):
    form = ForeignKey("Form", related_name="fields")
    order = IntegerField(_("Order"), null=True, blank=True)

    class Meta(AbstractField.Meta):
        ordering = ("order",)

    def get_choices(self):
        choices = super(Field, self).get_choices()
        return enumerate([c for (c, c) in choices])


class FieldEntry(AbstractFieldEntry):
    entry = ForeignKey("FormEntry", related_name="fields")

    @property
    def field(self):
        return Field.objects.filter(pk=self.field_id).first()

    @property
    def url(self):
        if self.field and self.field.is_a(forms_builder_fields.FILE):
            if hasattr(settings, 'DOWNLOAD_URL'):
                return settings.DOWNLOAD_URL + self.value
            else:
                return reverse('file_view', args=(self.id,))


admin.site.register(Form)
