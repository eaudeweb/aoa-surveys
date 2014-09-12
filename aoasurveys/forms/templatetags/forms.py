from aoasurveys.forms.models import Label
from django import template
from django.forms.forms import BoundField
from django.template.loader import get_template

from aoasurveys.forms.forms import DisplayedForm

register = template.Library()


class CustomFormNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        request = context["request"]
        post = getattr(request, "POST", None)
        files = getattr(request, "FILES", None)
        form = template.Variable(self.value).resolve(context)
        t = get_template("forms/built_form.html")
        context["form"] = form
        form_args = (form, context, post or None, files or None)
        form_for_form = DisplayedForm(*form_args)

        labels = [(label, label.order) for label in form.labels.all()]
        fields = zip(
            form_for_form.fields.values(),
            range(0, 10*len(form_for_form.fields), 10)
        )
        fields_and_labels = [
            f[0] for f in sorted(
                labels + fields,
                key=lambda elem: elem[1]
            )
        ]
        context['form_for_form'] = form_for_form

        class FakeForm(object):
            def __iter__(self):
                for field in fields_and_labels:
                    if isinstance(field, Label):
                        yield field
                    else:
                        yield BoundField(form_for_form, field, str(field))

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
        e = ()
        raise template.TemplateSyntaxError(render_built_form.__doc__)

    return CustomFormNode(name, value)