import os
import mimetypes

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from forms_builder.forms.models import Form, FieldEntry

from aoasurveys.reports.forms import SelectFieldsForm, FilteringForm
from aoasurveys.reports.models import FormExtra
from aoasurveys.reports.utils import set_visible_fields, set_url_value
from auth.views import LoginRequiredMixin


class DetailFormView(DetailView, FormView):

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)


class FormsIndex(ListView, LoginRequiredMixin):

    template_name = 'reports/index.html'
    model = Form


class AnswersView(DetailFormView):

    template_name = 'reports/answers.html'
    model = Form
    slug_url_kwarg = 'slug'
    form_class = FilteringForm
    context_object_name = 'survey'
    filter_query = {}

    def get_matching_answers(self):
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

        for answer in self.object.answers:
            set_visible_fields(answer, self.object.extra.visible_fields)
            for field in answer.visible_fields:
                set_url_value(field)
        context = super(AnswersView, self).get_context_data(**kwargs)
        context.update({'advanced_enabled': bool(self.filter_query)})
        return context

    def get_form_kwargs(self):
        kwargs = super(AnswersView, self).get_form_kwargs()
        kwargs.update({'fields': self.get_object().extra.filtering_fields})
        return kwargs

    def form_valid(self, form):
        self.filter_query = {int(k.split('_')[1]): v for k, v in
                             form.cleaned_data.iteritems() if v}
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(
            object=self.object, form=form))


class FormExtraView(DetailFormView):

    template_name = 'reports/form_extra.html'
    model = Form
    slug_url_kwarg = 'slug'
    form_class = SelectFieldsForm
    context_object_name = 'survey'

    def get_initial(self):
        survey = self.get_object()
        initial = {'status': survey.status}
        if survey.extra:
            initial.update({
                'visible_fields': survey.extra.visible_fields_slugs,
                'filtering_fields': survey.extra.filtering_fields_slugs,
            })
        return initial

    def get_success_url(self):
        return reverse('homepage')

    def get_context_data(self, **kwargs):
        context = super(FormExtraView, self).get_context_data(**kwargs)
        context.update({
            'separator': settings.FIELDS_SEPARATOR,
        })
        return context

    def form_valid(self, form):
        survey = self.get_object()
        survey.status = form.cleaned_data['status']
        survey.save()

        extra, _ = FormExtra.objects.get_or_create(form=survey)
        extra.visible_fields_slugs = form.cleaned_data['visible_fields']
        extra.filtering_fields_slugs = form.cleaned_data['filtering_fields']
        extra.save()

        return super(FormExtraView, self).form_valid(form)


def file_view(request, field_entry_id):
    field_entry = get_object_or_404(FieldEntry, pk=field_entry_id)
    path = os.path.join(settings.FORMS_BUILDER_UPLOAD_ROOT, field_entry.value)
    content_type = mimetypes.guess_type(path)[0]
    filename = os.path.split(path)[1]
    with open(path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=' + filename
    return response
