#!/usr/bin/python2
"""
Crawler

App written specially for the Target Price project.

"""
from lxml.html import fromstring  # More control
from lxml.html import submit_form  # Form submit
from random import shuffle
from random import random
from datetime import date
from datetime import datetime
import time
import json
import httplib
import re
import urlparse
import urllib
import urllib2  # Access interwebs
import logging  # Logging
import os  # Directories
from mailman import mailman


class crawler():
    """
    Crawler class
    """

    def __init__(self):
        """
        Initialization of the crawler buddy
        """
        self.url = 'http://stocktargetprices2.com/'
        self.current_url = self.url
        self.html = None
        self.login_page = 'login'
        self.login_username = 'arvydas.tamulis@gmail.com'
        self.login_password = 'liko789'
        self.companies_page = 'companies'
        self.alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.letter = None
        self.page_number = 1
        self.debug = True
        self.companies_list = []
        self.target_price_list = []
        self.open_http = self.make_open_http()
        self.absolute_path = os.path.dirname(os.path.realpath(__file__))
        self.logging_file = self.absolute_path + '/logs/crawler_' + date.today().isoformat() + '.log'
        self.logging_level = logging.DEBUG
        self.start_hour = 1  # Then the crawler starts its job
        self.len_hour = 8  # How long in hours the crawler works
        self.mailman = mailman(
            'AKIAJKFJFUKWVJSBYA5Q',
            'tdIQlhdUjXAC+CUkNPXjKLir3LuZKDiW2q96CFZn')  # Mail-man keys to the box

        logging.basicConfig(
            filename=self.logging_file,
            level=self.logging_level, format='%(asctime)s %(message)s')

    def main(self):
        """
        Main things happens here.

        Need to implement the threading right here
        """

        self.shuffle_letter()  # shuffle letter for initial browsing
        self.login()  # Make the login happen
        self.login_check()  # Check if the user logged in

        while (self.check_time()):
            self.companies()  # Go to the companies page and start the job
            sleep_time = int(random() * 300) + 30
            time.sleep(sleep_time)
            logging.debug("sleeping: " + sleep_time)
            if not self.login_check():
                if not self.login():
                    mailman.write(
                        "User cannot login: %s. Quiting user support" % self.login_username)
                    logging.error("Login fail for user %s. Quitting it's support " % self.login_username)
                return

        logging.debug("Quitting")

    def check_time(self):
        """
        Time management guy
        """
        if (
            datetime.now().hour >= self.start_hour and
            datetime.now() < self.start_hour + self.len_hour
        ):
            return True
        else:
            time.sleep(300)  # Wait for 5 minutes
            return False

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
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]  # Hacking
        urllib2.install_opener(opener)

        def open_http(method, url, values={}):
            if method == "POST":
                return opener.open(url, urllib.urlencode(values))
            else:
                return opener.open(self.url_with_query(url, values))

        return open_http

    def go_absolute(self, _url):
        """
        Absolute go to the page
        """
        self.html = fromstring(self.open_http("GET", _url).read())

    def go(self, page, cycle=1):
        """
        Method to go to the page
        """
        try:
            self.html = fromstring(self.open_http("GET", self.url + page).read())
            self.current_url = self.url + page
            return True
        except urllib2.URLError:
            time.sleep(1000*cycle)  # Sleeping time
            if cycle < 10:
                self.go(page, cycle + 1)
            else:
                mailman.write('Cannot connect to the page')
                logging.debug('Connection to the page failed')
                return False

    def rest(self, url, request, data=None, cycle=1):
        """
        Rest interface for the crawler API
        """
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        conn = httplib.HTTPConnection("cra.baklazanas.lt")
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        conn.close()
        if response.status != 502:
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
        else:
            time.sleep(1000*cycle)  # Sleeping
            if cycle < 10:
                return self.rest(url, request, data, cycle + 1)
            else:
                mailman.write('Cannot connect to cra.baklazanas.lt, check logs')
                logging.error('Cannot connect to cra.baklazanas.lt')
                return False

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
            logging.debug("No more pages available")
            logging.debug("Current Url: " + self.current_url)
            return False
        else:
            logging.debug("Pages are available")
            logging.debug("Current Url: " + self.current_url)
            return True

    def send_target_prices(self):
        """
        Method to send collected target prices

        The method sends the target price data to the Crawler API server.
        """

        for target_price in self.target_price_list:
            response = self.rest("/api/target_prices/", "POST", target_price)
            if not response:
                self.mailman.write('Target price send fail, please check the logs')
                logging.error("Target price send fail")
                logging.debug("Data wanted to send: ")
                logging.debug(json.dumps(target_price))
                return False

        return True
        """
        Return true if everything was send successfully
        """

    def targetprice_parse_list(self, company_index=None):
        """
        Method to visit the company page and get the list of the target prices
        """
        self.go(self.companies_list[company_index]['link'])

        table = self.html.xpath('//table[2]/tbody/tr[position()>1]')
        """Select the second table in the page"""

        if len(table) < 1:
            self.mailman.write('Companies target table select fail, please check the logs')
            logging.error("Companies target table select fail")
            logging.debug("Current url: " + self.current_url)
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
            date = datetime.strptime(items[4], "%m/%d/%y")

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
            self.mailman.write('Target Price list fail, please check the logs')
            logging.error("Target price list fail")
            logging.debug("Current url: " + self.current_url)
            return False

    def companies_parse_list(self):
        """
        Parse companies list
        """
        links = self.html.xpath('//div[@id="company-list"]//a')

        if len(links) < 1:
            self.mailman.write('Company-list selector link fail, please check the logs')
            logging.error("company-list links select fail")
            logging.debug("Current url: " + self.current_url)
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
            self.mailman.write('Companies list length fail, please check the logs')
            logging.error("Companies list length fail")
            logging.debug("Current url: " + self.current_url)
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
                    self.mailman.write('Ticker target prices list fail, please check the logs')
                    logging.error("Ticker target price list fail")
                    logging.debug("Current url: " + self.current_url)
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
            logging.debug("Some target price data was send from the list")
            logging.debug("Continue with the next letter from the big list")
            self.shuffle_letter()  # Shuffle the random letter
            self.page_number = 1  # Reset page numbering
            logging.debug("Next letter: " + self.letter)
        else:
            """If no companies data was sent -- switch to the next page if available"""
            logging.debug("No companies data was send, consider to go to the\
                next page or switch to the next letter")
            if self.companies_next_page_available:  # If there is any more pages
                self.page_number = self.page_number + 1  # Add next page
                logging.debug("Moving to the next page: " + str(self.page_number))
            else:
                self.shuffle_letter()  # Shuffle the next letter
                self.page_number = 1  # Reset the pages
            return  # Return to main

    def login(self):
        """
        Method to make a login happen

        Handles all the login information and handling of form submission.
        """
        self.go(self.login_page)
        # Login form is right after the search form
        try:
            login_form = self.html.forms[1]
        except:
            self.mailman.write('Login form find fail, please check the logs')
            logging.error("Login form find fail")
            return False

        login_form.action = self.url + '/' + login_form.action
        login_form.fields['username'] = self.login_username
        login_form.fields['password'] = self.login_password

        submit_values = {'submit': login_form.fields['Login']}

        submit_form(
            login_form,
            extra_values=submit_values, open_http=self.open_http
        )

        return self.login_check()

    def login_check(self):
        """
        Checking if the login was successfully
        """
        self.go("my-account")

        if len(self.html.xpath('//a[@href="/login?mode=logout"]')) == 0:
            return False
        else:
            return True

if __name__ == '__main__':
    cra = crawler()  # Define the crawler
    cra.main()  # Launch the main guy into the wild
