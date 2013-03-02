from apikey.auth import ApiKeyAuthentication
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import AnalyticHandler, TickerHandler, TargetPriceHandler, FeatureHandler, FeatureAnalyticTickerHandler, ApiKeyHandler, UnitHandler

# feature_analytic_ticker_handler = Resource(FeatureAnalyticTickerHandler, authentication=ApiKeyAuthentication())
feature_analytic_ticker_handler = Resource(FeatureAnalyticTickerHandler)
# analytic_handler = Resource(AnalyticHandler, authentication=ApiKeyAuthentication())
analytic_handler = Resource(AnalyticHandler)
# ticker_handler = Resource(TickerHandler, authentication=ApiKeyAuthentication())
ticker_handler = Resource(TickerHandler)
# target_price_handler = Resource(TargetPriceHandler, authentication=ApiKeyAuthentication())
target_price_handler = Resource(TargetPriceHandler)
# feature_handler = Resource(FeatureHandler, authentication=ApiKeyAuthentication())
feature_handler = Resource(FeatureHandler)
# unit_handler = Resource(UnitHandler, authentication=ApiKeyAuthentication())
unit_handler = Resource(UnitHandler)
apikey_handler = Resource(ApiKeyHandler)

urlpatterns = patterns(
    '',
    url(r'^feature_analytic_tickers/$', feature_analytic_ticker_handler),
    url(r'^analytics/$', analytic_handler),
    url(r'^analytics/(?P<analytic_slug>[^/]+)/$', analytic_handler),
    url(r'^tickers/$', ticker_handler),
    url(r'^tickers/(?P<ticker_slug>[^/]+)/$', ticker_handler),
    url(r'^target_prices/$', target_price_handler),
    url(r'^target_prices/(?P<target_price_id>\d+)/$', target_price_handler),
    url(r'^features/$', feature_handler),
    url(r'^features/(?P<feature_id>\d+)/$', feature_handler),
    url(r'^units/$', unit_handler),
    url(r'^apikeys/', apikey_handler)
)
