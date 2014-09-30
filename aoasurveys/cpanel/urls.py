from django.conf.urls import patterns, url
from aoasurveys.cpanel.views import RolesOverview, index_view

urlpatterns = patterns(
    '',
    url(r'^$', index_view, name='index'),
    url(r'^roles/$', RolesOverview.as_view(), name='roles'),
)
