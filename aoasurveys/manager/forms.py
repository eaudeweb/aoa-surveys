from django.forms import ModelForm

from aoasurveys.aoaforms.models import Form as Survey


class PropertiesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropertiesForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['size'] = 50

    class Meta:
        model = Survey
        fields = ['status', 'title']
