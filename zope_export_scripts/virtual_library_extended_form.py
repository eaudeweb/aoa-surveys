request = container.REQUEST
response =  request.response


mega_survey = "/aoa/tools/virtual_library/virtual-library-extended/"
languages = ["en", "ru"]


form = {}
survey = context.restrictedTraverse(mega_survey)
survey_locals = context.get_local(survey)

  
questions = []
for attribute in survey.objectValues():
  if attribute.id.startswith("w_"):
    field = {"slug": attribute.id, "order": attribute.sortorder, "required": attribute.required}
 
    local_properties = context.get_local(attribute) # get_local is an external method
    title = {}
    for lang in languages:
      title[lang] = local_properties["title"][lang][0]
    field["title"] = title

    if attribute.meta_type == "Naaya Radio Widget":
      field["type"] = "RadioWidget"
      field["display"] = attribute.display
      field["add_extra_choice"] = attribute.add_extra_choice
      field["choices"] = {}
      for lang in languages:
        field["choices"][lang] = local_properties["choices"][lang][0]

    if attribute.meta_type == "Naaya File Widget":
      field["type"] = "FileWidget"
      field["size_max"] = attribute.size_max
 
    if attribute.meta_type == "Naaya Localized String Widget":
      field["type"] = "LocalizedStringWidget"
      field["size_max"] = attribute.size_max
      field["width"] = attribute.width

    if attribute.meta_type == "Naaya Geo Widget":
      field["type"] = "GeoWidget"
        
    if attribute.meta_type == "Naaya String Widget":
      field["type"] = "StringWidget"
      field["size_max"] = attribute.size_max
      field["width"] = attribute.width

    if attribute.meta_type == "Naaya Checkboxes Widget":
      field["type"] = "CheckboxesWidget"
      field["display"] = attribute.display
      field["choices"] = {}
      for lang in languages:
        field["choices"][lang] = local_properties["choices"][lang][0]

    if attribute.meta_type == "Naaya Text Area Widget":
      field["type"] = "TextAreaWidget"
      field["rows"] = attribute.rows
      field["columns"] = attribute.columns
      
    questions.append(field)

form["questions"] = questions
form["slug"] = survey.id
form["title"] = {}
for lang in languages:
      form["title"][lang] = survey_locals["title"][lang][0]

print context.get_json(form) # get_json is an external method

return printed
