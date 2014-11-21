from django.conf.urls import patterns, url
from aoasurveys.aoaforms.views import (
    FormSent, FormView, CreateSurvey, DeleteSurvey,
)


urlpatterns = patterns('aoasurveys.aoaforms.views',
    url(r"(?P<slug>.*)/sent/$", FormSent.as_view(), name="form_sent"),
    url(r'^(?P<slug>.*)/form/$', FormView.as_view(), name='form_detail'),
    url(r'^new_form/$', CreateSurvey.as_view(), name='new_form'),
    url(r'^(?P<slug>.*)/delete/$', DeleteSurvey.as_view(), name='delete_form'),
)
