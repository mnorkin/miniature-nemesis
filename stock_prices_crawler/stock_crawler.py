"""
The stock crawler is the deamon which collects the data
from the yahoo stock prices and
"""
import re
import urllib as u
import logging
import os
import json
import httplib
import time
from datetime import date


class stock_crawler():

    def __init__(self):
        """
        """
        self.absolute_path = os.path.dirname(os.path.realpath(__file__))
        self.full_path = self.absolute_path + '/logs/'
        self.logging_file = self.full_path + date.today().isoformat() + '.log'
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
        The main guy in the field
        """
        pass

    def get_tickers(self):
        """
        Going to the page and fetch the tickers

        * Make the json response happen
        """
        response_data = self.rest('/api/tickers/', 'GET')
        if response_data:
            return "+".join((ticker['name'] for ticker in response_data))

    def get_data(self, ticker=None):
        PATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
        url = 'http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=b3c6p&e=.csv' % (
            ticker.upper())
        f = u.urlopen(url, proxies={})
        rows = f.readlines()
        r = rows[0]
        # return HttpResponse(r)
        """Get the first entry"""
        r = PATTERN.split(r[:-2])[1::2]
        """Remove the `\r\n` and split by comma"""

        r[1].replace('"', '')
        change = r[1]
        last_stock_price = float(r[0])
        change_percent = 0
        change_direction = 'up'

        if (change[1] == '+'):
            """Positive change"""
            change = change[2:-1]
            """Drop the sign"""
            change_direction = 'up'
        else:
            """Negative change"""
            change = change[2:-1]
            """Drop the sign"""
            change_direction = 'down'

        change = float(change)

        if change == 0:
            last_stock_price = r[2]

        if change != 0:
            change_percent = round(change / (last_stock_price - change) * 100, 2)
        else:
            change_percent = 0

        item = {
            "last_stock_price": last_stock_price,
            "change": change,
            "change_percent": change_percent,
            "change_direction": change_direction
        }
        return item

    def rest(self, url, request, data=None, cycle=1):
        """
        Rest interface for the crawler API
        """
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        # conn = httplib.HTTPConnection("cra.baklazanas.lt")
        conn = httplib.HTTPConnection("localhost:8000")
        logging.debug(url)
        logging.debug(headers)
        logging.debug(params)
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
            logging.debug("Received 502 error")
            time.sleep(1000*cycle)
            if cycle < 10:
                return self.rest(url, request, data, cycle + 1)
            else:
                return False

if __name__ == '__main__':
    sc = stock_crawler()
    sc.start()
