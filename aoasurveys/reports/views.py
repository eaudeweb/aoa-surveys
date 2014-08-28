from django.views.generic import ListView, DetailView
from forms_builder.forms.models import Form


class FormsIndex(ListView):

    template_name = 'reports/index.html'
    model = Form


class AnswersView(DetailView):

    template_name = 'reports/answers.html'
    model = Form
    slug_url_kwarg = 'slug'
