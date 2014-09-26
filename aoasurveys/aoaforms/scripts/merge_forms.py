from aoasurveys.aoaforms.models import Form


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

    for field in form1.fields.all():
        if field.slug in fields_keep:
            field.pk = None
            field.form = form3
            field.save()

    #TODO merge answers

merge_forms()





