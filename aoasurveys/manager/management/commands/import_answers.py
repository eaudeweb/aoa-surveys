import json

from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand

from aoasurveys.aoaforms.models import FormEntry, FieldEntry, Form, Field


class Command(BaseCommand):
    args = '<filename>'
    help = 'Import answers exported from Naaya-Survey'

    def _to_string(self, obj):
        if isinstance(obj, list):
            value = u",".join([str(x) for x in obj])

        elif isinstance(obj, dict):
            value = u"\n".join((obj.get("en", ""), obj.get("ru", "")))
        else:
            value = obj
        value = unicode(value)
        if len(value) > settings.FORMS_BUILDER_FIELD_MAX_LENGTH:
            print "Truncating value for obj %s" % obj
            value = value[:settings.FORMS_BUILDER_FIELD_MAX_LENGTH]
        return value


    def _parseAnswers(self, data):
        transaction.set_autocommit(False)
        try:
            form = Form.objects.filter(slug=data["form_id"]).first()
            if form:
                for answer in data["answer_sets"]:
                    formentry = FormEntry.objects.create(
                        form=form,
                        entry_time=answer["modification_time"]
                    )
                    #TODO set id, respondent, draft
                    for slug, value in answer["answers"].items():
                        field = (
                            Field.objects.filter(slug=slug, form=form).first()
                        )
                        if field:
                            FieldEntry.objects.create(
                                entry=formentry,
                                value=self._to_string(value),
                                field_id=field.pk
                            )
                        else:
                            self.stdout.write(
                                'Field with slug=%s doesnt exist' % slug)
            else:
                self.stdout.write('Form doesnt exist.')

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

        with open(args[0]) as datafile:
            try:
                data = json.load(datafile)
            except ValueError:
                self.stdout.write('File is not in JSON format.')
                return

            self._parseAnswers(data)
            datafile.close()
