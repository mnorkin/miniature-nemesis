from django.http import HttpResponse, Http404
from django.template import Context, loader
from sink.models import TargetPrice, Ticker
from sink.decorators import logged_in_or_basicauth

def index(request):
    """
    Index page, lol
    """
    raise Http404

@logged_in_or_basicauth(realm="Limited access")
def progress(request):
    """
    Index page
    """
    number_of_fetched_tickers = float(TargetPrice.objects.all().distinct('ticker').count())
    total_number_of_tickers = float(Ticker.objects.all().count())
    tickers_left = total_number_of_tickers - number_of_fetched_tickers
    current_progress = number_of_fetched_tickers / total_number_of_tickers * 100
    remaininng = tickers_left / total_number_of_tickers * 100

    t = loader.get_template('sink/progress.html')

    c = Context({
        'nt': number_of_fetched_tickers,
        'tt': total_number_of_tickers,
        'cp': current_progress,
        'rt': remaininng,
        'tl': tickers_left
    })

    return HttpResponse(t.render(c))
