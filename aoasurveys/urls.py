from django.conf.urls import patterns, include, url
import forms_builder.forms.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^forms/', include(forms_builder.forms.urls)),
    url(r'', include('aoasurveys.reports.urls')),
)
