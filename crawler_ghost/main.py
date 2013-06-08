#!/usr/bin/python2
import urllib2
import urllib
from logger import logger
from lxml.html import fromstring  # More control
from lxml.html import submit_form  # Submitting form
import time
from csv_parser import csv_parser
from random import random
import re
from datetime import datetime
import json
import urlparse
import rest


class main():
    """
    Crawler ghost
    """
    def __init__(self, username, password):
        """
        Initialization
        """
        self.url = 'http://stocktargetprices.com/'
        self.login_page = 'login'
        self.logger = logger('app')
        self.tickers = []
        self.csv_data = csv_parser('sp500.csv')
        self.target_price_list = []
        self.open_http = self.make_open_http()
        self.login_username = username
        self.login_password = password
        self.rest = rest

    def url_with_query(self, url, values):
        parts = urlparse.urlparse(url)
        rest, (query, frag) = parts[:-2], parts[-2:]
        return urlparse.urlunparse(rest + (urllib.urlencode(values), None))

    def make_open_http(self):
        proxy_support = urllib2.ProxyHandler({'http': '127.0.0.1:8118'})
        """Tor support"""
        cooki_support = urllib2.HTTPCookieProcessor()
        """Cookies support"""
        opener = urllib2.build_opener(cooki_support, proxy_support)
        # opener = urllib2.build_opener(proxy_support)
        # opener = urllib2.build_opener(cooki_support)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]  # Hacking
        urllib2.install_opener(opener)

        def open_http(method, url, values={}):
            if method == "POST":
                return opener.open(url, urllib.urlencode(values))
            else:
                self.logger.debug('url %s ' % url)
                self.logger.debug('params % s' % urllib.urlencode(values))
                self.logger.debug('full %s ' % self.url_with_query(url, values))
                return opener.open(self.url_with_query(url, values))

        return open_http

    def login(self):
        """
        Method to make a login happen

        Handles all the login information and handling of form submission.
        """
        self.go(self.login_page)
        self.logger.debug('Login into the system as ' + self.login_username)
        # Login form is right after the search form
        try:
            login_form = self.html.forms[1]
        except:
            self.mailman.write('Login form find fail, please check the logs')
            self.logger.error("Login form find fail")
            self.logger.debug("Current login: %s " % self.login_username)
            return False

        login_form.action = 'http://www.stocktargetprices.com/login?mode=login'
        login_form.fields['username'] = self.login_username
        login_form.fields['password'] = self.login_password

        submit_values = {'input': login_form.fields['Login']}

        submit_form(
            login_form,
            extra_values=submit_values,
            open_http=self.open_http
        )

    def login_check(self):
        """
        Checking if the login was successfully
        """
        self.go("my-account")

        if len(self.html.xpath('//a[@href="/login?mode=logout"]')) == 0:
            self.logger.debug('User %s is not logged in' % self.login_username)
            return False
        else:
            self.logger.debug('User %s is logged in' % self.login_username)
            return True

    def targetprice_parse_list(self, ticker=None):
        """
        Method to visit the company page and get the list of the target prices
        """

        # table = self.html.xpath('//table[2]/tbody/tr[position()>1]')
        table = self.html.xpath('//table[2]/tr')
        """Select the second table in the page"""

        if len(table) <= 0:
            """
            This only means, that there exists only one table, trying it
            """
            table = self.html.xpath('//table[1]/tr')
            if len(table) <= 0:
                self.logger.error("Companies target table select fail")
                return False

        self.target_price_list = []

        for entry in table:
            # items = entry.text_content().replace('\t', '').split('\n')[:-1]
            items = entry.getchildren()
            """Split the table entry row into places"""
            try:
                prices = re.findall(
                    r'[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', items[3].text_content().replace('\t', ''))
            except IndexError:
                self.logger.debug('Target price failed')
                return False

            # prices = re.findall(
                # r'[0-9,\,]+\.?[0-9]+', entry.text_content().replace('\t', ''))
            """Scan and find any prices"""

            if len(prices) == 0:
                """Check if there is less than two prices"""
                prices.append('0')
                prices.append('0')
                """Add an old price as zero"""
            elif len(prices) == 1:
                """
                check
                """
                prices.append('0')

            # self.logger.debug('Plain data: ' + entry.text_content().strip())
            # Month-Day-Year (stupid Americans)
            date = datetime.strptime(
                items[-1].text_content().strip(),
                "%m/%d/%y"  # Stupid America
            )

            item = {
                'action': items[0].text_content().strip(),
                'analytic': items[1].text_content().strip(),
                'rating': items[2].text.strip(),
                'price0': prices[0],
                'price1': prices[1],
                'date': date.strftime('%Y-%m-%d'),
                'ticker': ticker
            }
            """Form a list item"""

            self.logger.debug("Filtered data: " + json.dumps(item))

            self.target_price_list.append(item)
            """Append to the buffer"""

        if len(self.target_price_list) >= 1:
            return True
        else:
            self.logger.error("Target price list fail")
            self.logger.debug("Current url: " + self.current_url)
            self.logger.debug("Data\n" + json.dumps(self.target_price_list))
            return False

    def load_tickers(self):
        """
        Method to load the ticker
        """
        self.csv_data.read()
        self.tickers = self.csv_data.data()

    def go(self, page, params=[], cycle=1):
        """
        Method to go to the page
        """
        self.logger.debug('Going to: ' + page)
        try:
            self.html = fromstring(self.open_http("GET", self.url + page, params).read())
            self.current_url = self.url + page
        except urllib2.URLError:
            self.logger.debug('Urllib2.URLError : ' + self.url + page)
            self.logger.debug('Sleepying %s seconds' % 10*cycle)
            time.sleep(10*cycle)  # Sleeping time
            self.logger.debug('Sleeping finished')
            if cycle < 5:
                self.logger.debug('Trying again')
                self.go(page, params, cycle + 1)
            else:
                self.logger.debug('Connection to the page completely failed')
                self.logger.debug('Shutting down')
                return False
        return True

    def process(self, ticker=None):
        """
        Processing
        """
        self.go('companies/', {'q': ticker})
        if self.targetprice_parse_list(ticker):
            for tp in self.target_price_list:
                self.rest.send('POST', '/api/target_prices/', tp)

    def start(self):
        """
        Starting the process
        """
        self.load_tickers()
        self.login()
        # self.process('F')
        for ticker in self.tickers:
            if self.login_check():
                sleep_for = int(random() * 10)
                self.logger.debug('Sleeping for %s' % sleep_for)
                time.sleep(sleep_for)
                print "Processing %s" % ticker['ticker']
                self.process(ticker['ticker'])
            else:
                self.login()

            sleep_for = int(random() * 100)
            self.logger.debug('Sleeping for %s' % sleep_for)
            time.sleep(sleep_for)

if __name__ == '__main__':
    m = main('arvydas.tamulis@gmail.com', 'liko789')
    m.start()
