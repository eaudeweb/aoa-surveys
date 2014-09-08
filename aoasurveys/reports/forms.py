from django.forms import Form, CharField, MultipleChoiceField


class SelectFieldsForm(Form):
    visible_fields = CharField(max_length=255, required=False)
    filtering_fields = CharField(max_length=255, required=False)


class FilteringForm(Form):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', [])
        super(FilteringForm, self).__init__(*args, **kwargs)
        for field in fields:
            if field.choices:
                self.fields[field.slug] = MultipleChoiceField(
                    label=field.label,
                    choices=list(field.get_choices()),
                    required=False,
                )
            else:
                self.fields[field.slug] = CharField(
                    label=field.label,
                    max_length=255,
                    required=False,
                )
