from django.forms.fields import MultiValueField, CharField
from django.forms.widgets import MultiWidget
from django.forms import TextInput, Textarea

LOCALIZEDSTRING = 100
LOCALIZEDTEXTAREA = 101


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
        labels=["English", "Russian"],
        widgets=[TextInput, TextInput]
    )

    def __init__(self, *args, **kwargs):
        list_fields = [CharField(), CharField()]
        super(LocalizedStringField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        return "\n".join(values)


class LocalizedTextAreaField(LocalizedStringField):
    widget = LocalizedMultiWidget(
        labels=["English", "Russian"],
        widgets=[Textarea, Textarea]
    )