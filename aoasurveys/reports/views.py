import os
import mimetypes
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.http import HttpResponse
from forms_builder.forms.models import Form, FieldEntry


class FormsIndex(ListView):

    template_name = 'reports/index.html'
    model = Form


class AnswersView(DetailView):

    template_name = 'reports/answers.html'
    model = Form
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(AnswersView, self).get_context_data(**kwargs)
        return context


def file_view(request, field_entry_id):
    field_entry = get_object_or_404(FieldEntry, pk=field_entry_id)
    path = os.path.join(settings.FORMS_BUILDER_UPLOAD_ROOT, field_entry.value)
    response = HttpResponse(content_type=mimetypes.guess_type(path)[0])
    with open(path, 'rb') as f:
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            os.path.split(f.name)[1])
        response.write(f.read())
    return response
