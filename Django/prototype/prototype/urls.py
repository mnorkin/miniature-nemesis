from django.conf.urls import patterns, include, url
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from api.handlers import FeatureAnalyticTickerHandler

auth = HttpBasicAuthentication(realm='morbid_realm')
ad = { 'authentication' : auth }

feature_analytic_ticker_resource = Resource(handler=FeatureAnalyticTickerHandler, **ad)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prototype.views.home', name='home'),
    url(r'^$', 'morbid.views.index'),
    url(r'^analytic/(?P<slug>[^/]+)/$', 'morbid.views.analytic'),
    url(r'^ticker/(?P<slug>[^/]+)/$', 'morbid.views.ticker'),

    url(r'^feature_by_ticker/(?P<slug>[^/]+)/(?P<feature_id>\d+)/$', 'morbid.views.feature_by_ticker'), # JSON only
    url(r'^feature_by_analytic/(?P<slug>[^/]+)/(?P<feature_id>\d+)/$', 'morbid.views.feature_by_analytic'), # JSON only
    url(r'^search/(?P<search_me>[^/]+)/$', 'morbid.views.search'), # JSON only

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # API
    # url(r'^api/feature_analytic_ticker/(?P<analytic_slug>[^/]+)/(?P<ticker_slug>[^/]+)/(?P<feature_id>\d+)/(?P<value>[^/]+)/$', feature_analytic_ticker_resource)
    url(r'^api/', include('api.urls'))
)
