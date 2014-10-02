from aoasurveys.aoaforms.models import FieldEntry, FormEntry
from forms_builder.forms.forms import FormForForm


class DisplayedForm(FormForForm):
    field_entry_model = FieldEntry

    class Meta:
        model = FormEntry
        exclude = ("form", "entry_time", "respondent")
