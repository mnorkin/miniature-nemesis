import json
from django.conf import settings    # Settings
import psycopg2
import re
import time
import imp
from datetime import datetime
from datetime import timedelta


def stock_data(ticker=None):
    """
    Stock data method, returning the stock data on the sample ticker
    """
    try:
        f = open("".join((settings.STOCK_DATA_PATH, "/", ticker, '.json')), "r")
        data = json.loads(f.read())
        return data
    except IOError:
        return []


def beta_data(ticker=None):
    """
    The link between betas and utils interface
    """
    bt = betas()
    return bt.get_beta(ticker)


def target_data(ticker=None, analytic=None):
    """
    The link between target prices class and utils interface.

    Less typing in the django interface

    ticker -- ticker name (no slugs)
    analytic -- analytic name (no slugs)
    """
    tp = target_prices()
    return tp.return_target_prices(ticker, analytic)


def recent_target_data(ticker=None, analytic=None):
    """
    The link between the target prices class and utils interface

    ticker -- ticker name
    analytic -- analytic name
    """
    tp = target_prices()
    return tp.return_recent_target_prices(ticker, analytic)


def old_data_exists(ticker=None, analytic=None):
    """
    The link between the target prices class and utils interface

    ticker -- ticker name
    analytic -- analytic name
    """
    tp = target_prices()
    return tp.old_data_exists(ticker, analytic)


def ticker_analytics(ticker=None):
    """
    Returning all the analytics of ticker
    """
    tp = target_prices()
    return tp.return_ticker_analytics(ticker)


class betas():
    """
    Beta bridge
    """
    def __init__(self):
        """
        Initialization
        """
        self.cursor = self.connect_to_db()

    def connect_to_db(self):
        """
        """
        c_l = "dbname=%(NAME)s \
        user=%(USER)s \
        password=%(PASSWORD)s \
        host=%(HOST)s" % settings.TP_DATABASE
        db = psycopg2.connect(c_l)
        return db.cursor()

    def get_beta(self, ticker=None):
        """
        Function to return the beta value
        """
        if ticker:
            query = "SELECT value FROM betas WHERE name='%s' LIMIT 1" % (
                re.escape(ticker))
            if self.cursor.execute(query) != 0:
                row = self.cursor.fetchone()
                try:
                    return row[0]
                except:
                    return None
            else:
                return None
        else:
            return None


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
                # previous_targetprice = self.get_previous_targetprice(row[3], row[4], row[0])
                # Change is calculated in the app, because it needs the
                # Target price data
                change = 0

                item = {
                    'date_timestamp': time.mktime(row[0].timetuple()),
                    'date': str(row[0]),
                    'date_next': (
                        datetime.strptime(str(row[0]), '%Y-%m-%d') + timedelta(days=356)
                    ).strftime('%Y-%m-%d'),
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

    def return_recent_target_prices(self, ticker=None, analytic=None):
        """
        Returning recent target prices

        Which are not older than a year
        """
        if analytic and ticker:
            results = []
            query = "SELECT DISTINCT pub_date, price0, analytic, ticker \
                FROM entries \
                WHERE analytic=E'%s' AND ticker='%s' AND price0 != 0 \
                AND pub_date > NOW() - interval '1 year';" % (
                    re.escape(analytic),
                    re.escape(ticker))

            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                item = {
                    'date_timestamp': time.mktime(row[0].timetuple()),
                    'date': str(row[0]),
                    'date_next': (
                        datetime.strptime(str(row[0]), '%Y-%m-%d') + timedelta(days=356)
                    ).strftime('%Y-%m-%d'),
                    'price': row[1],
                    'analytic': row[2],
                    'ticker': row[3]
                }
                """Forming the dict"""
                results.append(item)

            return results
        else:
            return None

    def return_ticker_analytics(self, ticker=None):
        """
        Returning all the analytic, which analyses the ticker
        """
        if ticker:
            results = []
            query = "SELECT DISTINCT analytic \
                FROM entries \
                WHERE ticker='%s' AND price0 != 0 \
                GROUP BY analytic" % (
                    re.escape(ticker))

            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                item = {
                    'analytic': row[0]
                }
                results.append(item)

            return results
        else:
            return None

    def old_data_exists(self, ticker=None, analytic=None):
        """
        Checking if old data exists in the database (older than 12months)
        """
        if ticker and analytic:
            query = "SELECT DISTINCT pub_date, price0, analytic, ticker \
                FROM entries \
                WHERE analytic=E'%s' AND ticker='%s' AND price0 != 0 \
                AND pub_date < NOW() - interval '1 year';" % (
                    re.escape(analytic),
                    re.escape(ticker))
            self.cursor.execute(query)

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        else:
            return False


def feature_data(ticker=None):
    """
    Loading the feature data
    """
    # Getting stock data
    stock_data = stock_data(ticker)
    # Receive the beta
    beta = self.stock_quote.get_beta(target_price['ticker'])
    foo = imp.load_source('')
