from aoasurveys.reports.views import FormsIndex, AnswersView
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', FormsIndex.as_view()),
    url(r'^(?P<slug>.*)/answers/$', AnswersView.as_view(), name='answers_list'),
)
