import json
from django.conf import settings    # Settings
import psycopg2
import re
import time


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


def target_data(ticker=None, analytic=None):
    """
    The link between target prices class and utils interface.

    Less typing in the django interface

    ticker -- ticker name (no slugs)
    analytic -- analytic name (no slugs)
    """
    tp = target_prices()
    return tp.return_target_prices(ticker, analytic)


class target_prices():
    """
    Target prices bridge
    """
    def __init__(self):
        """
        Initialization
        """
        self.cursor = self.connect_to_db()

    def connect_to_db(self):
        """
        Connecting to database
        """
        c_l = "dbname=%(NAME)s \
        user=%(USER)s \
        password=%(PASSWORD)s \
        host=%(HOST)s" % settings.TP_DATABASE
        db = psycopg2.connect(c_l)
        return db.cursor()

    def return_target_prices(self, ticker=None, analytic=None):
        """
        Returning everything
        """
        if analytic and ticker:
            results = []
            query = "SELECT pub_date, price0, analytic, ticker \
                FROM entries \
                WHERE analytic=E'%s' AND ticker='%s' AND price0 != 0 \
                AND pub_date < NOW() - interval '1 year' \
                ORDER BY pub_date" % (
                    re.escape(analytic),
                    re.escape(ticker))
            """Query for the target prices, which are older than the maximum date
                (getting rid of the most recent one, because of model requires
                old data)"""
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                change = 0

                # previous_targetprice = self.get_previous_targetprice(row[3], row[4], row[0])
                # Change is calculated in the app, because it needs the
                # Target price data
                change = 0

                item = {
                    'date_timestamp': time.mktime(row[0].timetuple()),
                    'date': str(row[0]),
                    'price': row[1],
                    'analytic': row[2],
                    'ticker': row[3],
                    'change': round(change, 2)
                }
                """Forming the dict"""
                if item not in results:
                    """Escaping possible duplicates"""
                    results.append(item)

            return results
        else:
            return None
