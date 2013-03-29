"""
The Stock_Quete
"""
import urllib as u
import datetime
import time
import utils
import re
from database import database
import logging
import os
from datetime import date
from HTMLParser import HTMLParser


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
        self.absolute_path = os.path.dirname(os.path.realpath(__file__))
        self.logging_file = self.absolute_path + '/logs/' + date.today().isoformat() + '.log'
        self.logging_level = logging.DEBUG
        logging.basicConfig(
            filename=self.logging_file,
            level=self.logging_level, format='%(asctime)s %(message)s')

    def strip_tags(self, html):
        """
        Strip tags method
        """
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def get_data(self, ticker):
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
                        logging.debug("Stock data: %s", data)
            except ValueError:
                """
                This happens, then the ticker does not exists in the stock (somehow)
                """
                logging.debug("Value error, skipping ticker")
                return None

        data.reverse()
        return data

    def get_ticker_data(self, ticker):
        """
        Getting ticker data
        """
        PATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
        url = 'http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=nb3x&e=.csv' % (ticker)
        f = u.urlopen(url, proxies={})
        rows = f.readlines()
        r = rows[0]
        """Get the first entry"""
        r = PATTERN.split(r[:-2])[1::2]
        """Remove the `\r\n` and split by comma"""
        if (not isinstance(r[2], int)) or (not isinstance(r[2], float)):
            logging.debug("Data not available")
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
        beta = None
        if ticker:
            beta = self.database.get_beta(ticker)
            if beta:
                return beta
            else:
                PATTERN = re.compile(r'''((?:[^;"']|"[^"]*"|'[^']*')+)''')
                url = 'http://finance.yahoo.com/q?s=%s' % (ticker)
                f = u.urlopen(url, proxies={})
                rows = f.readlines()
                for row in rows:
                    row = self.strip_tags(row)
                    position = row.find('Beta:')
                    if position != -1:
                        r = PATTERN.split(row[position:])[1::2]
                        try:
                            beta = float(r[1])
                            """Write beta to database"""
                            self.database.write_beta(ticker, beta)
                        except ValueError:
                            beta = None
        return beta
