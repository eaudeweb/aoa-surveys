from django.conf.urls import patterns, url

from aoasurveys.manager.views import (
    FormPropertiesView, FormFieldsView, FormVisibleFieldsView,
    FormFilterFieldsView, FieldsOrderView, CreateSurvey, DeleteSurvey,
    DeleteField, EditField, CreateField, CreateLabel, EditLabel, DeleteLabel,
)

urlpatterns = patterns('',
    url(r'^(?P<formslug>.*)/delete-field/(?P<pk>.*)/$', DeleteField.as_view(),
        name='delete_field'),
    url(r'^(?P<formslug>.*)/delete-label/(?P<pk>.*)/$', DeleteLabel.as_view(),
        name='delete_label'),
    url(r'^(?P<formslug>.*)/edit-field/(?P<pk>.*)/$', EditField.as_view(),
        name='edit_field'),
    url(r'^(?P<formslug>.*)/edit-label/(?P<pk>.*)/$', EditLabel.as_view(),
        name='edit_label'),
    url(r'^(?P<formslug>.*)/new-field/$', CreateField.as_view(),
        name='new_field'),
    url(r'^(?P<formslug>.*)/new-label/$', CreateLabel.as_view(),
        name='new_label'),
    url(r'^(?P<slug>.*)/properties/$', FormPropertiesView.as_view(),
        name='manage_properties'),
    url(r'^(?P<slug>.*)/fields/$', FormFieldsView.as_view(),
        name='manage_fields'),
    url(r'^(?P<slug>.*)/visible-fields/$', FormVisibleFieldsView.as_view(),
        name='manage_visible_fields'),
    url(r'^(?P<slug>.*)/filter-fields/$', FormFilterFieldsView.as_view(),
        name='manage_filter_fields'),
    url(r'^(?P<slug>.*)/(?P<tab>.*)/order/$', FieldsOrderView.as_view(),
        name='order_fields'),
    url(r'^new-form/$', CreateSurvey.as_view(), name='new_form'),
    url(r'^(?P<slug>.*)/delete/$', DeleteSurvey.as_view(), name='delete_form'),
)
