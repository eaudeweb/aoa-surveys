from django.forms import ModelForm

from aoasurveys.aoaforms.models import Form as Survey, Field


class PropertiesForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'intro', 'publish_date', 'expiry_date',
                  'send_email', 'login_required', 'status']

    def __init__(self, *args, **kwargs):
        super(PropertiesForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['size'] = 50


class FieldForm(ModelForm):
    class Meta:
        model = Field
        fields = ['label', 'slug', 'required', 'visible', 'field_type',
                  'choices', 'default']

    def __init__(self, *args, **kwargs):
        self.form_id = kwargs.pop('form_id')
        self.order = kwargs.pop('order')
        super(FieldForm, self).__init__(*args, **kwargs)

    def save(self):
        field = super(FieldForm, self).save(commit=False)
        field.form_id = self.form_id
        field.order = self.order
        field.save()
        return field
