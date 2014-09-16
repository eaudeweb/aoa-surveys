from django.conf.urls import patterns, url


urlpatterns = patterns('aoasurveys.aoaforms.views',
    url(r'^(?P<slug>.*)/form/$', 'form_view', name='form_detail'),
)
