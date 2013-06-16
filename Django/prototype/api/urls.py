from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_control
from piston.resource import Resource
from api.handlers import AnalyticHandler
from api.handlers import TickerHandler
from api.handlers import TargetPriceHandler
from api.handlers import FeatureHandler
from api.handlers import FeatureAnalyticTickerHandler
from api.handlers import FeatureAnalyticTickerCheckHandler
from api.handlers import ApiKeyHandler
from api.handlers import UnitHandler
from api.handlers import TargetPriceNumberAnalyticTickerHandler
from api.handlers import VolatilityHandler
from api.handlers import StockPriceHandler
from api.handlers import TargetPriceAnalyticTickerHandler
from api.handlers import StockHandler

cached_resource = cache_control(public=True, maxage=30, s_maxage=300)

# feature_analytic_ticker_handler = Resource(FeatureAnalyticTickerHandler, authentication=ApiKeyAuthentication())
feature_analytic_ticker_handler = Resource(FeatureAnalyticTickerHandler)

feature_analytic_ticker_check_handler = Resource(FeatureAnalyticTickerCheckHandler)
# analytic_handler = Resource(AnalyticHandler, authentication=ApiKeyAuthentication())
analytic_handler = Resource(AnalyticHandler)
# ticker_handler = Resource(TickerHandler, authentication=ApiKeyAuthentication())
ticker_handler = Resource(TickerHandler)
# target_price_handler = Resource(TargetPriceHandler, authentication=ApiKeyAuthentication())
target_price_handler = cached_resource(Resource(TargetPriceHandler))
# feature_handler = Resource(FeatureHandler, authentication=ApiKeyAuthentication())
feature_handler = Resource(FeatureHandler)
# unit_handler = Resource(UnitHandler, authentication=ApiKeyAuthentication())
unit_handler = Resource(UnitHandler)
tpnat_handler = Resource(TargetPriceNumberAnalyticTickerHandler)
volatility_handler = Resource(VolatilityHandler)
apikey_handler = Resource(ApiKeyHandler)
stock_price_handler = Resource(StockPriceHandler)
stock_handler = Resource(StockHandler)
target_price_analytic_ticker = Resource(TargetPriceAnalyticTickerHandler)

urlpatterns = patterns(
    '',
    url(r'^stock_prices/$', stock_price_handler),
    url(r'^stocks/(?P<ticker_slug>[\w-]+)/$', stock_handler),
    url(r'^feature_analytic_tickers/$', feature_analytic_ticker_handler),
    url(r'^analytics/$', analytic_handler),
    url(r'^analytics/(?P<analytic_slug>[\w-]+)/$', analytic_handler),
    url(r'^tickers/$', ticker_handler),
    url(r'^tickers/(?P<ticker_slug>[\w-]+)/$', ticker_handler),
    url(r'^target_prices/$', target_price_handler),
    url(
        r'^target_prices/(?P<ticker_slug>[\w-]+)/(?P<analytic_slug>[\w-]+)/$',
        target_price_handler
    ),
    url(
        r'^target_prices/(?P<page>\d+)/$',
        target_price_handler
    ),
    url(
        r'^target_prices/(?P<sort_by>[\w-]+)/(?P<sort_direction>[\w-]+)/(?P<page>\d+)/$',
        target_price_handler
    ),
    url(r'^features/$', feature_handler),
    url(r'^features/(?P<feature_id>\d+)/$', feature_handler),
    url(r'^check/$', feature_analytic_ticker_check_handler),
    url(r'^units/$', unit_handler),
    url(r'^apikeys/$', apikey_handler),
    url(r'^volatilities/$', volatility_handler),
    url(r'^volatilities/(?P<analytic_slug>[\w-]+)/(?P<ticker_slug>[\w-]+)/$', volatility_handler),
    url(r'^target_price_numbers/$', tpnat_handler),
    url(r'^target_price_numbers/(?P<analytic_slug>[\w-]+)/(?P<ticker_slug>[\w-]+)/$', tpnat_handler),
    url(r'^target_price_analytic_ticker/$', target_price_analytic_ticker)
)
