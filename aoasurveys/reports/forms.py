from django.forms import Form, CharField, MultipleChoiceField

from aoasurveys.reports.utils import get_translation


class FilteringForm(Form):
    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language')
        self._fields = kwargs.pop('fields', [])
        super(FilteringForm, self).__init__(*args, **kwargs)
        for field in self._fields:
            field_name = field.slug
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

    def get_filter_query(self):
        if not self.is_valid():
            return {}
        field_map = {field.slug: field.id for field in self._fields}
        return {field_map[k]: v for k, v in self.cleaned_data.iteritems() if v}
