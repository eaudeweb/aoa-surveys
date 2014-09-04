import os
import mimetypes
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from forms_builder.forms.models import Form, FieldEntry

from aoasurveys.reports.forms import SelectFieldsForm
from aoasurveys.reports.models import FormExtra


class FormsIndex(ListView):

    template_name = 'reports/index.html'
    model = Form


class AnswersView(DetailView):

    template_name = 'reports/answers.html'
    model = Form
    slug_url_kwarg = 'slug'


class FormExtraView(DetailView, FormView):

    template_name = 'reports/form_extra.html'
    model = Form
    slug_url_kwarg = 'slug'
    form_class = SelectFieldsForm

    def get_success_url(self):
        return reverse('homepage')

    def get_context_data(self, **kwargs):
        context = super(FormExtraView, self).get_context_data(**kwargs)
        context.update({'form': SelectFieldsForm()})
        return context

    def form_valid(self, form):
        extra, _ = FormExtra.objects.get_or_create(form=self.get_object())
        extra.selected_fields_ids = form.cleaned_data['fields_list']
        extra.save()
        return super(FormExtraView, self).form_valid(form)


def file_view(request, field_entry_id):
    field_entry = get_object_or_404(FieldEntry, pk=field_entry_id)
    path = os.path.join(settings.FORMS_BUILDER_UPLOAD_ROOT, field_entry.value)
    response = HttpResponse(content_type=mimetypes.guess_type(path)[0])
    with open(path, 'rb') as f:
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            os.path.split(f.name)[1])
        response.write(f.read())
    return response
