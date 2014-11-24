from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import DetailView, TemplateView

from forms_builder.forms.signals import form_invalid, form_valid
from aoasurveys.aoaforms.forms import DisplayedForm
from aoasurveys.aoaforms.models import Form


class FormView(DetailView):
    template_name = 'forms/form_detail.html'
    model = Form
    slug_url_kwarg = 'slug'

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
                return redirect("form_sent", slug=form.slug)
        context = {"form": form, "form_for_form": form_for_form}
        return self.render_to_response(context)


class FormSent(TemplateView):
    template_name = "forms/form_sent.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.slug = kwargs['slug']
        return super(FormSent, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FormSent, self).get_context_data(**kwargs)
        published = Form.objects.published(for_user=self.user)
        context.update({
            "form": get_object_or_404(published, slug=self.slug),
        })
        return context
