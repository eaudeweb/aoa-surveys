from django.core.management.base import BaseCommand
from forms_builder.forms.models import Form, Field, FormEntry, FieldEntry
from forms_builder.forms.fields import *
import json


class Command(BaseCommand):
    args = '<filename>'
    help = 'Import a dynamic form exported from Naaya-Survey'

    def _parseForm(self, data):
        if "title" in data and "questions" in data and "labels" in data:
            form = Form.objects.create(title=data["title"])
            for question in data["questions"]:
                params = {"label": question["title"],
                          "slug": question["slug"],
                          "order": question["sortorder"],
                          "required": question["required"],
                          "form": form}

                if question["type"] == "FileWidget":
                    #TODO size_max
                    params["field_type"] = FILE

                if question["type"] == "StringWidget":
                    #TODO set width, size_max
                    params["field_type"] = TEXT

                if question["type"] == "CheckboxesWidget":
                    params["visible"] = question["display"]
                    params["choices"] = ",".join(question["choices"])
                    params["field_type"] = CHECKBOX_MULTIPLE

                if question["type"] == "RadioWidget":
                    #TODO set add_extra_choice
                    params["visible"] = question["display"]
                    params["choices"] = ",".join(question["choices"])
                    params["field_type"] = RADIO_MULTIPLE

                if question["type"] == "TextAreaWidget":
                    #TODO set columns, rows
                    params["field_type"] = TEXTAREA

                if question["type"] == "ComboboxWidget":
                    params["choices"] = ",".join(question["choices"])
                    params["field_type"] = SELECT

                if question["type"] == "CheckboxMatrixWidget":
                    params["choices"] = ",".join(question["choices"])
                    params["field_type"] = CHECKBOX_MULTIPLE

                if question["type"] == "LocalizedTextAreaWidget":
                    #TODO set columns, rows
                    params["field_type"] = TEXTAREA

                if question["type"] == "GeoWidget":
                    params["field_type"] = TEXT

                if question["type"] == "LocalizedStringWidget":
                    #TODO set width, size_max
                    params["field_type"] = TEXTAREA

                Field.objects.create(**params)

        else:
            self.stdout.write('JSON is not in expected format.')
            return

    def handle(self, *args, **options):
        if not args:
            self.stdout.write('Expecting a filename.')
            return

        datafile = open(args[0])
        try:
            data = json.load(datafile)
        except ValueError:
            self.stdout.write('File is not in JSON format.')
            return

        self._parseForm(data)

        datafile.close()