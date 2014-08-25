from django.core.management.base import BaseCommand
from pprint import pprint
import json


class Command(BaseCommand):
    args = '<filename>'
    help = 'Import a dynamic form exported from Naaya-Survey'

    def _parseForm(self, form):
        #TODO parse form
        for answer in form["answers"]:
            #TODO parse answers
            self._parseAnswer(answer)

    def _parseAnswer(self, answer):
        #TODO parse answer
        pass

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

        if "forms" in data:
            for form in data["forms"]:
                self._parseForm(form)
        else:
            self.stdout.write('JSON is not in format expected.')
            return

        datafile.close()