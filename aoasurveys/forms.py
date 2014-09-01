from django.forms.fields import MultiValueField, CharField
from django.forms.widgets import MultiWidget
from django.forms import TextInput, Textarea

LOCALIZEDSTRING = 100
LOCALIZEDTEXTAREA = 101

class StringMultiWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = [TextInput(), TextInput()]
        super(StringMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split("\n")
        else:
            return ['', '']


class LocalizedStringField(MultiValueField):
    widget = StringMultiWidget

    def __init__(self, *args, **kwargs):
        list_fields = [CharField(), CharField()]
        super(LocalizedStringField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        return "\n".join(values)


class TextAreaMultiWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = [Textarea(), Textarea()]
        super(TextAreaMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split("\n")
        else:
            return ['', '']


class LocalizedTextAreaField(LocalizedStringField):
    widget = TextAreaMultiWidget