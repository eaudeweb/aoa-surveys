from django.core.urlresolvers import reverse
from django.views.generic import DetailView, FormView
from django.conf import settings

from aoasurveys.aoaforms.models import Form
from aoasurveys.manager.forms import SelectFieldsForm, PropertiesForm


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
        }

    def form_valid(self, form):
        survey = self.get_object()
        survey.status = form.cleaned_data['status']
        survey.save()
        return super(FormPropertiesView, self).form_valid(form)


class FormFieldsView(FormManagementView):
    template_name = 'fields.html'
    form_class = SelectFieldsForm
    tab = 'fields'

    def get_initial(self):
        survey = self.get_object()
        return {
            'visible_fields': survey.visible_fields_slugs,
            'filtering_fields': survey.filtering_fields_slugs,
        }

    def form_valid(self, form):
        survey = self.get_object()
        survey.visible_fields_slugs = form.cleaned_data['visible_fields']
        survey.filtering_fields_slugs = form.cleaned_data['filtering_fields']
        survey.save()
        return super(FormFieldsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FormFieldsView, self).get_context_data(**kwargs)

        form = context['object']
        fields_and_labels = list(form.fields.all()) + list(form.labels.all())
        fields_and_labels.sort(key=lambda x: x.order)

        context.update({
            'fields_and_labels': fields_and_labels,
            'separator': settings.FIELDS_SEPARATOR,
        })
        return context
