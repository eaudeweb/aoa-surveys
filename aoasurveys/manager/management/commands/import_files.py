import json
import os
import requests
import logging

from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand
from aoasurveys.aoaforms.models import (
    FormEntry, FieldEntry, Form, Field, Label,
)


class Command(BaseCommand):
    args = '<filename>'
    help = 'Download files exported from Naaya-Survey'

    def _parse_answers(self, data):
        transaction.set_autocommit(False)
        try:
            form = Form.objects.filter(slug=data["form_id"]).first()
            if form:
                for answer in data["answer_sets"]:
                    form_entry = FormEntry.objects.filter(
                        form=form,
                        creation_time=answer["creation_date"],
                        entry_time=answer["modification_time"],
                        respondent=answer["respondent"]
                    ).first()

                    if "w_assessment-upload" in answer["answers"]:
                        slug = "w_assessment-upload"
                        value = answer["answers"][slug]
                        if value:
                            if not Label.objects.filter(slug=slug).exists():
                                field = Field.objects.filter(
                                    slug=slug,
                                    form=form
                                ).first()

                                if field:
                                    field_entry = FieldEntry.objects.filter(
                                        entry=form_entry,
                                        field_id=field.pk
                                    ).first()
                                    field_entry.value = self._download_file(
                                        value["url"],
                                        value["title"]
                                    )
                                    field_entry.save()
                                else:
                                    logging.error(
                                        'Field with slug=%s doesnt exist' % slug)
            else:
                logging.error('Form doesnt exist.')

        except KeyError:
            logging.error('JSON is not in expected format.')
            transaction.rollback()
            transaction.set_autocommit(True)
            return

        transaction.commit()
        transaction.set_autocommit(True)

    def _download_file(self, url, filename):
        try:
            r = requests.get(settings.DOWNLOAD_URL + url, stream=True,
                             verify=True)
            if r.status_code == requests.codes.ok:
                path = os.path.join(settings.FORMS_BUILDER_UPLOAD_ROOT,
                                    filename)
                with open(path, 'wb') as fd:
                    for chunk in r.iter_content(512):
                        fd.write(chunk)
                return filename
            else:
                logging.error("For url: {url} status code is {code}".format(
                    url=settings.DOWNLOAD_URL + url,
                    code=r.status_code
                ))
        except Exception as e:
            logging.exception(e)

        return None

    def handle(self, *args, **options):
        if not args:
            logging.error('Expecting a filename.')
            return

        with open(args[0]) as datafile:
            try:
                data = json.load(datafile)
            except ValueError:
                logging.error('File is not in JSON format.')
                return

            self._parse_answers(data)
            datafile.close()


