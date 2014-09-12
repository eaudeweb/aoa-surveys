from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from forms_builder.forms.models import AbstractField
from aoasurveys.reports.models import Form


class Label(models.Model):
    form = models.ForeignKey(Form, related_name="labels")
    order = models.IntegerField(_("Order"), null=True, blank=True)

    class Meta(AbstractField.Meta):
        ordering = ("order",)
        verbose_name = 'Label'
        verbose_name_plural = 'Labels'

admin.site.register(Label)