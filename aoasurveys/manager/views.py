from django.core.urlresolvers import reverse
from django.views.generic import DetailView, FormView, View
from django.http import HttpResponse
from django.conf import settings

from aoasurveys.aoaforms.models import Form
from aoasurveys.manager.forms import PropertiesForm
from aoasurveys.reports.utils import get_translation, set_translation


class FormPropertiesView(DetailView, FormView):
    model = Form
    slug_url_kwarg = 'slug'
    context_object_name = 'survey'
    template_name = 'properties.html'
    form_class = PropertiesForm
    tab = 'properties'

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_initial(self):
        survey = self.get_object()
        return {
            'status': survey.status,
            'title': get_translation(survey.title, self.request.language),
        }

    def form_valid(self, form):
        survey = self.get_object()
        survey.status = form.cleaned_data['status']
        set_translation(survey, 'title', form.cleaned_data['title'],
                        self.request.language)
        survey.save()
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
        tab = self.request.POST['tab']

        if tab == 'fields':
            order_nr = 10
            for slug in ordered_slugs:
                field = form.fields.filter(slug=slug).first() or \
                    form.labels.filter(slug=slug).first()
                field.order = order_nr
                order_nr += 10
                field.save()
        else:
            slugs_str = settings.FIELDS_SEPARATOR.join(ordered_slugs)
            if tab == 'visible_fields':
                form.visible_fields_slugs = slugs_str
            elif tab == 'filter_fields':
                form.filtering_fields_slugs = slugs_str
            form.save()

        return HttpResponse({'succes': True})
