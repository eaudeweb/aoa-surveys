from django.forms import Form, CharField


class SelectFieldsForm(Form):
    fields_list = CharField(max_length=255, required=False)
