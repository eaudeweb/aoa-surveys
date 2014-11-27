from django.core.urlresolvers import reverse
from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404

from aoasurveys.aoaforms.models import Form, Field, Label
from aoasurveys.manager.forms import (
    PropertiesForm, FieldForm, LabelForm, SurveyForm,
)
from aoasurveys.reports.utils import get_translation, set_translation


class FormPropertiesView(UpdateView):
    model = Form
    template_name = 'properties.html'
    form_class = PropertiesForm
    tab = 'properties'
    trans_attrs = ['title', 'intro']

    def get_initial(self):
        initial = super(FormPropertiesView, self).get_initial()
        for attr in self.trans_attrs:
            initial[attr] = get_translation(getattr(self.object, attr),
                                            self.request.language)
        return initial

    def form_valid(self, form):
        for attr in self.trans_attrs:
            value = form.cleaned_data[attr].replace('\n', '')
            set_translation(self.object, attr, value, self.request.language)
        self.object.save()
        return super(FormPropertiesView, self).form_valid(form)

    def get_success_url(self):
        return reverse('homepage')

    def get_context_data(self, **kwargs):
        context = super(FormPropertiesView, self).get_context_data(**kwargs)
        context['tab'] = self.tab
        return context


class FormFieldsView(DetailView):
    template_name = 'form_fields.html'
    model = Form

    def get_context_data(self, **kwargs):
        context = super(FormFieldsView, self).get_context_data(**kwargs)

        fields_and_labels = list(self.object.fields.all()) + \
            list(self.object.labels.all())
        fields_and_labels.sort(key=lambda x: x.order)

        context.update({
            'fields': fields_and_labels,
            'tab': 'fields',
        })
        return context


class FormVisibleFieldsView(DetailView):
    template_name = 'visible_fields.html'
    model = Form

    def get_context_data(self, **kwargs):
        context = super(FormVisibleFieldsView, self).get_context_data(**kwargs)

        form = self.object
        vis_slugs = form.visible_fields_slugs.split(settings.FIELDS_SEPARATOR)
        fields = form.fields.exclude(slug__in=vis_slugs).order_by('order')

        context.update({
            'fields': fields,
            'tab': 'visible_fields'
        })
        return context


class FormFilterFieldsView(DetailView):
    template_name = 'filter_fields.html'
    model = Form

    def get_context_data(self, **kwargs):
        context = super(FormFilterFieldsView, self).get_context_data(**kwargs)

        form = self.object
        f_slugs = form.filtering_fields_slugs.split(settings.FIELDS_SEPARATOR)
        fields = form.fields.exclude(slug__in=f_slugs).order_by('order')

        context.update({
            'fields': fields,
            'tab': 'filter_fields'
        })
        return context


class FieldsOrderView(View):
    def post(self, request, *args, **kwargs):
        form = Form.objects.filter(slug=kwargs['slug']).first()
        ordered_slugs = self.request.POST['slugs'].split(',')

        if kwargs['tab'] == 'fields':
            order_nr = 1
            for slug in ordered_slugs:
                field = form.fields.filter(slug=slug).first() or \
                    form.labels.filter(slug=slug).first()
                field.order = order_nr
                order_nr += 1
                field.save()
        else:
            slugs_str = settings.FIELDS_SEPARATOR.join(ordered_slugs)
            if kwargs['tab'] == 'visible_fields':
                form.visible_fields_slugs = slugs_str
            elif kwargs['tab'] == 'filter_fields':
                form.filtering_fields_slugs = slugs_str
            form.save()

        return HttpResponse('{"success": true}')


class CreateSurvey(CreateView):
    form_class = SurveyForm
    template_name = 'new_form.html'

    def get_success_url(self):
        return reverse('homepage')


class DeleteSurvey(DeleteView):
    model = Form
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse('homepage')


class DeleteField(DeleteView):
    model = Field
    template_name = 'delete_field.html'

    def get_success_url(self):
        return reverse('manage_fields', args=[self.kwargs['formslug']])


class DeleteLabel(DeleteField):
    model = Label


class EditField(UpdateView):
    model = Field
    template_name = 'edit_field.html'
    fields = ['label']

    def get_initial(self):
        initial = super(EditField, self).get_initial()
        initial['label'] = get_translation(self.object.label,
                                           self.request.language)
        return initial

    def get_success_url(self):
        return reverse('manage_fields', args=[self.kwargs['formslug']])


class EditLabel(EditField):
    model = Label


class CreateField(CreateView):
    form_class = FieldForm
    template_name = 'new_field.html'

    def get_form_kwargs(self):
        form_kwargs = super(CreateField, self).get_form_kwargs()
        self.form_slug = self.kwargs['formslug']
        survey = get_object_or_404(Form, slug=self.form_slug)
        form_kwargs['form_id'] = survey.id
        return form_kwargs

    def get_success_url(self):
        return reverse('manage_fields', args=[self.form_slug])


class CreateLabel(CreateField):
    form_class = LabelForm
