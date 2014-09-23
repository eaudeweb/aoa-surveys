import os
import mimetypes

from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q
from aoasurveys.aoaforms.filter import filter_entries

from aoasurveys.aoaforms.views import DetailFormView
from aoasurveys.aoaforms.models import Form, FieldEntry
from aoasurveys.reports.forms import FilteringForm


class FormsIndex(ListView):
    template_name = 'index.html'
    model = Form


class AnswersView(DetailFormView):
    template_name = 'answers.html'
    model = Form
    slug_url_kwarg = 'slug'
    form_class = FilteringForm
    context_object_name = 'survey'
    filter_query = {}

    def get_matching_answers(self):
        return filter_entries(self.object, self.filter_query)

    def get_matching_answers_old(self):
        answers = set(list(self.object.entries.all()))
        for filter_id, filter_value in self.filter_query.iteritems():
            if isinstance(filter_value, list):
                q_expression = Q()
                for choice in filter_value:
                    q_expression |= Q(fields__value__contains=choice)
            else:
                q_expression = Q(fields__value__contains=filter_value)
            q_expression &= Q(fields__field_id=filter_id)
            answers &= set(list(self.object.entries.filter(q_expression)))
            if not answers:
                break
        return answers

    def get_context_data(self, **kwargs):
        self.object.answers = self.get_matching_answers()
        context = super(AnswersView, self).get_context_data(**kwargs)
        context.update({
            'advanced_enabled': bool(self.filter_query),
            'custom_js': settings.CUSTOM_JS.get(self.object.slug),
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(AnswersView, self).get_form_kwargs()
        kwargs.update({
            'fields': self.get_object().filtering_fields,
            'language': self.request.language,
        })
        return kwargs

    def form_valid(self, form):
        self.filter_query = {int(k.split('_')[0]): v for k, v in
                             form.cleaned_data.iteritems() if v}
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(
            object=self.object, form=form))


def file_view(request, field_entry_id):
    field_entry = get_object_or_404(FieldEntry, pk=field_entry_id)
    path = os.path.join(settings.FORMS_BUILDER_UPLOAD_ROOT, field_entry.value)
    content_type = mimetypes.guess_type(path)[0]
    filename = os.path.split(path)[1]
    with open(path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=' + filename
    return response
