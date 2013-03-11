from sink.models import Ticker, TargetPrice, TickerChange
from piston.handler import BaseHandler
from piston.utils import rc, validate
from django.http import HttpResponse, Http404


class TickerHandler(BaseHandler):
    """
    Ticker data handler
    """
    allowed_methods = ('GET', 'POST', 'PUT')
    model = Ticker

    def read(self, request):
        if request.content_type:
            pass
        else:
            super(Ticker, self).create(request)

    def create(self, request):
        if request.content_type:
            pass
        else:
            super(Ticker, self).create(request)

    def update(self, request):
        if request.content_type:
            pass
        else:
            super(Ticker, self).create(request)

    def delete(self, request):
        if request.content_type:
            pass
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
            pass
        else:
            super(TargetPrice, self).create(request)

    def create(self, request):
        if request.content_type:
            pass
        else:
            super(TargetPrice, self).create(request)

    def update(self, request):
        if request.content_type:
            pass
        else:
            super(TargetPrice, self).create(request)

    def delete(self, request):
        if request.content_type:
            pass
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
            pass
        else:
            super(TickerChange, self).create(request)

    def create(self, request):
        if request.content_type:
            pass
        else:
            super(TickerChange, self).create(request)

    def update(self, request):
        if request.content_type:
            pass
        else:
            super(TickerChange, self).create(request)

    def delete(self, request):
        if request.content_type:
            pass
        else:
            super(TickerChange, self).create(request)
