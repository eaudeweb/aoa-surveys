from django.conf.urls import patterns, url
from aoasurveys.mapapi.views import json_map

urlpatterns = patterns(
    '',
    url('jsmap_search_map_documents/', json_map, name='json_map'),
)