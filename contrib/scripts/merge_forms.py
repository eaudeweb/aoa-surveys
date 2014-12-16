"""
    Merge the two forms.

    Note:
        form2 overrides form1 (important for choices).
"""
import sys, os
sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aoasurveys.settings")

from aoasurveys.aoaforms.models import Form, FormEntry

form1_slug = "virtual-library-extended"
form2_slug = "bibliography-details-each-assessment"
form3_slug = "virtual-library-merged"
form3_title = "Welcome to the Virtual Library - Merged"

fields_exclude = [
    "w_information-about-data-uploader",
    "w_specify-topics",
    "w_water-resources-topics",
    "w_submitter-email", "w_green-economy-topics",
    "w_submitter-name", "w_submitter-organisation",
    "w_resource-efficiency-topics",
    "w_water-resource-management-topics",
]
fields_keep = [
    "w_theme-coverage", "w_other-criteria",
    "w_specific-scope-or-purpose", "w_is-formal",
    "w_assessment-upload", "w_main-criterion", "w_assessment-name",
    "w_body-conducting-assessment",
    "w_publicly-available", "w_location", "w_assessment-url",
    "w_assessment-year", "w_theme",
    "w_paper-only", "w_official-country-region",
    "w_geo-coverage-region", "w_type-document",
    "w_title-original-language",
    "w_country-or-international-organisation",
]
values_translate = {
    form1_slug: {
        'w_theme': {
            '0': '1',
            '1': '0',
            '2': '0',
            '3': '1',
        }
    }
}


def merge_forms():
    form1 = Form.objects.filter(slug=form1_slug).first()
    form2 = Form.objects.filter(slug=form2_slug).first()
    form3, created = Form.objects.get_or_create(
        title=form3_title,
        slug=form3_slug
    )
    form3.entries.get_queryset().delete()
    form3.fields.get_queryset().delete()

    for form in form1, form2:
        for field in form.fields.all():
            if field.slug in fields_keep and not form3.fields.filter(
                    slug=field.slug).count():
                field.pk = None
                field.form = form3
                field.save()

        for form_entry in FormEntry.objects.filter(form=form):
            new_form_entry = FormEntry.objects.create(
                form=form3,
                creation_time=form_entry.creation_time,
                entry_time=form_entry.entry_time,
                respondent=form_entry.respondent
            )

            for field_entry in form_entry.fields.all():
                form_field = form.fields.filter(
                    pk=field_entry.field_id).first()
                if form_field.slug in fields_keep:
                    new_form_field = form3.fields.filter(
                        slug=form_field.slug
                    ).first()
                    field_entry.pk = None
                    field_entry.entry = new_form_entry
                    field_entry.field_id = new_form_field.pk
                    if form.slug in values_translate:
                        translate = values_translate[form.slug]
                        if field_entry.field.slug in translate:
                            field_entry.value = translate.get(
                                field_entry.field.slug, field_entry.value)
                    field_entry.save()


if __name__ == '__main__':
    merge_forms()
