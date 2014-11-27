from forms_builder.forms.forms import FormForForm

from aoasurveys.aoaforms.models import FieldEntry, FormEntry


class DisplayedForm(FormForForm):
    field_entry_model = FieldEntry

    class Meta:
        model = FormEntry
        exclude = ("form", "entry_time", "respondent", "creation_time")
