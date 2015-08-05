from django.conf.urls import patterns, url

from aoasurveys.reports.views import (
    FormsIndex, AnswersView, file_view, AnswersListJson,
    EntryDetail, AnswerDelete,
)

urlpatterns = patterns('',
    url(r'^$', FormsIndex.as_view(), name='homepage'),
    url(r'^(?P<slug>.*)/answers/$', AnswersView.as_view(),
        name='answers_list'),
    url(r'^(?P<slug>.*)/data/$', AnswersListJson.as_view(),
        name='answers_data'),
    url(r'^(?P<slug>.*)/delete_answer/(?P<pk>.*)/$', AnswerDelete.as_view(),
        name='delete_answer'),
    url(r'^file/(?P<field_entry_id>.*)/$', file_view, name='file_view'),

    url(r'^entry/(?P<id>\d+)/$', EntryDetail.as_view(),
        name='entry-detail')
)
