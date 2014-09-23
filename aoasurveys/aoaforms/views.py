from django.views.generic import DetailView, FormView as GenericFormView
from aoasurveys.aoaforms.models import Form


class FormView(DetailView):
    model = Form
    slug_url_kwarg = 'slug'
    template_name = 'forms/form_detail.html'

    # TODO: handle post


form_view = FormView.as_view()


class DetailFormView(DetailView, GenericFormView):
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)
