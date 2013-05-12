import json
from django.conf import settings    # Settings


def stock_data(ticker=None):
    """
    Stock data method, returning the stock data on the sample ticker
    """
    try:
        f = open("".join((settings.STOCK_DATA_PATH, "/", ticker, '.json')), "r")
        data = json.loads(f.read())[1::10]
        return data
    except IOError:
        return []
