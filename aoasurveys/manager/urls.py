from django.conf.urls import patterns, url

from aoasurveys.manager.views import FormManagementView

urlpatterns = patterns('',
    url(r'^(?P<slug>.*)/$', FormManagementView.as_view(), name='manage_form'),
)
