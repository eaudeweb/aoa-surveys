import os
import mimetypes
from urllib import urlencode

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.http import HttpResponse
from django_datatables_view.base_datatable_view import BaseDatatableView

from aoasurveys.aoaforms.filter import filter_entries
from aoasurveys.aoaforms.models import Form, FieldEntry
from aoasurveys.reports.forms import FilteringForm
from aoasurveys.reports.templatetags.extra_tags import get_choices, translate


class FormsIndex(ListView):
    template_name = 'index.html'
    model = Form


class AnswersView(DetailView):
    template_name = 'answers.html'
    model = Form
    slug_url_kwarg = 'slug'
    context_object_name = 'survey'

    def get_context_data(self, **kwargs):
        context = super(AnswersView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_kwargs = {
            'fields': self.object.filtering_fields,
            'language': self.request.language,
            'data': self.request.GET
        }
        form = FilteringForm(**form_kwargs)
        context = self.get_context_data(object=self.object, form=form)
        context.update({
            'custom_js': settings.CUSTOM_JS.get(self.object.slug),
            'filters': urlencode({'filters': form.get_filter_query()}),
        })
        return self.render_to_response(context)


def file_view(request, field_entry_id):
    field_entry = get_object_or_404(FieldEntry, pk=field_entry_id)
    path = os.path.join(settings.FORMS_BUILDER_UPLOAD_ROOT, field_entry.value)
    content_type = mimetypes.guess_type(path)[0]
    filename = os.path.split(path)[1]
    with open(path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=' + filename
    return response


class AnswersListJson(BaseDatatableView):
    order_columns = ['id']

    def get_initial_queryset(self):
        object = Form.objects.get(slug=self.kwargs['slug'])
        filters = eval(self.request.GET['filters'])
        return filter_entries(object, filters)

    def filter_queryset(self, qs):
        # TODO: apply filters
        return qs

    def prepare_results(self, qs):
        json_data = []
        for entry in qs:
            row = []
            for field in entry.visible_fields:
                if not field:
                    continue
                if field.url:
                    data = '<a href="{{ url }}">View attachment</a>'.format(
                        url=field.url)
                elif field.field.choices:
                    data = get_choices(field, self.request.language)
                else:
                    data = translate(field.value, self.request.language) or ''
                row.append(data)
            json_data.append(row)
        return json_data
