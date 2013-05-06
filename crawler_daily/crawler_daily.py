#!/usr/bin/python2
"""
The Daily crawler
"""
from lxml.html import fromstring  # Making tree from string
from datetime import date
from datetime import datetime
import logging
import os
import urllib
import urllib2
import urlparse
import json
import httplib
import time
import re
import settings


class crawler_daily():
    """
    The daily guy matters
    """

    def __init__(self):
        """
        Initialization of the younger crawler guy
        """
        self.url = 'http://stocktargetprices.com/'
        self.current_url = self.url
        self.html = None
        self.open_http = self.make_open_http()
        self.absolute_path = os.path.dirname(os.path.realpath(__file__))
        self.logging_file = self.absolute_path + '/logs/' + date.today().isoformat() + '.log'
        self.logging_level = logging.DEBUG
        # Check if the log directory exists
        self.log_dir_check()

        logging.basicConfig(
            filename=self.logging_file,
            level=self.logging_level, format='%(asctime)s %(message)s')

    def log_dir_check(self):
        """
        Checking if log directory exists
        """
        if not os.path.exists(self.absolute_path + '/logs/'):
            os.makedirs(self.absolute_path + '/logs/')

    def start(self):
        """
        All the fun
        """
        # Collect all the target prices
        if self.targetprice_parse_list():
            if self.send_target_prices():
                logging.debug('Target prices collected')
            else:
                logging.debug('Target price send fail')
        else:
            logging.debug('Target price parse list fail')

    def go(self, page, cycle=1):
        """
        Making the go happen
        """
        logging.debug("Going to %s " % page)
        try:
            self.html = fromstring(
                self.open_http("GET", self.url + page).read()
            )
            self.current_url = self.url + page
        except urllib2.URLError:
            logging.debug("Urllib2 Error : %s " % self.url + page)
            time.sleep(1000*cycle)  # Sleeping time
            if cycle < 10:
                self.go(page, cycle + 1)
            else:
                logging.debug("Connection to the page failed")
                return False
        return True

    def url_with_query(self, url, values):
        parts = urlparse.urlparse(url)
        rest, (query, frag) = parts[:-2], parts[-2:]
        return urlparse.urlunparse(rest + (urllib.urlencode(values), None))

    def make_open_http(self):
        proxy_support = urllib2.ProxyHandler({'http': '127.0.0.1:8118'})
        cooki_support = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cooki_support, proxy_support)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)

        def open_http(method, url, values={}):
            if method == "POST":
                return opener.open(url, urllib.urlencode(values))
            else:
                return opener.open(self.url_with_query(url, values))

        return open_http

    def rest(self, url, request, data=None, cycle=1):
        """
        Rest interface for the crawler API
        """
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        # conn = httplib.HTTPConnection("cra.baklazanas.lt")
        # conn = httplib.HTTPConnection("localhost:8000")
        conn = httplib.HTTPConnection(settings.rest_url)
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        conn.close()
        if response.status == 500:
            # This parameter is return, then there is error from the server
            # side
            logging.debug('500 ERROR')
            logging.debug('***')
            logging.debug(url)
            logging.debug(headers)
            logging.debug(params)
            logging.debug('***')
        if response.status == 404:
            logging.debug('404 returned')
            logging.debug(params)
        if response.status != 502:
            # ALL_OK
            if response.status == 200 and request.upper() == 'GET':
                return True
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
            logging.debug("Received 502 error")
            time.sleep(1000*cycle)
            if cycle < 10:
                return self.rest(url, request, data, cycle + 1)
            else:
                return False

    def send_target_prices(self):
        """
        Method to send the target prices
        """

        for target_price in self.target_price_list:
            response = self.rest("/api/target_prices/", "POST", target_price)
            if not response:
                logging.error("FAIL Target price send data")
            else:
                logging.error("OK Target price send")
        return True

    def targetprice_parse_list(self):
        """
        Parsing the target price list
        """
        self.go('')

        table = self.html.xpath('//table[1]/tr')

        if len(table) <= 0:
            """
            This means only that the page have changed, dropping
            """
            logging.error('Specified table not found')
            return False

        self.target_price_list = []

        for entry in table:
            items = entry.getchildren()
            prices = re.findall(
                r'[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', items[4].text_content().replace('\t', ''))

            # No prices found
            if len(prices) == 0:
                prices.append('0')
                prices.append('0')
            elif len(prices) == 1:
                prices.append('0')

            parsed_date = datetime.strptime(
                items[-1].text_content().strip(),
                "%m/%d/%y"  # Stupid America
            )

            parsed_raiting = items[3].text

            if parsed_raiting is None:
                parsed_raiting = 'NULL'

            # Form a list
            item = {
                'action': items[0].text_content().strip(),
                'analytic': items[2].text_content().strip(),
                'rating': parsed_raiting,
                'price0': prices[0],
                'price1': prices[1],
                'date': parsed_date.strftime('%Y-%m-%d'),
                'company_name': items[1].text_content().strip()  # Need to change in the APIs
            }
            # Construct the list
            self.target_price_list.append(item)

        if len(self.target_price_list) >= 1:
            return True
        else:
            logging.error('Target price list construct fail')
            return False

if __name__ == '__main__':
    cra_daily = crawler_daily()
    cra_daily.start()  # Make this happen
