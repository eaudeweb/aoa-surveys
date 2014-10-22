from django.core.urlresolvers import reverse
from django.views.generic import DetailView, FormView, View
from django.conf import settings
from django.http import HttpResponse

from aoasurveys.aoaforms.models import Form
from aoasurveys.manager.forms import PropertiesForm
from aoasurveys.reports.utils import get_translation, set_translation


class FormManagementView(DetailView, FormView):
    model = Form
    slug_url_kwarg = 'slug'
    context_object_name = 'survey'

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('homepage')

    def get_context_data(self, **kwargs):
        context = super(FormManagementView, self).get_context_data(**kwargs)
        context['tab'] = self.tab
        return context


class FormPropertiesView(FormManagementView):
    template_name = 'properties.html'
    form_class = PropertiesForm
    tab = 'properties'

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


class FormFieldsView(DetailView):
    template_name = 'form_fields.html'
    tab = 'fields'
    model = Form

    def get_context_data(self, **kwargs):
        context = super(FormFieldsView, self).get_context_data(**kwargs)

        form = context['object']
        fields_and_labels = list(form.fields.all()) + list(form.labels.all())
        fields_and_labels.sort(key=lambda x: x.order)

        context.update({
            'fields_and_labels': fields_and_labels,
            'separator': settings.FIELDS_SEPARATOR,
            'tab': self.tab,
        })
        return context


class FieldsOrderView(View):
    def post(self, request, *args, **kwargs):
        form = Form.objects.filter(slug=kwargs['slug']).first()
        ordered_slugs = self.request.POST['slugs'].split(',')
        order_nr = 10
        for slug in ordered_slugs:
            field = form.fields.filter(slug=slug).first() or \
                form.labels.filter(slug=slug).first()
            field.order = order_nr
            order_nr += 10
            field.save()
        return HttpResponse({'succes': True})
