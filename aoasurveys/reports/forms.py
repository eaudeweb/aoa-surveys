from django.forms import (
    Form, CharField, MultipleChoiceField, ChoiceField, RadioSelect, TextInput,
)
from forms_builder.forms.models import STATUS_CHOICES


class SelectFieldsForm(Form):
    visible_fields = CharField(max_length=255, required=False,
                               widget=TextInput(attrs={'size': 40}))
    filtering_fields = CharField(max_length=255, required=False,
                                 widget=TextInput(attrs={'size': 40}))
    status = ChoiceField(choices=STATUS_CHOICES, widget=RadioSelect)


class FilteringForm(Form):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', [])
        super(FilteringForm, self).__init__(*args, **kwargs)
        for field in fields:
            field_name = '{0}_{1}'.format(field.id, field.slug)
            if field.choices:
                self.fields[field_name] = MultipleChoiceField(
                    label=field.label,
                    choices=list(field.get_choices()),
                    required=False,
                )
            else:
                self.fields[field_name] = CharField(
                    label=field.label,
                    max_length=255,
                    required=False,
                )
