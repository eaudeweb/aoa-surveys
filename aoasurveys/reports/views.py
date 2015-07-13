import os
import mimetypes
from urllib import urlencode
from ast import literal_eval

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.conf import settings
from django.http import HttpResponse
from django_datatables_view.base_datatable_view import BaseDatatableView

from aoasurveys.aoaforms.filter import filter_entries
from aoasurveys.aoaforms.models import Form, FieldEntry, FormEntry
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


class AnswerDelete(DeleteView):
    model = Form
    template_name = 'delete_answer.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'survey'

    def get_object(self):
        object = Form.objects.get(
            slug=self.kwargs['slug']).entries.get(pk=self.kwargs['pk'])
        return object

    def get_success_url(self):
        return reverse('homepage')


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
    def get_object(self):
        return Form.objects.get(slug=self.kwargs['slug'])

    def get_order_columns(self):
        form = self.get_object()
        return [str(f.id) for f in form.visible_fields]

    def get_initial_queryset(self):
        form = self.get_object()
        filters = literal_eval(self.request.GET['filters'])
        return filter_entries(form, filters)

    def filter_queryset(self, qs):
        form = self.get_object()
        search_text = self.request.GET.get('search[value]', '')
        search_fields = [
            f.id for f in filter(lambda f: not f.choices, form.visible_fields)]
        if not (search_text or search_fields):
            return qs

        filters = literal_eval(self.request.GET['filters'])
        return filter_entries(form, filters, search_text, search_fields)

    def prepare_results(self, qs):
        json_data = []
        for entry in qs:
            row = []
            for field in entry.visible_fields:
                if not field:
                    data = ''
                elif field.url:
                    data = u'<a href="{url}">View attachment</a>'.format(
                        url=field.url)
                elif field.field.choices:
                    data = get_choices(field, self.request.language)
                else:
                    data = translate(field.value, self.request.language) or ''
                row.append(data)
            row.append(self._get_detail_link(entry))
            row.append(self._get_delete_link(entry))
            json_data.append(row)
        return json_data

    def _get_detail_link(self, entry):
        entry_url = reverse('entry-detail', kwargs=dict(id=entry.id))
        link = (
            '<a class="view-entry launch-modal" '
            'data-toggle="modal" data-action="{entry_url}" '
            'data-title="Entry #{entry_id}" data-target="#myModal" >'
            '<i class="glyphicon glyphicon-list"></i></a>'
        ).format(entry_url=entry_url, entry_id=entry.id)
        return link

    def _get_delete_link(self, entry):
        delete_url = reverse('delete_answer',
                             kwargs=dict(
                                 slug=self.kwargs['slug'], pk=entry.pk))
        link = (
            '<a href="{delete_url}">Delete</a>'
        ).format(delete_url=delete_url)
        return link


class EntryDetail(DetailView):
    template_name = 'entry.html'
    model = FormEntry
    pk_url_kwarg = 'id'
