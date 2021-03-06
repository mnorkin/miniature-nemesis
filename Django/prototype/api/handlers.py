from morbid.models import ApiKey
from morbid.models import FeatureAnalyticTicker
from morbid.models import FeatureAnalyticTickerCheck
from morbid.models import TargetPriceAnalyticTicker
from morbid.models import Feature
from morbid.models import TargetPrice
from morbid.models import Ticker
from morbid.models import Analytic
from morbid.models import Unit
from morbid.models import Volatility
from morbid.models import TargetPriceNumberAnalyticTicker
from morbid.utils import stock_data
from morbid.utils import target_data
from piston.handler import BaseHandler
from piston.utils import rc
from piston.utils import validate
from django.http import HttpResponse, Http404


class StockHandler(BaseHandler):
    """
    The yahoo stock handler
    """

    def read(self, request, ticker_slug=None):
        if ticker_slug:
            ticker = Ticker.objects.get(slug=ticker_slug)
            return stock_data(ticker.name)
        else:
            return rc.NOT_IMPLEMENTED

    def create(self, request):
        return rc.NOT_IMPLEMENTED

    def update(self, request):
        return rc.NOT_IMPLEMENTED

    def delete(self, request):
        return rc.NOT_IMPLEMENTED


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


class TargetPriceAnalyticTickerHandler(BaseHandler):
    """
    Keeping record of what features are stored on which target price record from
    the crawler
    """
    model = TargetPriceAnalyticTicker

    def read(self, request):
        """
        Returning all the calculated records
        """
        if request.content_type:
            targetpriceanalyticticker = TargetPriceAnalyticTicker
            analytic = Analytic
            ticker = Ticker
            data = request.data
            try:
                try:
                    analytic = Analytic.objects.get(
                        analytic_name=data['analytic']
                    )
                except analytic.DoesNotExist:
                    return rc.NOT_FOUND

                try:
                    ticker = Ticker.objects.get(
                        ticker_name=data['ticker']
                    )
                except ticker.DoesNotExist:
                    return rc.NOT_FOUND

                targetpriceanalyticticker.objects.get(
                    analytic=analytic,
                    ticker=ticker,
                    date=data['date']
                )
                return rc.ALL_OK
            except targetpriceanalyticticker.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return TargetPriceAnalyticTicker.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data
            _analytic = Analytic
            _ticker = Ticker
            targetpriceanalyticticker = TargetPriceAnalyticTicker

            try:
                _analytic = Analytic.objects.get(
                    name=data['analytic']
                )
            except _analytic.DoesNotExist:
                return rc.NOT_FOUND

            try:
                _ticker = Ticker.objects.get(
                    name=data['ticker']
                )
            except _ticker.DoesNotExist:
                return rc.NOT_FOUND

            try:
                targetpriceanalyticticker = TargetPriceAnalyticTicker.objects.get(
                    analytic=_analytic,
                    ticker=_ticker,
                    date=data['date']
                )
                return rc.CREATED
            except targetpriceanalyticticker.DoesNotExist:
                return rc.NOT_FOUND

        else:
            super(TargetPriceAnalyticTicker, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data
            targetpriceanalyticticker = TargetPriceAnalyticTicker(
                analytic=Analytic.objects.get(name=data['analytic']),
                ticker=Ticker.objects.get(name=data['ticker']),
                date=data['date']
            )
            targetpriceanalyticticker.save()
            return rc.ALL_OK
        else:
            super(TargetPriceAnalyticTicker, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTED


class TargetPriceNumberAnalyticTickerHandler(BaseHandler):
    """
    Number of Target prices for the ticker by the Analytic
    """

    model = TargetPriceNumberAnalyticTicker

    def read(self, request, analytic_slug=None, ticker_slug=None):
        if analytic_slug and ticker_slug:
            tpnat = TargetPriceNumberAnalyticTicker.get(
                analytic=Analytic.objects.get(slug=analytic_slug),
                ticker=Ticker.objects.get(slug=ticker_slug))
            return tpnat
        else:
            return TargetPriceNumberAnalyticTicker.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data
            tpnat = TargetPriceNumberAnalyticTicker
            try:
                tpnat = self.model.objects.get(
                    analytic=Analytic.objects.get(slug=data['analytic_slug']),
                    ticker=Ticker.objects.get(slug=data['ticker_slug']))
                return rc.DUPLICATE_ENTRY
            except tpnat.DoesNotExist:
                em = self.model(
                    analytic=Analytic.objects.get(slug=data['analytic_slug']),
                    ticker=Ticker.objects.get(slug=data['ticker_slug']),
                    number=data['number'])
                em.save()
                return rc.CREATED
        else:
            super(TargetPriceNumberAnalyticTicker, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data
            em = self.model.objects.get(
                analytic=Analytic.objects.get(slug=data['analytic_slug']),
                ticker=Ticker.objects.get(slug=data['ticker_slug']))
            em.number = data['number']
            em.save()
            return rc.ALL_OK
        else:
            super(TargetPriceNumberAnalyticTicker, self).create(request)

    def delete(self, request, analytic_slug=None, ticker_slug=None):
        if analytic_slug and ticker_slug:
            em = self.model.objects.get(
                analytic=Analytic.objects.get(slug=analytic_slug),
                ticker=Ticker.objects.get(slug=ticker_slug))
            em.delete()
            return rc.DELETED
        else:
            super(TargetPriceNumberAnalyticTicker, self).create(request)


class VolatilityHandler(BaseHandler):
    """
    Volatility Handler
    """
    model = Volatility

    def read(self, request, analytic_slug=None, ticker_slug=None):
        if analytic_slug and ticker_slug:
            volatility = Volatility.objects.get(
                analytic=Analytic.objects.get(slug=analytic_slug),
                ticker=Ticker.objects.get(slug=ticker_slug))
            return volatility
        else:
            return Volatility.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data
            volatility = Volatility
            try:
                volatility = self.model.objects.get(
                    analytic=Analytic.objects.get(slug=data['analytic_slug']),
                    ticker=Ticker.objects.get(slug=data['ticker_slug']))
                return rc.DUPLICATE_ENTRY
            except volatility.DoesNotExist:
                em = self.model(
                    analytic=Analytic.objects.get(slug=data['analytic_slug']),
                    ticker=Ticker.objects.get(slug=data['ticker_slug']),
                    total=data['total'],
                    number=data['number'])
                em.save()
                return rc.CREATED

        else:
            super(Volatility, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data
            em = self.model.objects.get(
                analytic=Analytic.objects.get(slug=data['analytic_slug']),
                ticker=Ticker.objects.get(slug=data['ticker_slug']))
            em.number = data['number']
            em.total = data['total']
            em.save()
            return rc.ALL_OK
        else:
            super(Volatility, self).create(request)

    def delete(self, request, analytic_slug=None, ticker_slug=None):
        if analytic_slug and ticker_slug:
            em = self.model.objects.get(
                analytic=Analytic.objects.get(slug=analytic_slug),
                ticker=Ticker.objects.get(slug=ticker_slug))
            em.delete()
            return rc.DELETED
        else:
            super(Volatility, self).create(request)


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

            em.save()

            return rc.ALL_OK
        else:
            super(Analytic, self).create(request)

    def delete(self, request):
        if request.content_type:
            data = request.data

            em = self.model.objects.get(slug=data['slug'])

            em.delete()

            return rc.DELETED
        else:
            super(Analytic, self).create(request)


class StockPriceHandler(BaseHandler):
    """
    Stock price handler
    """

    allowed_methods = ('PUT')
    model = Ticker

    def read(self, request):
        return rc.NOT_IMPLEMENTED

    def create(self, request):
        return rc.NOT_IMPLEMENTED

    def update(self, request):
        if request.content_type:
            data = request.data
            # Ticker part
            ticker = Ticker
            try:
                ticker = Ticker.objects.get(name=data['ticker'])
            except ticker.DoesNotExist:
                return rc.NOT_FOUND

            ticker.last_stock_price = data['last_stock_price']
            ticker.last_stock_change = data['last_stock_change']
            ticker.save()

            # TP part
            target_prices = TargetPrice.objects.filter(ticker=ticker)
            for target in target_prices:
                if data['last_stock_price'] != 0:
                    target.change = round(
                        float(
                            target.price - data['last_stock_price'])/target.price*100*10)/10
                    target.save()
                else:
                    target.change = 0.00
                    target.save()

            return rc.ALL_OK
        else:
            super(Ticker, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTED


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
            return Ticker.objects.with_display()

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
                    last_stock_change=0,
                    consensus_min=data['consensus_min'],
                    consensus_avg=data['consensus_avg'],
                    consensus_max=data['consensus_max'],
                    slug=data['slug'],
                    display=data['display']
                )

                em.save()

            return rc.CREATED
        else:
            super(Ticker, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            ticker = Ticker

            try:
                if 'slug' in data:
                    ticker = Ticker.objects.get(slug=data['slug'])
                if 'name' in data:
                    ticker = Ticker.objects.get(name=data['name'])
            except ticker.DoesNotExist:
                return rc.NOT_FOUND

            if 'name' in data:
                ticker.name = data['name']
            if 'long_name' in data:
                ticker.long_name = data['long_name']
            if 'last_stock_price' in data:
                ticker.last_stock_price = data['last_stock_price']
            if 'last_stock_change' in data:
                ticker.last_stock_change = data['last_stock_change']
            if 'consensus_min' in data:
                ticker.consensus_min = data['consensus_min']
            if 'consensus_avg' in data:
                ticker.consensus_avg = data['consensus_avg']
            if 'consensus_max' in data:
                ticker.consensus_max = data['consensus_max']

            ticker.save()

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

    def read(
        self, 
        request,
        ticker_slug=None, 
        analytic_slug=None,
        page=0, 
        sort_by=None, 
        sort_direction=None
    ):

        if ticker_slug and sort_by and sort_direction:
            """
            Ticker, sort, direction
            """
            return TargetPrice.objects.sorted_ticker_target_prices(
                ticker_slug, 
                sort_by, 
                sort_direction, 
                page
            )
        elif analytic_slug and sort_by and sort_direction:
            """
            Analytic, sort, direction
            """
            return TargetPrice.objects.sorted_analytic_target_prices(
                analytic_slug, 
                sort_by, 
                sort_direction, 
                page
            )
        elif ticker_slug and analytic_slug:
            """
            Ticker, Analytic
            """
            ticker = Ticker.objects.get(slug=ticker_slug)
            analytic = Analytic.objects.get(slug=analytic_slug)
            return target_data(
                ticker.name, 
                analytic.name
            )
        elif ticker_slug and not analytic_slug:
            """
            Only ticker
            """
            return TargetPrice.objects.ticker_target_prices(
                ticker_slug, 
                page
            )
        elif not ticker_slug and analytic_slug:
            """
            Only Analytic
            """
            return TargetPrice.objects.analytic_target_prices(
                analytic_slug, 
                page
            )
        elif sort_by and sort_direction:
            """
            Only sort
            """
            return TargetPrice.objects.sorted(
                sort_by, 
                sort_direction, 
                page
            )
        else:
            """
            Default
            """
            return TargetPrice.objects.recent_target_prices(page)

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
                targetprice = TargetPrice.objects.get(
                    analytic=analytic,
                    ticker=ticker,
                    date=data['date']
                )
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
                    position=data['position'],
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
            feature.position = data['position']

            feature.save()

            return rc.ALL_OK

        else:
            super(Feature, self).create(request)

    def delete(self, request):
        rc.NOT_IMPLEMENTED


class FeatureAnalyticTickerCheckHandler(BaseHandler):
    """
    Testing platform for the feature analytic ticker
    """
    allowed_methods = ('GET', 'POST')
    model = FeatureAnalyticTickerCheck

    def read(self, request):
        return FeatureAnalyticTickerCheck.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data
            print data

            analytic = Analytic
            ticker = Ticker
            feature = Feature
            featureanalyticticker = FeatureAnalyticTicker

            try:
                analytic = Analytic.objects.get(name=data['analytic'])
            except analytic.DoesNotExist:
                return rc.NOT_FOUND

            try:
                ticker = Ticker.objects.get(name=data['ticker'])
            except ticker.DoesNotExist:
                return rc.NOT_FOUND

            try:
                feature = Feature.objects.get(slug=data['feature'])
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

            em = self.model(
                feature_analytic_ticker=featureanalyticticker,
                value=data['value']
            )

            em.save()
            return rc.CREATED
        else:
            super(FeatureAnalyticTickerCheck, self).create(request)

    def update(self, request):
        return rc.NOT_IMPLEMENTED

    def delete(self, request):
        return rc.NOT_IMPLEMENTED


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
