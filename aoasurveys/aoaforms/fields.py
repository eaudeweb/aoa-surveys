from django.forms.fields import MultiValueField, CharField
from django.conf import settings
from django.forms.widgets import MultiWidget, Widget
from django.forms import TextInput, Textarea
from django.utils.safestring import mark_safe


class LocalizedMultiWidget(MultiWidget):
    def __init__(self, labels, widgets, attrs=None):
        self.labels = labels
        super(LocalizedMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split("\n")
        else:
            return ['', '']

    def format_output(self, rendered_widgets):

        def _make_field(field):
            return "<br/><label>%s</label><br/>%s" % field

        return ''.join(map(_make_field, zip(self.labels, rendered_widgets)))


class LocalizedStringField(MultiValueField):
    widget = LocalizedMultiWidget(
        labels=settings.LOCALIZED_LANGUAGES,
        widgets=[TextInput, TextInput]
    )

    def __init__(self, *args, **kwargs):
        list_fields = [CharField(), CharField()]
        super(LocalizedStringField, self).__init__(list_fields, *args,
                                                   **kwargs)

    def compress(self, values):
        return "\n".join(values)


class LocalizedTextAreaField(LocalizedStringField):
    widget = LocalizedMultiWidget(
        labels=settings.LOCALIZED_LANGUAGES,
        widgets=[Textarea, Textarea]
    )


class LabelWidget(Widget):
    def render(self, name, value, attrs=None):
        return mark_safe("<h4>%s</h4>" % self.attrs["value"])


class LabelField(CharField):
    widget = LabelWidget()

    def widget_attrs(self, widget):
        attrs = super(LabelField, self).widget_attrs(widget)
        attrs.update({'value': self.label})
        return attrs
