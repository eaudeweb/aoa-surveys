from django.conf.urls import patterns, url
from aoasurveys.aoaforms.views import FormSent, FormView


urlpatterns = patterns('aoasurveys.aoaforms.views',
    url(r"(?P<slug>.*)/sent/$", FormSent.as_view(), name="form_sent"),
    url(r'^(?P<slug>.*)/form/$', FormView.as_view(), name='form_detail'),
)
