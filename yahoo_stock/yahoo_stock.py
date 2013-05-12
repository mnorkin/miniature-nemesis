"""
Merging yahoo stock data with the database in question
"""
import os
from logger import logger
import json
import httplib
import time
import urlparse
import urllib
import urllib2


class yahoo_stock():

    def __init__(self):
        # Making the http
        self.open_http = self.make_open_http()
        self.absolute_path = os.path.dirname(os.path.realpath(__file__))
        self.data_dir = self.absolute_path + '/data/'
        # Logging
        self.dir_check(self.data_dir)
        self.logger = logger('Yahoo')

    def dir_check(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def url_with_query(self, url, values):
        parts = urlparse.urlparse(url)
        rest, (query, frag) = parts[:-2], parts[-2:]
        return urlparse.urlunparse(rest + (urllib.urlencode(values), None))

    def make_open_http(self):
        # proxy_support = urllib2.ProxyHandler({'http': 'localhost:8118'})
        """Tor support"""
        # cooki_support = urllib2.HTTPCookieProcessor()
        """Cookies support"""
        # opener = urllib2.build_opener(cooki_support, proxy_support)
        # opener = urllib2.build_opener(proxy_support)
        opener = urllib2.build_opener()
        # opener.addheaders = [('User-agent', 'Mozilla/5.0')]  # Hacking
        urllib2.install_opener(opener)

        def open_http(method, url, values={}):
            if method == "POST":
                return opener.open(url, urllib.urlencode(values))
            else:
                return opener.open(self.url_with_query(url, values))

        return open_http

    def stock_request(self, ticker):
        """
        Requesting the stocks
        """
        data = []
        url = 'http://ichart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&ignore=.csv' % (
            ticker, 0, 1, 2001)
        # print url
        # f = self.open_http("GET", url)
        f = urllib.urlopen(url)
        # try:
            # f = self.open_http("GET", url)
        # except urllib2.HTTPError, e:
            # print e
            # raise e

        rows = f.readlines()
        for r in rows[1:]:
            values = r.split(',')
            try:
                # dstr = datetime.strptime(values[0], '%Y-%m-%d').timetuple()
                stock_date = values[0]
                stock_open = float(values[1])
                stock_high = float(values[2])
                stock_low = float(values[3])
                stock_close = float(values[4])
                item = {
                    'date': stock_date,
                    'price_open': stock_open,
                    'price_high': stock_high,
                    'price_low': stock_low,
                    'price_close': stock_close,
                    'ticker': ticker
                }

                data.append(item)
            except ValueError:
                """
                This happens, then the ticker does not exists in the stock (somehow)
                """
                self.logger.debug("Value error, skipping ticker %s" % ticker)
            except IndexError:
                self.logger.debug("Index error, skipping ticker %s" % ticker)
        return data

    def rest(self, url, request, data=None, cycle=1):
        """
        Rest interface for the crawler API
        """
        params = json.dumps(data)
        # print params
        headers = {"Content-type": "application/json"}
        # conn = httplib.HTTPConnection("cra.baklazanas.lt")
        conn = httplib.HTTPConnection("localhost:8000")
        self.logger.debug(url)
        self.logger.debug(headers)
        self.logger.debug(params)
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        conn.close()
        if response.status != 502:
            # ALL_OK
            if response.status == 200 and request.upper() == 'GET':
                # Returning all the data
                return json.loads(response.read())
            # CREATED
            elif response.status == 201 and request.upper() == 'POST':
                return True
            # ALL_OK
            elif response.status == 200 and request.upper() == 'PUT':
                return True
            # DELETED
            elif response.status == 204 and request.upper() == 'DELETE':
                return True
            else:
                return None
        else:
            self.logger.debug("Received 502 error")
            time.sleep(1000*cycle)
            if cycle < 10:
                return self.rest(url, request, data, cycle + 1)
            else:
                return False

    def main(self):
        """
        Getting all the tickers from the server
        """
        # tickers = self.rest('/api/stocks/', 'GET')
        # tickers = [{'ticker': '^GSPC'}]
        tickers = [{'ticker': 'YRI'}]
        start_time = 0
        # Start the request loop
        for ticker in tickers:
            try:
                # Check if exported file exists
                with open('%s.json' % ticker['ticker']):
                    # Do nothing
                    pass
            except:
                # If file does not exist -- proceed
                if start_time != 0:
                    print time.time() - start_time, "seconds, for ticker", ticker['ticker']
                start_time = time.time()
                data = self.stock_request(ticker['ticker'])
                f = open('%s%s.json' % (self.data_dir, ticker['ticker']), 'w')
                f.write(json.dumps(data))

if __name__ == '__main__':
    ys = yahoo_stock()
    ys.main()
