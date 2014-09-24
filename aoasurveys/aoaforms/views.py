from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import DetailView, FormView as GenericFormView

from aoasurveys.aoaforms.forms import DisplayedForm
from aoasurveys.aoaforms.models import Form

from forms_builder.forms.signals import form_invalid, form_valid


class FormView(DetailView):
    model = Form
    slug_url_kwarg = 'slug'
    template_name = 'forms/form_detail.html'

    def post(self, request, *args, **kwargs):
        published = Form.objects.published(for_user=request.user)
        form = get_object_or_404(published, slug=kwargs["slug"])
        form_for_form = DisplayedForm(form, RequestContext(request),
                                    request.POST or None,
                                    request.FILES or None)
        if not form_for_form.is_valid():
            form_invalid.send(sender=request, form=form_for_form)
        else:
            entry = form_for_form.save()
            form_valid.send(sender=request, form=form_for_form, entry=entry)
            if not request.is_ajax():
                return redirect("homepage")
        context = {"form": form, "form_for_form": form_for_form}
        return self.render_to_response(context)

form_view = FormView.as_view()


class DetailFormView(DetailView, GenericFormView):
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)
