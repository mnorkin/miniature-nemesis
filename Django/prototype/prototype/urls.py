from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prototype.views.home', name='home'),
    url(r'^$', 'morbid.views.index'),
    url(r'^analytic/(?P<slug>.+)/$', 'morbid.views.analytic'),
    url(r'^ticker/(?P<slug>.+)/$', 'morbid.views.ticker'),

    url(r'^feature_by_ticker/(?P<slug>.+)/(?P<feature_id>\d+)/$', 'morbid.views.feature_by_ticker'), # JSON only
    url(r'^feature_by_analytic/(?P<slug>.+)/(?P<feature_id>\d+)/$', 'morbid.views.feature_by_analytic'), # JSON only
    url(r'^search/(?P<search_me>.+)/$', 'morbid.views.search'), # JSON only

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
