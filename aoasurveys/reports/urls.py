from aoasurveys.reports.views import FormsIndex
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', FormsIndex.as_view()),
)
