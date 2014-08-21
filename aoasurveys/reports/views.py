from django.views.generic import ListView
from forms_builder.forms.models import Form


class FormsIndex(ListView):

    template_name = 'reports/index.html'
    model = Form

