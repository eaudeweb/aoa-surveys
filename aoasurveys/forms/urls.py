from django.conf.urls import patterns, url


urlpatterns = patterns('aoasurveys.forms.views',
    url(r'^(?P<slug>.*)/form/$', 'form_view', name='form_detail'),
)
