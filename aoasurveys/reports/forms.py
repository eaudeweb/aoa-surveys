from django.forms import Form, CharField, MultipleChoiceField


class SelectFieldsForm(Form):
    visible_fields = CharField(max_length=255, required=False)
    filtering_fields = CharField(max_length=255, required=False)


class FilteringForm(Form):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', [])
        super(FilteringForm, self).__init__(*args, **kwargs)
        for field in fields:
            field_name = 'id_{}'.format(field.id)
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
