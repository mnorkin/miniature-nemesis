from sink.models import Ticker
from sink.models import TargetPrice
from sink.models import TickerChange
from sink.models import Market
from sink.models import Analytic
from sink.models import Stock
from piston.handler import BaseHandler
from piston.utils import require_mime
from piston.utils import rc
from django.http import Http404


class StockHandler(BaseHandler):

    model = Stock

    def read(self, request):
        """
        Returning the stock list, which is required
        """
        return Ticker.objects.all()

    @require_mime('json')
    def create(self, request):
        if request.content_type:
            data = request.data

            ticker = Ticker
            try:
                ticker = Ticker.objects.get(ticker=data['ticker'])
            except ticker.DoesNotExist:
                return rc.NOT_FOUND
            em = self.model(
                ticker=ticker,
                date=data['date'],
                price_open=data['price_open'],
                price_close=data['price_close'],
                price_high=data['price_high'],
                price_low=data['price_low']
            )
            em.save()

            return rc.CREATED
        else:
            super(Stock, self).create(request)

    def update(self, request):
        return rc.NOT_IMPLEMENTED

    def delete(self, request):
        return rc.NOT_IMPLEMENTED


class TickerHandler(BaseHandler):
    """
    Ticker data handler
    """
    allowed_methods = ('GET', 'POST', 'PUT')
    model = Ticker

    def read(self, request, _ticker=None):
        """
        Read if the Ticker does exists in the database
        """
        # return request.data
        # if request.content_type:
        # data = request.data

        ticker = Ticker
        target_price = TargetPrice
        if _ticker is not None:
            try:
                ticker = self.model.objects.get(ticker=_ticker)
                """
                If ticker exists, check if we have any data
                """

                target_price = TargetPrice.objects.filter(ticker=ticker)

                if len(target_price) < 10:
                    """
                    We have no data of this ticket, feed me
                    """
                    return rc.ALL_OK
                else:
                    """
                    We have some data, don't need anything to send
                    """
                    return rc.CREATED

            except ticker.DoesNotExist:
                return rc.NOT_FOUND
        else:
            having_tickers = TargetPrice.objects.values_list(
                'ticker__ticker',
                flat=True
            ).distinct('ticker__ticker')
            ticker = Ticker.objects.exclude(ticker__in=having_tickers).order_by('?')[0]
            return ticker
        # super(Ticker, self).create(request)

        # else:
            # super(Ticker, self).create(request)

    def create(self, request):
        if request.content_type:
            data = request.data

            ticker = Ticker

            """
            Ticker add logic
            """
            try:
                ticker = self.model.objects.get(ticker=data['ticker'])
                return rc.DUPLICATE_ENTRY
            except ticker.DoesNotExist:
                market = Market

                """
                Market logic
                """
                try:
                    market = Market.objects.get(name=data['market'])
                except market.DoesNotExist:
                    em = Market(name=data['market'])
                    em.save()
                    market = Market.objects.get(name=data['market'])

                em = self.model(
                    name=data['name'],
                    ticker=data['ticker'],
                    market=market
                )
                em.save()

                return rc.CREATED

            raise Http404

        else:
            super(Ticker, self).create(request)

    def update(self, request):
        if request.content_type:
            return rc.NOT_IMPLEMENTED
        else:
            super(Ticker, self).create(request)

    def delete(self, request):
        if request.content_type:
            return rc.NOT_IMPLEMENTED
        else:
            super(Ticker, self).create(request)


class TargetPriceHandler(BaseHandler):
    """
    TargetPrice data handler
    """
    allowed_methods = ('GET', 'POST', 'PUT')
    model = TargetPrice

    def read(self, request):
        if request.content_type:
            return rc.NOT_IMPLEMENTED
        else:
            super(TargetPrice, self).create(request)

    @require_mime('json')
    def create(self, request):
        if request.content_type:
            data = request.data

            analytic = Analytic
            ticker = Ticker

            try:
                analytic = Analytic.objects.get(name=data['analytic'])
            except analytic.DoesNotExist:
                em = Analytic(name=data['analytic'])
                em.save()
                analytic = Analytic.objects.get(name=data['analytic'])

            # Daily Crawler has only company name information,
            # no ticker information is provided
            if 'company_name' in data:
                try:
                    ticker = Ticker.objects.filter(name__icontains=data['company_name'])[0]
                except IndexError:
                    return rc.NOT_FOUND

            # Big ticker browser has the information in ticker information
            # so, the ticker in the database is identified by `ticker`
            if 'ticker' in data:
                try:
                    ticker = Ticker.objects.get(ticker=data['ticker'])
                except ticker.DoesNotExist:
                    return rc.NOT_FOUND

            # Saving the entry
            em = self.model(
                action=data['action'],
                analytic=analytic,
                rating=data['rating'],
                price0=data['price0'],
                price1=data['price1'],
                ticker=ticker,
                date=data['date']
            )

            em.save()
            return rc.CREATED

        else:
            super(TargetPrice, self).create(request)

    def update(self, request):
        if request.content_type:
            return rc.NOT_IMPLEMENTED
        else:
            super(TargetPrice, self).create(request)

    def delete(self, request):
        if request.content_type:
            return rc.NOT_IMPLEMENTED
        else:
            super(TargetPrice, self).create(request)


class TickerChangeHandler(BaseHandler):
    """
    TickerChange data handler
    """
    allowed_methods = ('GET', 'POST', 'PUT')
    model = TickerChange

    def read(self, request):
        if request.content_type:
            return rc.NOT_IMPLEMENTED
        else:
            super(TickerChange, self).create(request)

    def create(self, request):
        if request.content_type:
            return rc.NOT_IMPLEMENTED
        else:
            super(TickerChange, self).create(request)

    def update(self, request):
        if request.content_type:
            return rc.NOT_IMPLEMENTED
        else:
            super(TickerChange, self).create(request)

    def delete(self, request):
        if request.content_type:
            return rc.NOT_IMPLEMENTED
        else:
            super(TickerChange, self).create(request)
