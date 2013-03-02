from morbid.models import ApiKey, FeatureAnalyticTicker, Feature, TargetPrice, Ticker, Analytic, Unit
from piston.handler import BaseHandler
from piston.utils import rc, validate
from django.http import HttpResponse, Http404


class ApiKeyHandler(BaseHandler):
    """
    * TODO
    """
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
            # return HttpResponse(api_key)
            return api_key
        else:
            # Create API key
            api_key = ApiKey(user=request.user)
            api_key.save()
            return api_key
        #     # return HttpResponse(api_key)


class AnalyticHandler(BaseHandler):
    """
    Analytic data handler
    """

    allowed_methods = ('GET', 'POST', 'PUT')
    model = Analytic

    def read(self, request, analytic_slug=None):
        if analytic_slug:
            analytic = Analytic
            try:
                analytic = Analytic.objects.get(slug=analytic_slug)
                return analytic
            except analytic.DoesNotExist:
                raise Http404
        else:
            return Analytic.objects.all()

    def create(self, request):

        if request.content_type:
            data = request.data

            analytic = Analytic

            try:
                analytic = self.model.objects.get(slug=data['slug'])
                return rc.DUPLICATE_ENTRY
            except analytic.DoesNotExist:
                em = self.model(
                    name=data['name'],
                    number_of_companies=data['number_of_companies'],
                    number_of_tp=data['number_of_tp'],
                    volatility_positive=data['volatility_positive'],
                    volatility_negative=data['volatility_negative'],
                    last_target_price=data['last_target_price'],
                    slug=data['slug']
                )
                em.save()
                return rc.CREATED
        else:
            super(Analytic, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            em = self.model.objects.get(slug=data['slug'])

            em.name = data['name']
            em.number_of_companies = data['number_of_companies']
            em.number_of_tp = data['number_of_tp']
            em.volatility_positive = data['volatility_negative']
            em.last_target_price = data['last_target_price']

            em.save()

            return rc.ALL_OK
        else:
            super(Analytic, self).create(request)

    def delete(self, request):
        if request.content_type:
            data = request.data

            em = self.model.objects.get(slug=data['slug'])

            em.delete

            return rc.DELETED
        else:
            super(Analytic, self).create(request)


class TickerHandler(BaseHandler):
    """
    Ticker data handler
    """

    allowed_methods = ('GET', 'POST', 'PUT')
    model = Ticker

    def read(self, request, ticker_slug=None):
        if ticker_slug:
            return Ticker.objects.get(slug=ticker_slug)
        else:
            return Ticker.objects.all()

    def create(self, request):

        if request.content_type:

            data = request.data

            ticker = Ticker

            try:
                ticker = self.model.objects.get(slug=data['slug'])
                return rc.DUPLICATE_ENTRY
            except ticker.DoesNotExist:

                em = self.model(
                    name=data['name'],
                    long_name=data['long_name'],
                    last_stock_price=data['last_stock_price'],
                    number_of_analytics=data['number_of_analytics'],
                    number_of_tp=data['number_of_tp'],
                    consensus_min=data['consensus_min'],
                    consensus_avg=data['consensus_avg'],
                    consensus_max=data['consensus_max'],
                    slug=data['slug']
                )

                em.save()

            return rc.CREATED
        else:
            super(Ticker, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            try:
                em = self.model.objects.get(slug=data['slug'])
            except em.DoesNotExist:
                return rc.NOT_FOUND

            em.name = data['name']
            em.long_name = data['long_name']
            em.last_stock_price = data['last_stock_price']
            em.number_of_analytics = data['number_of_analytics']
            em.number_of_tp = data['number_of_tp']
            em.consensus_min = data['consensus_min']
            em.consensus_avg = data['consensus_avg']
            em.consensus_max = data['consensus_max']

            em.save()

            return rc.ALL_OK
        else:
            super(Ticker, self).create(request)

    def delete(self, request):
        rc.NOT_IMPLEMENTED


class TargetPriceHandler(BaseHandler):
    """
    Target price data handler
    """

    allowed_methods = ('GET', 'POST', 'PUT')
    model = TargetPrice

    def read(self, request, target_price_id=None):
        if target_price_id:
            return TargetPrice.objects.get(id=target_price_id)
        else:
            return TargetPrice.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data

            ticker = Ticker
            analytic = Analytic
            targetprice = TargetPrice

            try:
                ticker = Ticker.objects.get(slug=data['ticker_slug'])
            except ticker.DoesNotExist:
                return rc.NOT_FOUND

            try:
                analytic = Analytic.objects.get(slug=data['analytic_slug'])
            except analytic.DoesNotExist:
                return rc.NOT_FOUND

            try:
                targetprice = TargetPrice.objects.get(analytic=analytic, ticker=ticker, date=data['date'])
            except targetprice.DoesNotExist:

                em = self.model(
                    date=data['date'],
                    price=data['price'],
                    change=data['change'],
                    ticker=ticker,
                    analytic=analytic
                )
                em.save()

                return rc.CREATED

            return rc.DUPLICATE_ENTRY

        else:
            super(TargetPrice, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            ticker = Ticker
            analytic = Analytic

            try:
                ticker = Ticker.objects.get(slug=data['ticker_slug'])
            except ticker.DoesNotExist:
                return rc.NOT_FOUND

            try:
                analytic = Analytic.objects.get(slug=data['analytic_slug'])
            except analytic.DoesNotExist:
                return rc.NOT_FOUND

            try:
                em = self.model.objects.get(date=data['date'], analytic=analytic, ticker=ticker)
            except em.DoesNotExist:
                return rc.NOT_FOUND

            em.price = data['price']
            em.change = data['change']
            em.save()

            return rc.ALL_OK
        else:
            super(TargetPrice, self).create(request)

    def delete(self, request):
        rc.NOT_IMPLEMENTED


class UnitHandler(BaseHandler):
    """
    Units data handler
    """
    allowed_methods = ('GET', 'POST', 'PUT')
    model = Unit

    def read(self, request):
        return rc.NOT_IMPLEMENTED

    def create(self, request):
        if request.content_type:
            data = request.data

            em = self.model(
                id=data['unit_id'],
                name=data['name'],
                value=data['value']
            )
            em.save()

            return rc.CREATED
        else:
            super(Unit, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            em = self.model.objects.get(id=data['unit_id'])

            em.name = data['name']
            em.value = data['value']
            em.save()

            return rc.ALL_OK
        else:
            super(Unit, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTED


class FeatureHandler(BaseHandler):
    """
    Feature definition data handler
    """

    allowed_methods = ('GET', 'POST', 'PUT')
    model = Feature

    def read(self, request, feature_id=None):
        if feature_id:
            return Feature.objects.get(id=feature_id)
        else:
            return Feature.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data

            unit = Unit
            feature = Feature

            try:
                feature = Feature.objects.get(slug=data['feature_slug'])
            except feature.DoesNotExist:

                try:
                    unit = Unit.objects.get(id=data['unit_id'])
                except unit.DoesNotExist:
                    return rc.NOT_FOUND

                em = self.model(
                    name=data['name'],
                    unit=unit,
                    display_in_frontpage=data['display_in_frontpage'],
                    description=data['description'],
                    slug=data['feature_slug']
                )

                em.save()

                return rc.CREATED

            return rc.NOT_FOUND

        else:
            super(Feature, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            feature = Feature
            unit = Unit

            try:
                feature = Feature.objects.get(slug=data['feature_slug'])
            except feature.DoesNotExist:
                return rc.NOT_FOUND

            try:
                unit = Unit.objects.get(id=data['unit_id'])
            except unit.DoesNotExist:
                return rc.NOT_FOUND

            feature.name = data['name']
            feature.unit = unit
            feature.display_in_frontpage = data['display_in_frontpage']
            feature.description = data['description']

            feature.save()

            return rc.ALL_OK

        else:
            super(Feature, self).create(request)

    def delete(self, request):
        rc.NOT_IMPLEMENTED


class FeatureAnalyticTickerHandler(BaseHandler):
    """
    Values of features to specific ticker on analytic and vice versa data handler
    """
    allowed_methods = ('GET', 'POST', 'PUT')
    model = FeatureAnalyticTicker

    def read(self, request, feature_analytic_ticker_id=None):

        if feature_analytic_ticker_id:
            return FeatureAnalyticTicker.objects.get(id=feature_analytic_ticker_id)
        else:
            return FeatureAnalyticTicker.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data

            analytic = Analytic
            ticker = Ticker
            feature = Feature
            featureanalyticticker = FeatureAnalyticTicker

            try:
                analytic = Analytic.objects.get(slug=data['analytic_slug'])
            except analytic.DoesNotExist:
                return rc.NOT_FOUND

            try:
                ticker = Ticker.objects.get(slug=data['ticker_slug'])
            except ticker.DoesNotExist:
                return rc.NOT_FOUND

            try:
                feature = Feature.objects.get(slug=data['feature_slug'])
            except feature.DoesNotExist:
                return rc.NOT_FOUND

            try:
                featureanalyticticker = FeatureAnalyticTicker.objects.get(
                    analytic=analytic,
                    ticker=ticker,
                    feature=feature
                )
            except featureanalyticticker.DoesNotExist:

                em = self.model(
                    value=data['value'],
                    analytic=analytic,
                    ticker=ticker,
                    feature=feature
                )
                em.save()

                return rc.CREATED

            rc.DUPLICATE_ENTRY

        else:
            super(FeatureAnalyticTicker, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            analytic = Analytic
            ticker = Ticker
            feature = Feature

            featureanalyticticker = FeatureAnalyticTicker

            try:
                analytic = Analytic.objects.get(slug=data['analytic_slug'])
            except analytic.DoesNotExist:
                return rc.NOT_FOUND

            try:
                ticker = Ticker.objects.get(slug=data['ticker_slug'])
            except ticker.DoesNotExist:
                return rc.NOT_FOUND

            try:
                feature = Feature.objects.get(slug=data['feature_slug'])
            except feature.DoesNotExist:
                return rc.NOT_FOUND

            try:
                featureanalyticticker = FeatureAnalyticTicker.objects.get(
                    analytic=analytic,
                    ticker=ticker,
                    feature=feature
                )
            except featureanalyticticker.DoesNotExist:
                return rc.NOT_FOUND

            featureanalyticticker.value = data['value']

            featureanalyticticker.save()

            return rc.ALL_OK

        else:
            super(FeatureAnalyticTicker, self).create(request)

    def delete(self, request):
        rc.NOT_IMPLEMENTED
