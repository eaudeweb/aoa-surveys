from django.forms import Form, CharField


class SelectFieldsForm(Form):
    visible_fields = CharField(max_length=255, required=False)
    filtering_fields = CharField(max_length=255, required=False)
