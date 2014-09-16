from django.forms import Form, CharField, ChoiceField, RadioSelect, TextInput
from forms_builder.forms.models import STATUS_CHOICES


class SelectFieldsForm(Form):
    visible_fields = CharField(max_length=255, required=False,
                               widget=TextInput(attrs={'size': 40}))
    filtering_fields = CharField(max_length=255, required=False,
                                 widget=TextInput(attrs={'size': 40}))
    status = ChoiceField(choices=STATUS_CHOICES, widget=RadioSelect)
