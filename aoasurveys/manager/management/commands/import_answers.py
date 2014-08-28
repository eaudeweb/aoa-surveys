import json
from datetime import datetime

from django.db import transaction
from django.core.management.base import BaseCommand
from forms_builder.forms.models import FormEntry, FieldEntry, Form, Field


class Command(BaseCommand):
    args = '<filename>'
    help = 'Import answers exported from Naaya-Survey'

    def _parseAnswers(self, data):
        transaction.set_autocommit(False)
        try:
            form = Form.objects.filter(slug=data["form_id"]).first()
            for answer in data["answer_sets"]:
                formentry = FormEntry.objects.create(
                    form=form,
                    entry_time=answer["modification_time"]
                )
                #TODO set id, respondent, draft
                for slug, value in answer["answers"].items():
                    field = Field.objects.filter(slug=slug).first()
                    if field:
                        FieldEntry.objects.create(
                            entry=formentry,
                            value=",".join(value) if isinstance(value, list) else value,
                            field_id=field.pk
                        )

        except KeyError:
            self.stdout.write('JSON is not in expected format.')
            transaction.rollback()
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

        self._parseAnswers(data)

        datafile.close()