from django.core.management.base import BaseCommand

from aoasurveys.aoaforms.models import Form


class Command(BaseCommand):
    args = '<form_slug>'
    help = 'Flush all answers from a form'

    def handle(self, *args, **options):
        if not args:
            self.stdout.write('Expecting a form slug.')
            return

        form = Form.objects.filter(slug=args[0]).first()
        if not form:
            self.stdout.write('No such form: ' + args[0])
            return

        form.entries.all().delete()
