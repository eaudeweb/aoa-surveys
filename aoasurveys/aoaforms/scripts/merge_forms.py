from aoasurveys.aoaforms.models import Form, FormEntry

form1_slug = "virtual-library-extended"
form2_slug = "bibliography-details-each-assessment"
form3_slug = "merged_form"
form3_title = "Merged Form"

fields_exclude = ["w_information-about-data-uploader", "w_specify-topics",
                  "w_water-resources-topics",
                  "w_submitter-email", "w_green-economy-topics",
                  "w_submitter-name", "w_submitter-organisation",
                  "w_resource-efficiency-topics",
                  "w_water-resource-management-topics",
                  "w_country-or-international-organisation"]
fields_keep = ["w_theme-coverage", "w_other-criteria",
               "w_specific-scope-or-purpose", "w_is-formal",
               "w_assessment-upload", "w_main-criterion", "w_assessment-name",
               "w_body-conducting-assessment",
               "w_publicly-available", "w_location", "w_assessment-url",
               "w_assessment-year", "w_theme",
               "w_paper-only", "w_official-country-region",
               "w_geo-coverage-region", "w_type-document",
               "w_title-original-language"]


def merge_forms():
    form1 = Form.objects.filter(slug=form1_slug).first()
    form2 = Form.objects.filter(slug=form2_slug).first()
    form3, created = Form.objects.get_or_create(
        title=form3_title,
        slug=form3_slug
    )

    #TODO handle diffrent choices for w_theme
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
                entry_time=form_entry.entry_time
            )

            for field_entry in form_entry.fields.all():
                form_field = form.fields.filter(pk=field_entry.field_id).first()
                if form_field.slug in fields_keep:
                    new_form_field = form3.fields.filter(
                        slug=form_field.slug
                    ).first()
                    field_entry.pk = None
                    field_entry.entry = new_form_entry
                    field_entry.field_id = new_form_field.pk
                    field_entry.save()


merge_forms()





