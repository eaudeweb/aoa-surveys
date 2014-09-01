from django.db import transaction
from django.core.management.base import BaseCommand

from forms_builder.forms.models import Form, Field
from forms_builder.forms.fields import TEXT, FILE, CHECKBOX_MULTIPLE, \
    RADIO_MULTIPLE, TEXTAREA, SELECT
from aoasurveys.forms import LOCALIZEDSTRING, LOCALIZEDTEXTAREA

import json


class Command(BaseCommand):
    args = '<filename>'
    help = 'Import a dynamic form exported from Naaya-Survey'

    def _parseForm(self, data):
        transaction.set_autocommit(False)
        try:
            form = Form.objects.create(title=data["title"], slug=data["slug"])
            for question in data["questions"]:
                params = {
                    "label": question["title"],
                    "slug": question["slug"],
                    "order": question["sortorder"],
                    "required": question["required"],
                    "form": form
                }

                if question["type"] == "FileWidget":
                    #TODO size_max
                    params["field_type"] = FILE

                elif question["type"] == "StringWidget":
                    #TODO set width, size_max
                    params["field_type"] = TEXT

                elif question["type"] == "CheckboxesWidget":
                    params["visible"] = question["display"]
                    params["choices"] = ",".join(question["choices"])
                    params["field_type"] = CHECKBOX_MULTIPLE

                elif question["type"] == "RadioWidget":
                    #TODO set add_extra_choice
                    params["visible"] = question["display"]
                    params["choices"] = ",".join(question["choices"])
                    params["field_type"] = RADIO_MULTIPLE

                elif question["type"] == "TextAreaWidget":
                    #TODO set columns, rows
                    params["field_type"] = TEXTAREA

                elif question["type"] == "ComboboxWidget":
                    params["choices"] = ",".join(question["choices"])
                    params["field_type"] = SELECT

                elif question["type"] == "CheckboxMatrixWidget":
                    params["choices"] = ",".join(question["choices"])
                    params["field_type"] = CHECKBOX_MULTIPLE

                elif question["type"] == "LocalizedTextAreaWidget":
                    #TODO set columns, rows
                    params["field_type"] = LOCALIZEDTEXTAREA

                elif question["type"] == "GeoWidget":
                    params["field_type"] = TEXT

                elif question["type"] == "LocalizedStringWidget":
                    #TODO set width, size_max
                    params["field_type"] = LOCALIZEDSTRING

                else:
                    self.stdout.write('Unrecognized type in JSON.')
                    return

                Field.objects.create(**params)

        except KeyError:
            self.stdout.write('JSON is not in expected format.')
            transaction.rollback()
            transaction.set_autocommit(True)
            return

        transaction.commit()
        transaction.set_autocommit(True)

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