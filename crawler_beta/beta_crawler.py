# Betas crawler
from logger import logger
import os
import rest
import urlparse
import urllib
import urllib2
import re
from HTMLParser import HTMLParser
from database import database


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


class beta_crawler():

    def __init__(self):
        # Make the http
        self.open_http = self.make_open_http()
        # logging
        self.logger = logger('Beta')
        self.database = database()

    def strip_tags(self, html):
        """
        Strip tags method
        """
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def dir_check(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def url_with_query(self, url, values):
        parts = urlparse.urlparse(url)
        rest, (query, frag) = parts[:-2], parts[-2:]
        return urlparse.urlunparse(rest + (urllib.urlencode(values), None))

    def make_open_http(self):
        proxy_support = urllib2.ProxyHandler({'http': 'localhost:8118'})
        """Tor support"""
        cooki_support = urllib2.HTTPCookieProcessor()
        """Cookies support"""
        opener = urllib2.build_opener(cooki_support, proxy_support)
        # opener = urllib2.build_opener(proxy_support)
        # opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]  # Hacking
        urllib2.install_opener(opener)

        def open_http(method, url, values={}):
            if method == "POST":
                return opener.open(url, urllib.urlencode(values))
            else:
                return opener.open(self.url_with_query(url, values))

        return open_http

    def main(self):
        """
        The beta values crawler
        """
        # Go to the server, ask for the tickers
        tickers = rest.send('GET', '/api/stocks/')

        for ticker in tickers:
            self.logger.debug('Ticker: %s' % ticker['ticker'])
            beta = None
            PATTERN = re.compile(r'''((?:[^;"']|"[^"]*"|'[^']*')+)''')
            url = 'http://finance.yahoo.com/q?s=%s' % (ticker['ticker'])
            f = urllib.urlopen(url, proxies={})
            rows = f.readlines()
            for row in rows:
                try:
                    row = self.strip_tags(row)
                    position = row.find('Beta:')
                    if position != -1:
                        r = PATTERN.split(row[position:])[1::2]
                        try:
                            beta = float(r[1])
                            """Write beta to database"""
                            self.logger.debug('Writing the beta value into the database')
                            self.database.write_beta(ticker['ticker'], beta)
                        except ValueError:
                            beta = None
                except UnicodeDecodeError:
                    beta = None

if __name__ == '__main__':
    bc = beta_crawler()
    bc.main()
