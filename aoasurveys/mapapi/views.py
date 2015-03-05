import json, calendar
from django.http import HttpResponse
from django.conf import settings
from aoasurveys.aoaforms.models import FormEntry, FieldEntry, Field
from aoasurveys.reports.templatetags.extra_tags import (
    translate, get_choices_list_field,
)


def parse_json_file(json_filename, short_names_mapping):
    result_dict = {}
    with open(json_filename) as json_file:
        try:
            json_data = json.load(json_file)

            result_dict.update((k, v) for k, v in json_data.items()
                               if k != 'documents')
            short_names_mapping['country'] = dict(
                (v['en'], k) for k, v in json_data['country_name'].items()
            )
            short_names_mapping['region'] = dict(
                (v['en'], k) for k, v in json_data['region_name'].items()
            )
            short_names_mapping['theme'] = {
                'Water resources': 'water',
                'Water resource management': 'water',
                'Green economy': 'green-economy',
                'Resource efficiency': 'green-economy',
            }
        except ValueError:
            return {"error": "error parsing json file"}
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
    form_entries = dict(
        FormEntry.objects.filter(form_id=1).values_list('id', 'entry_time')
    )
    field_entries = (
        FieldEntry.objects.filter(entry__id__in=form_entries.keys())
        .order_by('entry__id')
    )
    field_map = dict(Field.objects.values_list('id', 'slug'))
    field_obj_map = dict((f.slug, f) for f in Field.objects.all())

    def _fix_time(some_time):
        return float(calendar.timegm(some_time.timetuple()))

    def _entries():
        entry = {}
        entry_id = None
        for fe in field_entries:
            if fe.entry_id != entry_id:
                if entry:
                    entry['upload-time'] = _fix_time(form_entries[entry_id])
                    yield entry
                    entry = {}
                entry_id = fe.entry_id
            entry[field_map[fe.field_id]] = fe.value

        if entry:
            entry['upload-time'] = _fix_time(form_entries[entry_id])
            yield entry

    for form_entry in _entries():
        form_dict = {'upload-time': form_entry['upload-time']}
        for old_field_name, orig_value in form_entry.items():
            if old_field_name not in FIELDS_MAPPING:
                continue
            value = translate(orig_value, 'en')
            field = field_obj_map[old_field_name]
            if field.choices:
                value = get_choices_list_field(field, value, 'en')
            field_name = FIELDS_MAPPING[old_field_name]
            if field_name in ('country', 'region', 'theme'):
                value = list(set(
                    [short_names_mapping[field_name][v] for v in value if
                     v in short_names_mapping[field_name]]))
            if field_name in BILINGUAL_FIELDS:
                value = {'ru': translate(orig_value, 'ru'),
                         'en': translate(orig_value, 'en')}
            form_dict[field_name] = value
        documents.append(form_dict)

    return documents


def json_map(request):
    short_names_mapping = {}
    json_data = parse_json_file(settings.JSON_MAP_FILE_PATH,
                                short_names_mapping)
    json_data['documents'] = get_documents(short_names_mapping)
    response = json.dumps(json_data)
    return HttpResponse(response, content_type="application/json")
