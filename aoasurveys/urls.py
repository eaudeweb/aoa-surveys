from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^forms/', include('aoasurveys.aoaforms.urls')),
    url(r'', include('aoasurveys.reports.urls')),
)
