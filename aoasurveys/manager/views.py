from django.core.urlresolvers import reverse
from django.views.generic import DetailView, FormView
from django.conf import settings

from aoasurveys.aoaforms.models import Form
from aoasurveys.manager.forms import SelectFieldsForm


class FormManagementView(DetailView, FormView):
    template_name = 'manage_form.html'
    model = Form
    slug_url_kwarg = 'slug'
    form_class = SelectFieldsForm
    context_object_name = 'survey'

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
            'visible_fields': survey.visible_fields_slugs,
            'filtering_fields': survey.filtering_fields_slugs,
        }

    def get_success_url(self):
        return reverse('homepage')

    def get_context_data(self, **kwargs):
        context = super(FormManagementView, self).get_context_data(**kwargs)

        form = context['object']
        fields_and_labels = list(form.fields.all()) + list(form.labels.all())
        fields_and_labels.sort(key=lambda x: x.order)

        context.update({
            'fields_and_labels': fields_and_labels,
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
