from morbid.models import ApiKey, FeatureAnalyticTicker, Feature, TargetPrice, Ticker, Analytic
from piston.handler import BaseHandler
from piston.utils import rc, validate

class ApiKeyHandler(BaseHandler):
  model = ApiKey
  allowed_methods = ('GET', 'POST')
  fields = ('user', 'key')

  def read(self, request):
    # Read Key from the request.user
    values_query_set = request.user.keys.values('key')
    api_key = list(values_query_set)[0]['key']
    return HttpResponse(api_key)

  def create(self, request):
    if request.user.keys.count() > 0:
      # Check if key exists
      values_query_set = request.user.keys.values('key')
      api_key = list(values_query_set)[0]['key']
      return HttpResponse(api_key)
    else:
      # Create API key
      api_key = ApiKey(user=request.user)
      api_key.save()
    return HttpResponse(api_key)

    

class AnalyticHandler(BaseHandler):

  allowed_methods = ('GET', 'POST')
  model = Analytic

  def read(self, request, analytic_slug=None):
    if analytic_slug:
      return Analytic.objects.get(slug=analytic_slug)
    else:
      return Analytic.objects.all()

  def create(self, request):
    if request.content_type:
      data = request.data

      em = self.model(name=data['name'], 
        number_of_companies=data['number_of_companies'],
        number_of_tp=data['number_of_tp'],
        volatility=data['volatility'],
        last_target_price=data['last_target_price'],
        slug=data['slug'])

      em.save()

      return rc.CREATED
    else:
      super(Analytic, self).create(request)

  def update(self, request):
    pass

  def delete(self, request):
    pass

class TickerHandler(BaseHandler):

  allowed_methods = ('GET', 'POST')
  model = Ticker

  def read(self, request, ticker_slug=None):
    if ticker_slug:
      return Ticker.objects.get(slug=ticker_slug)
    else:
      return Ticker.objects.all()

  def create(self, request):
    if request.content_type:
      data = request.data

      em = self.model(name=data['name'],
        long_name=data['long_name'],
        last_stock_price=data['last_stock_price'],
        number_of_analytics=data['number_of_analytics'],
        number_of_tp=data['number_of_tp'],
        consensus_min=data['consensus_min'],
        consensus_avg=data['consensus_avg'],
        consensus_max=data['consensus_max'],
        slug=data['slug'])

      em.save()

      return rc.CREATED
    else:
      super(Ticker, self).create(request)

  def update(self, request):
    pass

  def delete(self, request):
    pass

class TargetPriceHandler(BaseHandler):

  allowed_methods = ('GET', 'POST')
  model = TargetPrice

  def read(self, request, target_price_id=None):
    if target_price_id:
      return TargetPrice.objects.get(id=target_price_id)
    else:
      return TargetPrice.objects.all()

  def create(self, request):
    if request.content_type:
      data = request.data

      ticker_instance = Ticker.objects.get(slug=data['ticker_slug'])
      analytic_instance = Analytic.objects.get(slug=data['analytic_slug'])

      em = self.model(date=data['date'],
        price=data['price'],
        ticker=ticker_instance.id,
        analytic=analytic_instance.id)

      em.save()

      return rc.CREATED
    else:
      super(TargetPrice, self).create(request)

  def update(self, request):
    pass

  def delete(self, request):
    pass

class FeatureHandler(BaseHandler):

  allowed_methods = ('GET', 'POST')
  model = Feature

  def read(self, request, feature_id=None):
    if feature_id:
      return Feature.objects.get(id=feature_id)
    else:
      return Feature.objects.all()

  def create(self, request):
    if request.content_type:
      data = request.data

      em = self.model(name=data['name'],
        unit=data['unit'], # FIXME: Change this buddy to id
        display_in_frontpage=data['display_in_frontpage'],
        description=data['description'] 
        )

      em.save()

      return rc.CREATED

    else:
      super(Feature, self).create(request)

  def update(self, request):
    pass

  def delete(self, request):
    pass

class FeatureAnalyticTickerHandler(BaseHandler):
  allowed_methods = ('GET', 'POST', 'PUT')
  model = FeatureAnalyticTicker

  def read(self, request, feature_analytic_ticker_id):
    if feature_analytic_ticker_id:
      return FeatureAnalyticTicker.objects.get(id=feature_analytic_ticker_id)
    else:
      return FeatureAnalyticTicker.objects.all()

  def create(self, request):
    if request.content_type:
      data = request.data

      analytic_instance = Analytic.objects.get(slug=data['analytic_slug'])
      ticker_instance = Ticker.objects.get(slug=data['ticker_slug'])

      em = self.model(value=data['value'],
        feature=data['feature'],
        analytic=analytic_instance.id,
        ticker=ticker_instance.id)

      em.save()

      return rc.CREATED

    else:
      super(FeatureAnalyticTicker, self).create(request)

  def update(self, request):
    pass

  def delete(self, request):
    pass