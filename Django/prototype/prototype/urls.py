from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from api.handlers import FeatureAnalyticTickerHandler
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

auth = HttpBasicAuthentication(realm='morbid_realm')
ad = {'authentication': auth}

feature_analytic_ticker_resource = Resource(handler=FeatureAnalyticTickerHandler, **ad)

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^page/(?P<page>\d+)/$', 'morbid.views.index'),
    url(r'^testing/$', 'morbid.views.test'),
    url(r'^testing/(?P<ticker_slug>[\w-]+)$', 'morbid.views.test'),
    url(r'^testing/(?P<analytic_slug>[\w-]+)$', 'morbid.views.test'),
    url(r'^testing/(?P<ticker_slug>[\w-]+)/(?P<analytic_slug>[\w-]+)$', 'morbid.views.test'),
    url(r'^$', 'morbid.views.index'),

    url(r'^analytic/target_prices/(?P<analytic_slug>[^/]+)/$', 'morbid.views.target_prices'),
    url(r'^ticker/target_prices/(?P<ticker_slug>[^/]+)/$', 'morbid.views.target_prices'),
    url(r'^analytic/(?P<slug>[^/]+)/$', 'morbid.views.analytic'),
    url(r'^ticker/(?P<slug>[^/]+)/$', 'morbid.views.ticker'),
    url(r'^tickers/$', 'morbid.views.tickers'),
    url(r'^targets/(?P<sort_by>[^/]+)/(?P<sort_direction>[^/]+)$', 'morbid.views.target_prices_sort'),
    url(r'^targets/(?P<sort_by>[^/]+)/(?P<sort_direction>[^/]+)/(?P<page>\d+)/$', 'morbid.views.target_prices_sort'),
    url(r'^get_ticker_data/(?P<ticker>[^/]+)/$', 'morbid.views.ticker_data'),

    url(r'^subscribe/$', 'accounts.views.account_subscribe'),
    url(r'^thanks/$', 'accounts.views.account_subscribe_after'),

    url(r'^feature_by_ticker/(?P<slug>[^/]+)/(?P<feature_id>\d+)/$', 'morbid.views.feature_by_ticker'),  # JSON only
    url(r'^feature_by_analytic/(?P<slug>[^/]+)/(?P<feature_id>\d+)/$', 'morbid.views.feature_by_analytic'),  # JSON only
    url(r'^search/(?P<search_me>[^/]+)/$', 'morbid.views.search'),  # JSON only
    url(r'^test_page_search/(?P<search_me>[\w-]+)/$', 'morbid.views.test_page_search'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # API
    # url(r'^api/feature_analytic_ticker/(?P<analytic_slug>[^/]+)/(?P<ticker_slug>[^/]+)/(?P<feature_id>\d+)/(?P<value>[^/]+)/$', feature_analytic_ticker_resource)
    url(r'^api/', include('api.urls')),

    # Screen page
    url(r'^screen/$', 'morbid.views.screen')
)

# Statics (need for gunicorn)
urlpatterns += staticfiles_urlpatterns()
