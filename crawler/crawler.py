#!/usr/bin/python2
"""
Crawler

App written specially for the Target Price project.

"""
from lxml.html import fromstring  # More control
from lxml.html import submit_form  # Form submit
from random import shuffle
import json
import httplib
import re
import datetime
import urlparse
import urllib
import urllib2


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
        self.open_http = self.make_open_http()

        self.shuffle_letter()  # Shuffle letter for initial browsing

    def url_with_query(self, url, values):
        parts = urlparse.urlparse(url)
        rest, (query, frag) = parts[:-2], parts[-2:]
        return urlparse.urlunparse(rest + (urllib.urlencode(values), None))

    def make_open_http(self):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        opener.addheaders = []  # Hacking

        def open_http(method, url, values={}):
            if method == "POST":
                return opener.open(url, urllib.urlencode(values))
            else:
                return opener.open(self.url_with_query(url, values))

        return open_http

    def go(self, page):
        """
        Method to go to the page
        """
        self.html = fromstring(self.open_http("GET", self.url + page).read())
        # self.html = parse(self.url + page).getroot()
        # self.current_url = self.url + page

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

        There are two possibilities: go for the pop() method, which returns the
        last element from the list and removes it from the list completely, or
        just say make a single request and keep all the letters in the alphabet.

        The random letters distribution is uniform, so there is equal
        probability for each letter to pop-out
        """
        shuffle(self.alphabet)  # Randomize the list
        self.letter = str(self.alphabet[1])  # Return the letter

    def companies_next_page_available(self):
        """
        Checking if there is a next page in the current page

        The method gets the links from the page_nav_bar class element and
        fetches which of the following links are `last` and which is `previous`.
        Using the numbers of those links (pagination numbers), one can define
        then the page has reached its limit.
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

        The method sends the target price data to the Crawler API server.
        """

        for target_price in self.target_price_list:
            response = self.rest("/api/target_prices/", "POST", target_price)
            if not response:
                print "Target price send fail"
                return False

        return True
        """
        Return true if everything was send successfully
        """

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

            # Month-Day-Year (stupid Americans)
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

    def digesture_companies_list(self):
        """
        Method to scroll the companies list
        """

        something_was_sent = False
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
                    if self.send_target_prices():
                        something_was_sent = True
                else:
                    print "Ticker target price list fail"
                    return False
            else:
                """
                API said it's ok, go on to the next one
                """
                print "Ticker does not exist or is very confidential with data"

        return something_was_sent

    def companies(self):
        """
        Method to crawl the companies page
        """
        self.go(
            self.companies_page
            + '/' + self.letter + '/' + str(self.page_number)
        )  # Go the companies list page, with specific letter and page number

        self.companies_parse_list()  # Make the list of companies in the page
        if self.digesture_companies_list():  # Scroll through every company and check with server
            """Check if any company in the list was good for the serve"""
            self.shuffle_letter()  # Shuffle the random letter
            self.page_number = 1  # Reset page numbering
            self.companies()  # Start all over again
        else:
            """If no companies data was sent -- switch to the next page if available"""
            if self.companies_next_page_available:  # If there is any more pages
                self.page_number = self.page_number + 1  # Add next page
            else:
                self.shuffle_letter()  # Shuffle the next letter
                self.page_number = 1  # Reset the pages
            self.companies()  # Keep the job going

    def login(self):
        """
        Method to make a login happen

        Handles all the login information and handling of form submission.
        """
        self.go(self.login_page)
        # Login form is right after the search form
        try:
            login_form = self.html.forms[1]
        except Exception, e:
            raise e
            return False

        login_form.action = self.url + '/' + login_form.action
        login_form.fields['username'] = 'arvydas.tamulis@gmail.com'
        login_form.fields['password'] = 'liko789'

        submit_values = {'submit': login_form.fields['Login']}

        submit_form(
            login_form,
            extra_values=submit_values, open_http=self.open_http
        )

        return True

if __name__ == '__main__':
    cra = crawler()  # Define the crawler
    cra.login()  # Make the login happen
    cra.companies()  # Go to the companies page and start the job
