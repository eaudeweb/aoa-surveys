from django import template
from django.forms.forms import BoundField
from django.template.loader import get_template

from aoasurveys.aoaforms.forms import DisplayedForm
from aoasurveys.aoaforms.models import Label

register = template.Library()


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
            (label, label.order) for label in form.labels.all()
        ]
        fields_order = {
            field.slug: field.order for field in form.fields.visible()
        }
        fields = [
            (value, fields_order[key]) for key, value in
            form_for_form.fields.iteritems()
        ]
        fields_and_labels = [
            elem for elem, order in sorted(
                labels + fields,
                key=lambda (f, o): o
            )
        ]

        class FakeForm(object):
            def __iter__(self):
                for field in fields_and_labels:
                    if isinstance(field, Label):
                        yield field
                    else:
                        for key, value in form_for_form.fields.iteritems():
                            if value == field:
                                yield BoundField(form_for_form, field, key)
                                break

        context['form_for_form'] = form_for_form
        context['fields_and_labels'] = FakeForm()
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
