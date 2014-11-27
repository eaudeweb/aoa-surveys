from django.forms import ModelForm, TextInput

from aoasurveys.aoaforms.models import Form as Survey, Field, Label
from aoasurveys.aoaforms.fields import (
    LocalizedStringField, LocalizedTextAreaField,
)


class PropertiesForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'intro', 'publish_date', 'expiry_date', 'send_email',
                  'login_required', 'status']
        widgets = {'title': TextInput(attrs={'size': 100})}


class SurveyForm(PropertiesForm):
    title = LocalizedStringField()
    intro = LocalizedTextAreaField()


class FieldForm(ModelForm):
    label = LocalizedStringField()

    class Meta:
        model = Field
        fields = ['label', 'required', 'visible', 'field_type', 'choices',
                  'default']

    def __init__(self, *args, **kwargs):
        self.form_id = kwargs.pop('form_id')
        super(FieldForm, self).__init__(*args, **kwargs)

    def save(self):
        field = super(FieldForm, self).save(commit=False)
        field.form_id = self.form_id
        field.save()
        return field


class LabelForm(FieldForm):
    label = LocalizedStringField()

    class Meta:
        model = Label
        fields = ['label']
