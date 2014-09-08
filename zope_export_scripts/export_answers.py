request = container.REQUEST
response = request.response

mega_survey = "/aoa/tools/virtual_library/bibliography-details-each-assessment/"
languages = ["en", "ru"]

form = {}
answer_sets = []
survey = context.restrictedTraverse(mega_survey)

for answer in survey.objectValues():
    if answer.id.startswith("answer_"):
        answers = {}

        attributes = context.get_dict(answer)
        for attr, value in attributes.items():
            if attr.startswith("w_"):
                if attr.startswith("w_location"):
                    answers[attr] = context.get_geo(value)
                elif attr.startswith("w_assessment-upload"):
                    answers[attr] = context.get_file(value)
                else:
                    answers[attr] = value
            
        entry = {"id": attributes["id"], "respondent": attributes["respondent"],
                 "modification_time": attributes["modification_time"].ISO8601()}
        if "draft" in attributes:
            entry["draft"] = attributes["draft"]
        else:
            entry["draft"] = False
        
        entry["answers"] = answers
        answer_sets.append(entry)

form["form_id"] = survey.id
form["answer_sets"] = answer_sets

print context.get_json(form)

return printed
