from django.http import HttpResponse, Http404
from django.template import Context
from django.template import loader
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import DatabaseError
from morbid.models import TargetPrice
from morbid.models import Analytic
from morbid.models import FeatureAnalyticTicker
from morbid.models import FeatureAnalyticTickerCheck
from morbid.models import Feature
from morbid.models import Ticker
from morbid.forms import FeatureAnalyticTickerCheckForm
from morbid.utils import stock_data
from morbid.utils import target_data
from morbid.utils import beta_data
import re
import json
import urllib as u


def index(request, page=0):
    """
    Index page

    @return: Http Response
    """

    dates = [tp['date'] for tp in TargetPrice.objects.with_count().order_by('-date').distinct('date').values()]

    if page > dates.__len__() or page >= 1:
        raise Http404

    latest_target_prices = TargetPrice.objects.with_count().filter(
        date__range=(dates[4], dates[0])
    ).order_by('-id')

    feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(
        analytic_id__in=latest_target_prices.values_list(
            'analytic_id',
            flat=True
        ).distinct,
        ticker_id__in=latest_target_prices.values_list(
            'ticker_id',
            flat=True
        ).distinct,
        feature__display_in_frontpage=True)
    target_price_list = []

    for target_price in latest_target_prices:
        target_price.fap = feature_analytic_tickers.filter(
            analytic=target_price.analytic,
            ticker=target_price.ticker
        ).order_by('-feature').distinct('feature')
        if sum(target_price.fap.values_list('value', flat=True)) > 0:
            target_price.sum = sum(target_price.fap.values_list('value', flat=True))
            target_price_list.append(target_price)

    t = loader.get_template('morbid/index.html')

    date = dates[page]

    if page == 0:
        extends_template = 'morbid/base.html'
    else:
        extends_template = 'morbid/base_page.html'

    c = Context({
        'latest_target_prices': target_price_list,
        'extends_template': extends_template,
        'date': date
    })

    return HttpResponse(t.render(c))


def ticker(request, slug):
    """
    Ticker page

    @param slug: the request for the specific Ticker
    @type: C{str}

    @return: Http Response. If the Ticker was not found -- rises the 404 error
    """

    ticker = Ticker()

    try:
        ticker = Ticker.objects.get(slug=slug)
    except ticker.DoesNotExist:
        raise Http404

    # Load target orice info
    latest_target_prices = TargetPrice.objects.filter(
        ticker_id=ticker.id
    ).order_by('analytic', 'date').reverse().distinct('analytic')

    feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(
        analytic_id__in=latest_target_prices.values_list(
            'analytic_id',
            flat=True
        ).distinct,
        ticker_id=ticker.id)

    target_price_list = []

    for target_price in latest_target_prices:

        target_price.fap = feature_analytic_tickers.filter(
            analytic_id=target_price.analytic_id
        )
        target_price_list.append(target_price)

    # Load feature info
    list_of_features = Feature.objects.all()

    t = loader.get_template('morbid/ticker.html')

    c = Context({
        'ticker': ticker,
        'target_prices': target_price_list,
        'features': list_of_features
    })

    return HttpResponse(t.render(c))



def tickers(request):
    """
    Returning all the tickers, in the system
    """
    _tickers = Ticker.objects.with_display().order_by('name')
    tickers = []

    for ticker in _tickers:
        item = {
            'name': ticker.name,
            'long_name': ticker.long_name,
            'url': ticker.get_absolute_url()
        }
        tickers.append(item)

    return HttpResponse(json.dumps(tickers, indent=4))



def ticker_data(request, ticker):
    PATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
    url = 'http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=b3c6p&e=.csv' % (ticker.upper())
    f = u.urlopen(url, proxies={})
    rows = f.readlines()
    r = rows[0]
    # return HttpResponse(r)
    """Get the first entry"""
    r = PATTERN.split(r[:-2])[1::2]
    """Remove the `\r\n` and split by comma"""

    r[1].replace('"', '')
    change = r[1]
    last_stock_price = float(r[0])
    change_percent = 0
    change_direction = 'up'

    if (change[1] == '+'):
        """Positive change"""
        change = change[2:-1]
        """Drop the sign"""
        change_direction = 'up'
    else:
        """Negative change"""
        change = change[2:-1]
        """Drop the sign"""
        change_direction = 'down'

    change = float(change)

    if change == 0:
        last_stock_price = r[2]

    if change != 0:
        change_percent = round(change / (last_stock_price - change) * 100, 2)
    else:
        change_percent = 0

    item = {
        "last_stock_price": last_stock_price,
        "change": change,
        "change_percent": change_percent,
        "change_direction": change_direction
    }

    return HttpResponse(json.dumps(item))



def analytic(request, slug):
    """
    Analytic page

    @param slug: the slug to reach the page

    @return: Http Response. If the analytic was not found by the slug -- 404
    error rises
    """

    # Load analytic info
    try:
        analytic = Analytic.objects.get(slug=slug)
    except Analytic.DoesNotExist:
        raise Http404

    # Load target price info
    latest_target_prices = TargetPrice.objects.filter(
        analytic_id=analytic.id
    ).order_by('ticker', 'date').reverse().distinct('ticker')

    target_price_list = []

    feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(
        analytic_id=analytic.id,
        ticker_id__in=latest_target_prices.values_list('ticker_id', flat=True).distinct
    )

    for target_price in latest_target_prices:

        feature_analytic_tickers = feature_analytic_tickers.filter(
            ticker_id=target_price.ticker_id
        )

        target_price.fap = feature_analytic_tickers
        target_price_list.append(target_price)

    # Load feature info
    list_of_features = Feature.objects.all()

    t = loader.get_template('morbid/analytic.html')

    c = Context({
        'analytic': analytic,
        'target_prices': target_price_list,
        'features': list_of_features
    })

    return HttpResponse(t.render(c))



def target_prices(self, analytic_slug=None, ticker_slug=None):

    target_price_list = []

    if analytic_slug:

        analytic = Analytic
        try:
            analytic = Analytic.objects.get(slug=analytic_slug)
            target_prices = TargetPrice.objects.filter(analytic=analytic)
            feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(
                analytic=analytic, feature__display_in_frontpage=True)

            for target_price in target_prices:
                target_price.fap = feature_analytic_tickers.filter(
                    analytic=target_price.analytic,
                    ticker=target_price.ticker
                )
                target_price_list.append(target_price)

        except analytic.DoesNotExist:
            raise Http404

    elif ticker_slug:

        ticker = Ticker
        try:
            ticker = Ticker.objects.get(slug=ticker_slug)
            target_prices = TargetPrice.objects.filter(ticker=ticker)
            feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(
                ticker=ticker, feature__display_in_frontpage=True)

            for target_price in target_prices:
                target_price.fap = feature_analytic_tickers.filter(
                    analytic=target_price.analytic,
                    ticker=target_price.ticker
                )
                target_price_list.append(target_price)

        except ticker.DoesNotExist:
            raise Http404

    else:
        raise Http404

    date = target_price_list[0].date

    t = loader.get_template('morbid/target_prices.html')

    c = Context({
        'target_prices': target_price_list,
        'date': date
    })

    return HttpResponse(t.render(c))



def feature_by_ticker(self, slug, feature_id):
    """
    The feature return management on the Ticker page

    @param slug: the slug to reach the Ticker
    @param feature_id: the feature id to return

    @return: Http Response. If the Ticker was not found using the slug -- 404
    error rises

    JSON only
    """

    try:
        ticker = Ticker.objects.get(slug=slug)
    except Ticker.DoesNotExist:
        return Http404

    feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(
        ticker_id=ticker.id,
        feature_id=feature_id
    ).values('value', 'analytic__name', 'analytic__slug')

    # return feature_analytic_tickers

    [fat.update({'url': '/analytic/' + fat['analytic__slug']}) for fat in feature_analytic_tickers]

    return HttpResponse(json.dumps(list(feature_analytic_tickers), indent=4))



def feature_by_analytic(self, slug, feature_id):
    """
    The feature return management on the analytic page

    @param slug: the slug to reach the
    @param feature_id: the feature id to return

    @return: Http Response JSON only. If the analytic was not found using the
    slug -- 404 error rises


    """
    try:
        analytic = Analytic.objects.get(slug=slug)
    except analytic.DoesNotExist:
        return Http404

    feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(
        analytic_id=analytic.id,
        feature_id=feature_id
    ).values('value', 'ticker__name', 'ticker__slug')

    return HttpResponse(json.dumps(list(feature_analytic_tickers), indent=4))



def search(self, search_me):
    """
    The search of the page

    @param search_me: The string to query search the database

    @return: Http Response in JSON.
    """

    results = {}
    analytics = []
    tickers = []

    raw_analytics = Analytic.objects.filter(
        Q(name=search_me) | Q(name__icontains=search_me)
    )[:5]

    raw_tickers_names = Ticker.objects.filter(
        Q(name=search_me) | Q(name__icontains=search_me)
    ).extra(select={'length': 'Length(name)'}).order_by('length')[:5]

    raw_tickers_long_names = Ticker.objects.filter(
        Q(long_name=search_me) | Q(long_name__icontains=search_me)
    ).extra(select={'length': 'Length(name)'}).order_by('length')[:5]

    for analytic in raw_analytics:
        item = {
            'name': analytic.name,
            'url': analytic.get_absolute_url()
        }
        analytics.append(item)

    for ticker in raw_tickers_names:
        item = {
            'name': ticker.long_name,
            'ticker': ticker.name,
            'url': ticker.get_absolute_url()
        }
        tickers.append(item)

    for ticker in raw_tickers_long_names:
        item = {
            'name': ticker.long_name,
            'ticker': ticker.name,
            'url': ticker.get_absolute_url()
        }
        tickers.append(item)

    results['tickers'] = list(tickers)
    results['analytics'] = analytics

    return HttpResponse(json.dumps(results, indent=4))


def graph_01(request):
    """
    Example of graph 01
    """
    t = loader.get_template('graph_01.html')
    c = Context()

    return HttpResponse(t.render(c))


def graph_02(request):
    """
    Example of graph 02
    """

    t = loader.get_template("graph_02.html")

    c = Context()

    return HttpResponse(t.render(c))


def graph_03(request):
    """
    Example of graph 03
    """

    t = loader.get_template("graph_03.html")

    c = Context()

    return HttpResponse(t.render(c))


def screen(request):
    """
    This is the screen page, which displays the screen shots of the system
    """

    t = loader.get_template("screen.html")

    c = Context()

    return HttpResponse(t.render(c))


@login_required(login_url='/admin/')
def test(request, ticker_slug=None, analytic_slug=None):
    """
    This is the testing platform, which will make the role of testing platform
    from the various users, to make sure, all the data is calculated correctly
    """
    message = dict()
    if request.method == 'POST':
        feature_analytic_ticker_check_form = FeatureAnalyticTickerCheckForm(request.POST)
        if feature_analytic_ticker_check_form.is_valid():
            feature_analytic_ticker_id = feature_analytic_ticker_check_form.cleaned_data['feature_analytic_ticker']
            value = feature_analytic_ticker_check_form.cleaned_data['value']
            fatc = FeatureAnalyticTickerCheck()
            fatc.value = value
            fatc.feature_analytic_ticker = FeatureAnalyticTicker.objects.get(
                id=feature_analytic_ticker_id
            )

            try:
                fatc.save()
                message['type'] = 'message-success'
                message['text'] = 'Submission saved successfully'
            except DatabaseError:
                message['type'] = 'message-fail'
                message['text'] = 'Something failed'

    # Collect all the features
    feature_analytic_tickers = FeatureAnalyticTicker.objects.all()

    if ticker_slug and analytic_slug:
        # Select ticker in question
        feature_analytic_ticker = feature_analytic_tickers.filter(
            ticker__slug=ticker_slug,
            analytic__slug=analytic_slug
        )[0]
    elif ticker_slug:
        # Select ticker in question
        feature_analytic_ticker = feature_analytic_tickers.filter(
            ticker__name=ticker_slug
        ).order_by('?')[0]
    else:
        # Randomly select one
        feature_analytic_ticker = feature_analytic_tickers.order_by('?')[0]

    feature_analytic_ticker_data = feature_analytic_tickers.filter(
        ticker__slug=feature_analytic_ticker.ticker.slug,
        analytic__slug=feature_analytic_ticker.analytic.slug
    ).order_by('feature__position').values('feature__name', 'value', 'id')

    results = []

    for data in feature_analytic_ticker_data:
        feature_analytic_ticker_check_form = FeatureAnalyticTickerCheckForm(
            initial={'feature_analytic_ticker': data['id']}
        )
        item = {
            'name': data['feature__name'],
            'value': data['value'],
            'feature_analytic_ticker_check_form': feature_analytic_ticker_check_form
        }
        results.append(item)

    stocks_data = stock_data(
        ticker=feature_analytic_ticker.ticker.name
    )

    target_prices = target_data(
        ticker=feature_analytic_ticker.ticker.name,
        analytic=feature_analytic_ticker.analytic.name
    )

    for target_price in target_prices:
        matches = ((i, x) for i, x in enumerate(stocks_data) if x['date'] == target_price['date'])
        try:
            stock_entry = matches.next()
            target_price['stock_price_open'] = stock_entry[1]['price_open']
            target_price['stock_price_close'] = stock_entry[1]['price_close']
            try:
                target_price['stock_price_next_open'] = stocks_data[stock_entry[0]+250]['price_open']
                target_price['stock_price_next_close'] = stocks_data[stock_entry[0]+250]['price_close']
            except IndexError:
                target_price['stock_price_next_open'] = 0
                target_price['stock_price_next_close'] = 0
        except StopIteration:
            target_price['stock_price_open'] = 0
            target_price['stock_price_close'] = 0
            target_price['stock_price_next_open'] = 0
            target_price['stock_price_next_close'] = 0

    t = loader.get_template("test.html")

    c = RequestContext(request, {
        'feature_analytic_ticker': feature_analytic_ticker,
        'feature_analytic_ticker_data': results,
        'target_prices': target_prices,
        'current_url': request.path,
        'message': message,
        'beta': beta_data(feature_analytic_ticker.ticker.name)
    })

    return HttpResponse(t.render(c))


def test_page_search(self, search_me):
    """
    The search of the page

    @param search_me: The string to query search the database

    @return: Http Response in JSON.
    """

    results = []

    raw_tickers = Ticker.objects.filter(
        Q(name__icontains=search_me) | Q(long_name__icontains=search_me)
    )

    for ticker in raw_tickers:
        target_prices = TargetPrice.objects.filter(ticker=ticker).distinct('analytic')
        for target_price in target_prices:
            item = {
                'name': ticker.long_name,
                'ticker': ticker.name,
                'analytic': target_price.analytic.name,
                'title': ' '.join((ticker.name, target_price.analytic.name)),
                'url': '/' + '/'.join(('testing', ticker.slug, target_price.analytic.slug))
            }
            results.append(item)

    return HttpResponse(json.dumps(results, indent=4))
