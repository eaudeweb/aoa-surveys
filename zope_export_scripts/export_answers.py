request = container.REQUEST
response = request.response

def filter_lang(mapping):
    result = {}
    for key, value in mapping.items():
        result[key] = value[0]

    return result

mega_survey = "/aoa/tools/virtual_library/bibliography-details-each-assessment/"
languages = ["en", "ru"]

form = {}
answer_sets = []
survey = context.restrictedTraverse(mega_survey)

for answer in survey.objectValues():
    if answer.id.startswith("answer_"):
        answers = {}

        local_properties = context.get_local(answer)
        attributes = context.get_dict(answer)
        for attr, value in attributes.items():
            if attr.startswith("w_"):
                if attr.startswith("w_location"):
                    answers[attr] = context.get_geo(value)
                elif attr.startswith("w_assessment-upload"):
                    answers[attr] = context.get_file(value)
                else:
                    answers[attr] = value

        for attr, value in local_properties.items():
            if attr.startswith("w_"):
                answers[attr] = filter_lang(local_properties[attr])

        entry = {"id": attributes["id"], "respondent": attributes["respondent"],
                 "modification_time": attributes["modification_time"].ISO8601()}
        
        approved_date = attributes.get("approved_date", None)
        if isinstance(approved_date, DateTime):
            entry["approval_date"] = approved_date.ISO8601()
        else:
            entry["approval_date"] = None

        creation_date = attributes.get("creation_date", None)
        if isinstance(creation_date, DateTime):
            entry["creation_date"] = creation_date.ISO8601()
        else:
            entry["creation_date"] = None

        if "draft" in attributes:
            entry["draft"] = attributes["draft"]
        else:
            entry["draft"] = False
        
        entry["cf_approval_list"] = attributes.get("cf_approval_list", None)
        entry["answers"] = answers
        answer_sets.append(entry)

form["form_id"] = survey.id
form["answer_sets"] = answer_sets

print context.get_json(form)

return printed
