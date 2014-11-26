from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import (
    CharField, ForeignKey, IntegerField, Model, SlugField, DateTimeField, Max,
)
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.html import format_html
from forms_builder.forms import fields as forms_builder_fields
from forms_builder.forms.models import (
    AbstractForm, AbstractFormEntry, AbstractField, AbstractFieldEntry,
)
from forms_builder.forms.utils import slugify, unique_slug

from aoasurveys.reports.utils import get_translation


class Form(AbstractForm):
    class Meta:
        permissions = (
            ('config', 'Can change configuration'),
        )

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
    respondent = CharField(
        _("Respondent"),
        max_length=100
    )
    creation_time = DateTimeField(_("Creation time"), null=True)

    @property
    def visible_fields(self):
        return [self.fields.filter(field_id=field.id).first()
                for field in self.form.visible_fields]


class Field(AbstractField):
    form = ForeignKey("Form", related_name="fields")
    order = IntegerField(_("Order"), null=True, blank=True)

    class Meta(AbstractField.Meta):
        ordering = ("order",)
        unique_together = ('form', 'slug')

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


class Label(Model):
    form = ForeignKey(Form, related_name="labels")
    order = IntegerField(_("Order"), null=True, blank=True)
    slug = SlugField(_('Slug'), max_length=100, blank=True, default='')
    label = CharField(_('Label'), max_length=255)

    class Meta(AbstractField.Meta):
        ordering = ("order",)
        verbose_name = 'Label'
        verbose_name_plural = 'Labels'

    def __unicode__(self):
        return format_html('<label>{0}</label>', get_translation(
            self.label, getattr(self, 'language', settings.DEFAULT_LANGUAGE)))


@receiver(pre_save, sender=Label)
@receiver(pre_save, sender=Field)
def my_callback(sender, instance, *args, **kwargs):
    max_order = max(instance.form.fields.aggregate(Max('order')).values() +
                    instance.form.labels.aggregate(Max('order')).values())
    instance.order = max_order + 1


@receiver(pre_save, sender=Label)
def callback(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(instance.label)
        instance.slug = unique_slug(instance.__class__.objects, "slug", slug)


admin.site.register(Form)
admin.site.register(Field, list_display=('slug', 'required', 'form'),
                    list_filter=('form',))
admin.site.register(FormEntry, list_display=('entry_time', 'form'))
admin.site.register(FieldEntry, list_display=('entry', 'field_id', 'value'))
admin.site.register(Label, list_display=('slug', 'label', 'form'))
