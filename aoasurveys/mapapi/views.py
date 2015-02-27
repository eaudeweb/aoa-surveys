import json, calendar
from django.http import HttpResponse
from aoasurveys.aoaforms.models import FormEntry
from aoasurveys.reports.templatetags.extra_tags import translate, get_choices_list


def parse_json_file(json_filename, short_names_mapping):
    result_dict = {}
    json_file = open(json_filename)
    json_data = json.load(json_file)

    result_dict.update((k, v) for k, v in json_data.items()
                       if k != 'documents')
    short_names_mapping['country'] = dict((v['en'], k) for k, v
                                          in json_data['country_name'].items())
    short_names_mapping['region'] = dict((v['en'], k) for k, v
                                          in json_data['region_name'].items())
    short_names_mapping['theme'] = {
        'Water resources': 'water',
        'Water resource management': 'water',
        'Green economy': 'green-economy',
        'Resource efficiency': 'green-economy',
    }
    json_file.close()
    return result_dict


def get_documents(short_names_mapping):
    FIELDS_MAPPING = {
        'w_assessment-name': 'title',
        'w_assessment-url': 'url',
        'w_official-country-region': 'country',
        'w_body-conducting-assessment': 'author',
        'w_geo-coverage-region': 'region',
        'w_theme': 'theme',
        'w_assessment-year': 'year',
        'w_type-document': 'document_type',
        'w_theme-coverage': 'geolevel',
    }
    BILINGUAL_FIELDS = [
        'title',
    ]

    documents = []
    form_entries = FormEntry.objects.filter(form_id=1)
    for form_entry in form_entries:
        form_dict = {}

        form_dict['upload-time'] = float(calendar.\
            timegm(form_entry.entry_time.timetuple()))
        for field_entry in form_entry.all_fields:
            old_field_name = field_entry.field.slug
            if old_field_name in FIELDS_MAPPING:
                value = translate(field_entry.value, 'en')
                if field_entry.field.choices:
                    value = get_choices_list(field_entry, 'en')
                field_name = FIELDS_MAPPING[old_field_name]
                #special cases
                if field_name == 'country' or field_name == 'region'\
                        or field_name == 'theme':
                    value = list(set([short_names_mapping[field_name][v]
                             for v in value
                             if v in short_names_mapping[field_name]]))
                if field_name in BILINGUAL_FIELDS:
                    value = {'ru': translate(field_entry.value, 'ru'),
                             'en': value}
                form_dict[field_name] = value

        documents.append(form_dict)
    return documents


def json_map(request):
    short_names_mapping = {}
    json_data = parse_json_file('/Users/ana/test/json_data',
                                short_names_mapping)
    json_data['documents'] = get_documents(short_names_mapping)
    response = json.dumps(json_data)
    return HttpResponse(response, content_type="application/json")
