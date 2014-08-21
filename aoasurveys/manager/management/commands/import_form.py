from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '<filename>'
    help = 'Import a dynamic form exported from Naaya-Survey'

    def handle(self, *args, **options):
        if not args:
            self.stdout.write('Expecting a filename.')
            return

        self.stdout.write('Not implemented')
