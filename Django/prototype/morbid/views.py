from django.http import HttpResponse, Http404
from django.template import Context, loader
from morbid.models import TargetPrice, Analytic, FeatureAnalyticTicker, Feature, Ticker
from django.db.models import Q
import re
import json
from prototype.decorators import logged_in_or_basicauth
import urllib as u


@logged_in_or_basicauth(realm="Limited access")
def index(request, page=0):
    """
    Index page

    @return: Http Response
    """

    # if not settings.DEBUG:
        # Return week long entries
        # latest_target_prices = TargetPrice.objects.filter(date__lt=datetime(datetime.now().year, datetime.now().month, datetime.now().day) - timedelta(days=-7)).order_by('date').reverse()
    # else:
        # latest_target_prices = TargetPrice.objects.filter(date__lt=datetime(datetime.now().year, datetime.now().month, datetime.now().day) - timedelta(days=-1)).order_by('date').reverse()
    # latest_target_prices = TargetPrice.objects.filter(date__lt=datetime(datetime.now().year, datetime.now().month, datetime.now().day) - timedelta(days=-7)).order_by('date').reverse()

    dates = [tp['date'] for tp in TargetPrice.objects.order_by('-date').distinct('date').values()]

    page = int(page)

    # if page > dates.__len__() or page >= 7:
    if page > dates.__len__():
        raise Http404

    latest_target_prices = TargetPrice.objects.filter(date=dates[page]).order_by('id').reverse()

    feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(analytic_id__in=latest_target_prices.values_list('analytic_id', flat=True).distinct, ticker_id__in=latest_target_prices.values_list('ticker_id', flat=True).distinct, feature__display_in_frontpage=True)
    target_price_list = []

    for target_price in latest_target_prices:

        target_price.fap = feature_analytic_tickers.filter(analytic_id=target_price.analytic_id, ticker_id=target_price.ticker_id)
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
    latest_target_prices = TargetPrice.objects.filter(ticker_id=ticker.id).order_by('analytic', 'date').reverse().distinct('analytic')

    feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(analytic_id__in=latest_target_prices.values_list('analytic_id', flat=True).distinct, ticker_id=ticker.id)

    target_price_list = []

    for target_price in latest_target_prices:

        target_price.fap = feature_analytic_tickers.filter(analytic_id=target_price.analytic_id)
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


def ticker_data(request, ticker):
    PATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
    url = 'http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=b3c6&e=.csv' % (ticker)
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

    change_percent = round(change / (last_stock_price - change) * 100, 2)

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
    latest_target_prices = TargetPrice.objects.filter(analytic_id=analytic.id).order_by('ticker', 'date').reverse().distinct('ticker')

    target_price_list = []

    feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(analytic_id=analytic.id, ticker_id__in=latest_target_prices.values_list('ticker_id', flat=True).distinct)

    for target_price in latest_target_prices:

        feature_analytic_tickers = feature_analytic_tickers.filter(ticker_id=target_price.ticker_id)

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
                analytic=analytic, feature__display_in_frontpage=True).order_by('id')

            for target_price in target_prices:
                target_price.fap = feature_analytic_tickers.filter(analytic_id=target_price.analytic_id, ticker_id=target_price.ticker_id)
                target_price_list.append(target_price)

        except analytic.DoesNotExist:
            raise Http404

    elif ticker_slug:

        ticker = Ticker
        try:
            ticker = Ticker.objects.get(slug=ticker_slug)
            target_prices = TargetPrice.objects.filter(ticker=ticker)
            feature_analytic_tickers = FeatureAnalyticTicker.objects.filter(
                ticker=ticker, feature__display_in_frontpage=True).order_by('id')

            for target_price in target_prices:
                target_price.fap = feature_analytic_tickers.filter(analytic_id=target_price.analytic_id, ticker_id=target_price.ticker_id)
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

    # analytics = Analytic.objects.filter(name__icontains=search_me ).values('name', 'slug')
    raw_analytics = Analytic.objects.filter(name__icontains=search_me)

    # tickers = Ticker.objects.filter( Q(name__icontains=search_me) | Q(long_name__icontains=search_me) ).values('name', 'slug')
    raw_tickers = Ticker.objects.filter(Q(name__icontains=search_me) | Q(long_name__icontains=search_me))

    for analytic in raw_analytics:
        item = {'name': analytic.name, 'url': analytic.get_absolute_url()}
        analytics.append(item)

    for ticker in raw_tickers:
        item = {'name': ticker.long_name, 'url': ticker.get_absolute_url()}
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

    t = loader.get_template("screen.html")

    c = Context()

    return HttpResponse(t.render(c))
