from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import TickerHandler
from api.handlers import TargetPriceHandler
from api.handlers import TickerChangeHandler
from api.handlers import StockHandler

ticker_handler = Resource(TickerHandler)
target_price_handler = Resource(TargetPriceHandler)
ticker_change_handler = Resource(TickerChangeHandler)
stock_handler = Resource(StockHandler)

urlpatterns = patterns(
    '',
    url(r'^tickers/$', ticker_handler),
    url(r'^tickers/(?P<_ticker>[^/]+)/$', ticker_handler),
    url(r'^target_prices/$', target_price_handler),
    url(r'^ticker_changes/$', ticker_change_handler),
    url(r'^stocks/$', stock_handler)
)
