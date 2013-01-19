from django.conf.urls import patterns, include, url

urlpatterns = patterns('morbid.views',
	url(r'^$', 'index'),
	url(r'^analytic/(?P<slug>\w+)/$', 'analytic'),
	url(r'^ticket/(?P<slug>\w+)/$', 'ticket'),

	url(r'^feature_by_ticket/(?P<slug>\w+)/(?P<feature_id>\d+)/$', 'feature_by_ticket'), # JSON only
	url(r'^feature_by_analytic/(?P<slug>\w+)/(?P<feature_id>\d+)/$', 'feature_by_analytic'), # JSON only
)