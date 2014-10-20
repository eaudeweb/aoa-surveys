from django.forms import Form, CharField, TextInput, ModelForm

from aoasurveys.aoaforms.models import Form as Survey


class SelectFieldsForm(Form):
    # TODO: use ModelForm
    visible_fields = CharField(max_length=255, required=False,
                               widget=TextInput(attrs={'size': 40}))
    filtering_fields = CharField(max_length=255, required=False,
                                 widget=TextInput(attrs={'size': 40}))


class PropertiesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropertiesForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['size'] = 50

    class Meta:
        model = Survey
        fields = ['status', 'title']
