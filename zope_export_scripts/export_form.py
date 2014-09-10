request = container.REQUEST
response = request.response

mega_survey = "/aoa/tools/virtual_library/virtual-library-extended/"
languages = ["en", "ru"]

def filter_lang(mapping):
    result = {}
    for key, value in mapping.items():
        result[key] = value[0]

    return result

form = {}
survey = context.restrictedTraverse(mega_survey)
survey_locals = context.get_local(survey)

labels = []
questions = []
for attribute in survey.objectValues():
    if attribute.id.startswith("w_"):
        field = {"slug": attribute.id, "order": attribute.sortorder}
        if attribute.meta_type != "Naaya Label Widget":
            field["required"] = attribute.required

        local_properties = context.get_local(attribute)
        field["title"] = filter_lang(local_properties["title"])

        if attribute.meta_type == "Naaya Radio Widget":
            field["type"] = "RadioWidget"
            field["display"] = attribute.display
            field["add_extra_choice"] = attribute.add_extra_choice
            field["choices"] = filter_lang(local_properties["choices"])

        if attribute.meta_type == "Naaya File Widget":
            field["type"] = "FileWidget"
            field["size_max"] = attribute.size_max

        if attribute.meta_type == "Naaya Localized String Widget":
            field["type"] = "LocalizedStringWidget"
            field["size_max"] = attribute.size_max
            field["width"] = attribute.width

        if attribute.meta_type == "Naaya Geo Widget":
            field["type"] = "GeoWidget"

        if attribute.meta_type == "Naaya Combobox Widget":
            field["type"] = "ComboboxWidget"
            field["choices"] = filter_lang(local_properties["choices"])

        if attribute.meta_type == "Naaya String Widget":
            field["type"] = "StringWidget"
            field["size_max"] = attribute.size_max
            field["width"] = attribute.width

        if attribute.meta_type == "Naaya Checkboxes Widget":
            field["type"] = "CheckboxesWidget"
            field["display"] = attribute.display
            field["choices"] = filter_lang(local_properties["choices"])

        if attribute.meta_type == "Naaya Checkbox Matrix Widget":
            field["type"] = "CheckboxMatrixWidget"
            field["choices"] = filter_lang(local_properties["choices"])
            field["rows"] = filter_lang(local_properties["rows"])

        if attribute.meta_type == "Naaya Text Area Widget":
            field["type"] = "TextAreaWidget"
            field["rows"] = attribute.rows
            field["columns"] = attribute.columns

        if attribute.meta_type == "Naaya Localized Text Area Widget":
            field["type"] = "LocalizedTextAreaWidget"
            field["rows"] = attribute.rows
            field["columns"] = attribute.columns
 
        if attribute.meta_type == "Naaya Label Widget":
            labels.append(field)
        else:
            questions.append(field)

form["questions"] = questions
form["labels"] = labels
form["slug"] = survey.id
form["title"] = filter_lang(survey_locals["title"])
#form["description"] = filter_lang(survey_locals["description"])
#form["geographical_coverage"] = filter_lang(survey_locals["coverage"])
form["first_day"] = survey.releasedate
form["last_day"] = survey.expirationdate
form["notify_owner"] = survey.notify_owner
form["email_respondents_notify"] = survey.notify_respondents
form["multiple_reponses_one_user"] = survey.allow_multiple_answers
form["allow_anonymous"] = survey.allow_anonymous

print context.get_json(form)  # get_json is an external method

return printed
