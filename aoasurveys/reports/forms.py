from django.forms import Form, CharField, MultipleChoiceField

from aoasurveys.reports.utils import get_translation


class FilteringForm(Form):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', [])
        language = kwargs.pop('language')
        super(FilteringForm, self).__init__(*args, **kwargs)
        for field in fields:
            field_name = '{0}_{1}'.format(field.id, field.slug)
            field_label = get_translation(field.label, language)
            if field.choices:
                choices = [(idx, get_translation(choice, language))
                           for idx, choice in field.get_choices()]
                self.fields[field_name] = MultipleChoiceField(
                    label=field_label,
                    choices=choices,
                    required=False,
                )
            else:
                self.fields[field_name] = CharField(
                    label=field_label,
                    max_length=255,
                    required=False,
                )
