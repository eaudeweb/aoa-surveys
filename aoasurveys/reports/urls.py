from aoasurveys.reports.views import (
    FormsIndex, AnswersView, file_view, FormExtraView,
)
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', FormsIndex.as_view(), name='homepage'),
    url(r'^(?P<slug>.*)/answers/$', AnswersView.as_view(),
        name='answers_list'),
    url(r'^(?P<slug>.*)/manage/$', FormExtraView.as_view(),
        name='manage_form'),
    url(r'^file/(?P<field_entry_id>.*)/$', file_view, name='file_view'),
)
