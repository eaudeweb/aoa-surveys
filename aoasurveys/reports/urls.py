from django.conf.urls import patterns, url

from aoasurveys.reports.views import FormsIndex, AnswersView, file_view

urlpatterns = patterns('',
    url(r'^$', FormsIndex.as_view(), name='homepage'),
    url(r'^(?P<slug>.*)/answers/$', AnswersView.as_view(),
        name='answers_list'),
    url(r'^file/(?P<field_entry_id>.*)/$', file_view, name='file_view'),
)
