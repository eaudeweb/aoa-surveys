from django.views.generic import DetailView
from aoasurveys.aoaforms.models import Form


class FormView(DetailView):
    model = Form
    slug_url_kwarg = 'slug'
    template_name = 'forms/form_detail.html'

    # TODO: handle post

form_view = FormView.as_view()
