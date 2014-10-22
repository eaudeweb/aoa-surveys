from django.conf.urls import patterns, url

from aoasurveys.manager.views import (
    FormPropertiesView, FormFieldsView, FormVisibleFieldsView,
    FormFilterFieldsView, FieldsOrderView,
)

urlpatterns = patterns('',
    url(r'^(?P<slug>.*)/properties/$', FormPropertiesView.as_view(),
        name='manage_properties'),
    url(r'^(?P<slug>.*)/fields/$', FormFieldsView.as_view(),
        name='manage_fields'),
    url(r'^(?P<slug>.*)/visiblefields/$', FormVisibleFieldsView.as_view(),
        name='manage_visible_fields'),
    url(r'^(?P<slug>.*)/filterfields/$', FormFilterFieldsView.as_view(),
        name='manage_filter_fields'),
    url(r'^(?P<slug>.*)/orderfields/$', FieldsOrderView.as_view(),
        name='order_fields'),
)
