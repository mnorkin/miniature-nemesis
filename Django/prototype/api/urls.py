from apikey.auth import ApiKeyAuthentication
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import AnalyticHandler, TickerHandler, TargetPriceHandler, FeatureHandler, FeatureAnalyticTickerHandler

feature_analytic_ticker_handler = Resource(FeatureAnalyticTickerHandler, authentication=ApiKeyAuthentication())
analytic_handler = Resource(AnalyticHandler, authentication=ApiKeyAuthentication())
ticker_handler = Resource(TickerHandler, authentication=ApiKeyAuthentication())
target_price_handler = Resource(TargetPriceHandler, authentication=ApiKeyAuthentication())
feature_handler = Resource(FeatureHandler, authentication=ApiKeyAuthentication())

urlpatterns = patterns('',
  url(r'^feature_analytic_ticker/', feature_analytic_ticker_handler),
  url(r'^analytic/', analytic_handler),
  url(r'^ticker/', ticker_handler),
  url(r'^target_price/', target_price_handler),
  url(r'^feature/', feature_handler)
)