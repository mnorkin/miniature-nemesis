#!/usr/bin/python2
"""
Crawler
"""
from lxml.html import parse  # Page parser
from lxml.html import submit_form # Form submit
from random import shuffle
import json
import httplib
import re
import datetime

class crawler():
    """
    Crawler class
    """

    def __init__(self):
        """
        Initialization of the crawler buddy
        """
        self.url = 'http://stocktargetprices.com/'
        self.current_url = self.url
        self.html = None
        self.login_page = 'login'
        self.companies_page = 'companies'
        self.alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.letter = None
        self.page_number = 1
        self.debug = True
        self.companies_list = []
        self.target_price_list = []
        # if self.debug:
            # self.url = 'http://mstock.lt/'
            # self.companies_page = 'list.html'
            # self.company_page = 'aapl.html'

    def rest(self, url, request, data=None):
        """
        Rest interface for the crawler API
        """
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        conn = httplib.HTTPConnection("localhost:8000")
        print "Request: ", request
        print "Params: ", params
        print "Headers: ", headers
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        conn.close()
        if response.status == 200 and request.upper() == 'GET':  # ALL_OK
            return True
        elif response.status == 201 and request.upper() == 'POST':  # CREATED
            return True
        elif response.status == 200 and request.upper() == 'PUT':  # ALL_OK
            return True
        elif response.status == 204 and request.upper() == 'DELETE':  # DELETED
            return True
        else:
            return None

    def shuffle_letter(self):
        """
        Method to shuffle the alphabet and return random letter
        """
        shuffle(self.alphabet)
        self.letter = str(self.alphabet.pop())

    def go(self, page):
        """
        Method to go to the page
        """
        self.html = parse(self.url + page).getroot()
        self.current_url = self.url + page

    def companies_next_page_available(self):
        """
        Checking if there is a next page in the current page
        """
        link_last = self.html.xpath(
            '//div[@class="page_nav_bar"][1]/a[text()="last"]')[0]
        link_previous = self.html.xpath(
            '//div[@class="page_nav_bar"][1]/a[text()="previous"]')[0]

        if (
            link_last.attrib['href'].split("/")[-1] ==
            link_previous.attr['href'].split("/")[-1] + 1
        ):
            return False
        else:
            return True

    def send_target_prices(self):
        """
        Method to send collected target prices
        """

        for target_price in self.target_price_list:
            response = self.rest("/api/target_prices/", "POST", target_price)
            if not response:
                print "Target price send fail"
                return False

    def targetprice_parse_list(self, company_index=None):
        """
        Method to visit the company page and get the list of the target prices
        """
        if self.debug:
            """
            For debugging, go to the local page
            """
            self.go(self.company_page)
        else:
            """
            For production, go to the appropriate page
            """
            self.go(self.companies_list[company_index]['link'])

        table = self.html.xpath('//table[2]/tbody/tr[position()>1]')
        """Select the second table in the page"""

        if len(table) < 1:
            print "Companies target price list fail"
            return False

        self.target_price_list = []

        for entry in table:
            items = entry.text_content().split('\n')[:-1]
            """Split the table entry row into places"""
            prices = re.findall(
                r'[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', items[3])
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

            # Month-Day-Year
            date = datetime.datetime.strptime(items[4], "%m/%d/%y")

            item = {
                'action': items[0],
                'analytic': items[1],
                'rating': items[2],
                'price0': prices[0],
                'price1': prices[1],
                'date': date.strftime('%Y-%m-%d'),
                'ticker': self.companies_list[company_index]['ticker']
            }
            """Form a list item"""

            self.target_price_list.append(item)
            """Append to the buffer"""

        if len(self.target_price_list) > 1:
            return True
        else:
            return False

    def companies_parse_list(self):
        """
        Parse companies list
        """
        links = self.html.xpath('//div[@id="company-list"]//a')

        if len(links) < 1:
            print "company-list links fail"
            return False

        self.companies_list = []

        for link in links:
            item = {
                'name': link.text.split("(")[0].strip(),
                'market': link.text.split("(")[1].split(")")[0].split(":")[0],
                'ticker': link.text.split("(")[1].split(")")[0].split(":")[1],
                'link': link.attrib['href']
            }
            self.companies_list.append(item)

        if len(self.companies_list) > 1:
            return True
        else:
            print "Companies list fail"
            return False

    def companies(self):
        """
        Method to crawl the companies page
        """
        self.shuffle_letter()  # Shuffle the random letter
        if self.debug:
            self.go(self.companies_page)
        else:
            self.go(
                self.companies_page
                + '/' + self.letter + '/' + str(self.page_number)
            )
        self.companies_parse_list()
        for company_index, company in enumerate(self.companies_list):
            if company['ticker'].isalpha():
                response = self.rest(
                    "/api/tickers/" + company['ticker'] + "/", "GET")
            else:
                response = None

            if response:
                """
                Feed the API with data
                """
                print "Ticker exists and needs data, making the data happen"
                if self.targetprice_parse_list(company_index):
                    self.send_target_prices()
                else:
                    print "Ticker target price list fail"
                    return False
            else:
                """
                API said it's ok, go on to the next one
                """
                print "Ticker does not exist or is very confidential with data"

    def login(self):
        """
        Method to make a login happen
        """
        self.go(self.login_page)
        # Login form is right after the search form
        try:
            login_form = self.html.forms[1]
        except Exception, e:
            raise e

        login_form.fields['username'] = 'arvydas.tamulis@gmail.com'
        login_form.fields['password'] = 'liko789'

        self.html = parse(submit_form(login_form)).getroot()

        return True

if __name__ == '__main__':
    cra = crawler()
    cra.companies()
