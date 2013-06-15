"""
The Stock_Quete
"""
import urllib as u
import datetime
import time
import utils
import re
from database import database
from logger import logger
from HTMLParser import HTMLParser
import settings
import json


class MLStripper(HTMLParser):
    """
    HTML tags stripper
    """
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ';'.join(self.fed)


class stock_quote():

    def __init__(self):
        self.database = database()
        self.logger = logger('Stock_Quete')
        self.data_dir = settings.data_dir

    def strip_tags(self, html):
        """
        Strip tags method
        """
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def get_data(self, ticker=None):
        data = []
        try:
            with open('%s/%s.json' % (self.data_dir, ticker)):
                f = open('%s/%s.json' % (self.data_dir, ticker), 'r')
                try:
                    entries = json.loads(f.read())
                except ValueError:
                    return None
                if type(entries) is list:
                    self.logger.debug('Returning %s stock data' % ticker)
                    for entry in entries:
                        item = {
                            'date': time.mktime(datetime.datetime.strptime(entry['date'], "%Y-%m-%d").timetuple()),
                            'open': entry['price_open'],
                            'close': entry['price_close'],
                            'high': entry['price_high'],
                            'low': entry['price_low']
                        }
                        data.append(item)

                    try:
                        if data[0]['date'] > data[len(data)-1]['date']:
                            """
                            Data should start from the 2001 to 2013 or in similar
                            style -- from old to new
                            """
                            data.reverse()
                        return data
                    except:
                        return None
                return None
        except IOError:
            return False

    def get_data_inet(self, ticker=None):
        """
        Getting stock data
        """
        data = []
        url = 'http://ichart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&ignore=.csv' % (ticker, 0, 1, 2006)
        f = u.urlopen(url, proxies={})
        rows = f.readlines()
        for r in rows[1:]:
            values = r.split(',')
            try:
                stock_date = time.mktime(datetime.datetime.strptime(values[0], '%Y-%m-%d').timetuple())
                stock_open = float(values[1])
                stock_high = float(values[2])
                stock_low = float(values[3])
                stock_close = float(values[4])
                item = {
                    'date': stock_date,
                    'open': stock_open,
                    'high': stock_high,
                    'low': stock_low,
                    'close': stock_close
                }

                data.append(item)
                if utils.DEBUG:
                    if data.__len__() == 2:
                        self.logger.debug("Stock data: %s" % data)
            except ValueError:
                """
                This happens, then the ticker does not exists in the stock (somehow)
                """
                self.logger.debug("Value error, skipping ticker")
                return None

        data.reverse()
        return data

    def get_ticker_data(self, ticker):
        """
        Getting ticker data
        """
        PATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
        url = 'http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=nb3x&e=.csv' % (ticker)
        self.logger.debug("Url: %s" % url)
        try:
            f = u.urlopen(url, proxies={})
        except IOError:
            """
            Reset of connection
            """
            item = {
                "long_name": "",
                "last_stock_price": 0,
                "stock_exchange": None
            }
            return item

        rows = f.readlines()
        r = rows[0]
        """Get the first entry"""
        r = PATTERN.split(r[:-2])[1::2]
        """Remove the `\r\n` and split by comma"""
        if (not isinstance(r[2], int)) or (not isinstance(r[2], float)):
            self.logger.debug("Data not available")
            """Not available"""
            r[2] = None
            r[1] = 0

        item = {
            "long_name": r[0],
            "last_stock_price": r[1],
            "stock_exchange": r[2]
        }

        return item

    def get_beta(self, ticker):
        """
        Getting beta measure of ticker (currently only stock market is SP500 (^GSPC))
        """
        # beta = None
        if ticker:
            return self.database.get_beta(ticker)
        return None
        # Don't go anywhere, betas are stored locally
        # if ticker:
        #     beta = self.database.get_beta(ticker)
        #     if beta:
        #         return beta
        #     else:
        #         PATTERN = re.compile(r'''((?:[^;"']|"[^"]*"|'[^']*')+)''')
        #         url = 'http://finance.yahoo.com/q?s=%s' % (ticker)
        #         try:
        #             f = u.urlopen(url, proxies={})
        #             rows = f.readlines()
        #             for row in rows:
        #                 try:
        #                     row = self.strip_tags(row)
        #                     position = row.find('Beta:')
        #                     if position != -1:
        #                         r = PATTERN.split(row[position:])[1::2]
        #                         try:
        #                             beta = float(r[1])
        #                             """Write beta to database"""
        #                             self.database.write_beta(ticker, beta)
        #                         except ValueError:
        #                             beta = None
        #                 except UnicodeDecodeError:
        #                     beta = None
        #         except u.URLError:
        #             beta = None
        # return beta
