from django.conf.urls import patterns, url

from aoasurveys.manager.views import (
    FormPropertiesView, FormFieldsView, FormVisibleFieldsView,
    FormFilterFieldsView, FieldsOrderView, CreateSurvey, DeleteSurvey,
    DeleteField,
)

urlpatterns = patterns('',
    url(r'^(?P<formslug>.*)/(?P<pk>.*)/delete/$', DeleteField.as_view(),
        name='delete_field'),
    url(r'^(?P<slug>.*)/properties/$', FormPropertiesView.as_view(),
        name='manage_properties'),
    url(r'^(?P<slug>.*)/fields/$', FormFieldsView.as_view(),
        name='manage_fields'),
    url(r'^(?P<slug>.*)/visiblefields/$', FormVisibleFieldsView.as_view(),
        name='manage_visible_fields'),
    url(r'^(?P<slug>.*)/filterfields/$', FormFilterFieldsView.as_view(),
        name='manage_filter_fields'),
    url(r'^(?P<slug>.*)/(?P<tab>.*)/order/$', FieldsOrderView.as_view(),
        name='order_fields'),
    url(r'^new_form/$', CreateSurvey.as_view(), name='new_form'),
    url(r'^(?P<slug>.*)/delete/$', DeleteSurvey.as_view(), name='delete_form'),
)
