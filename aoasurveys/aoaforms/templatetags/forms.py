from django import template
from django.forms.forms import BoundField
from django.template.loader import get_template

from aoasurveys.aoaforms.forms import DisplayedForm
from aoasurveys.aoaforms.models import Label
from aoasurveys.reports.utils import get_translation

register = template.Library()


class FakeForm(object):
    def __init__(self, form, fields_and_labels):
        self.fields_and_labels = fields_and_labels
        self.form = form

    def __iter__(self):
        for field, slug in self.fields_and_labels:
            if isinstance(field, Label):
                yield field
            else:
                yield BoundField(self.form, field, slug)


class CustomFormNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        form = template.Variable(self.value).resolve(context)
        t = get_template("forms/built_form.html")
        context["form"] = form

        form_for_form = DisplayedForm(
            form,
            context,
            getattr(context["request"], "POST", None),
            getattr(context["request"], "FILES", None)
        )

        labels = [
            (label, label.order, None) for label in form.labels.all()
        ]
        fields_order = {
            field.slug: field.order for field in form.fields.visible()
        }
        fields = [
            (field, fields_order[slug], slug) for slug, field in
            form_for_form.fields.iteritems()
        ]

        fields_and_labels = [
            (field, slug) for field, order, slug in sorted(
                labels + fields,
                key=lambda (f, o, s): o
            )
        ]

        context['form_for_form'] = form_for_form
        context['fields_and_labels'] = FakeForm(form_for_form,
                                                fields_and_labels)
        return t.render(context)


@register.tag
def render_built_form(parser, token):
    """
    render_build_form takes one argument in one of the following format:

    {% render_build_form form_instance %}
    {% render_build_form form=form_instance %}
    {% render_build_form id=form_instance.id %}
    {% render_build_form slug=form_instance.slug %}

    """
    try:
        _, arg = token.split_contents()
        if "=" not in arg:
            arg = "form=" + arg
        name, value = arg.split("=", 1)
        if name not in ("form", "id", "slug"):
            raise ValueError
    except ValueError:
        raise template.TemplateSyntaxError(render_built_form.__doc__)

    return CustomFormNode(name, value)


@register.filter
def label_translated(field, language):
    return '<label for="{id}">{text}</label>'.format(
        id=field.name, text=get_translation(field.label, language))
