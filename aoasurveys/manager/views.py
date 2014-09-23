from django.core.urlresolvers import reverse
from django.conf import settings

from aoasurveys.aoaforms.views import DetailFormView
from aoasurveys.aoaforms.models import Form
from aoasurveys.manager.forms import SelectFieldsForm


class FormManagementView(DetailFormView):
    template_name = 'manage_form.html'
    model = Form
    slug_url_kwarg = 'slug'
    form_class = SelectFieldsForm
    context_object_name = 'survey'

    def get_initial(self):
        survey = self.get_object()
        return {
            'status': survey.status,
            'visible_fields': survey.visible_fields_slugs,
            'filtering_fields': survey.filtering_fields_slugs,
        }

    def get_success_url(self):
        return reverse('homepage')

    def get_context_data(self, **kwargs):
        context = super(FormManagementView, self).get_context_data(**kwargs)
        context.update({
            'separator': settings.FIELDS_SEPARATOR,
        })
        return context

    def form_valid(self, form):
        survey = self.get_object()
        survey.status = form.cleaned_data['status']
        survey.visible_fields_slugs = form.cleaned_data['visible_fields']
        survey.filtering_fields_slugs = form.cleaned_data['filtering_fields']
        survey.save()
        return super(FormManagementView, self).form_valid(form)
