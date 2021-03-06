#!/usr/bin/python2
"""
Crawler

App written specially for the Target Price project.

"""
from lxml.html import fromstring  # More control
from lxml.html import submit_form  # Form submit
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
import argparse
import settings


class crawler():
    """
    Crawler class
    """

    def __init__(self, _login_username, _login_password):
        """
        Initialization of the crawler buddy
        """
        self.url = 'http://stocktargetprices.com/'
        self.current_url = self.url
        self.html = None
        self.login_page = 'login'
        self.login_username = _login_username
        self.login_password = _login_password
        self.companies_page = 'companies'
        self.alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.letter = None
        self.ticker = None  # This is v2 addition, stores ticker
        self.name = None  # This is v2 adddition, stores company name
        self.page_number = 1
        self.debug = True
        self.companies_list = []
        self.target_price_list = []
        self.open_http = self.make_open_http()
        self.absolute_path = os.path.dirname(os.path.realpath(__file__))
        self.logging_file = self.absolute_path + '/logs/' + date.today().isoformat() + '.log'
        self.logging_level = logging.DEBUG
        self.start_hour = 0  # Then the crawler starts its job
        self.len_hour = 7  # How long in hours the crawler works
        self.mailman = mailman(
            'AKIAJKFJFUKWVJSBYA5Q',
            'tdIQlhdUjXAC+CUkNPXjKLir3LuZKDiW2q96CFZn')  # Mail-man keys to the box

        logging.basicConfig(
            filename=self.logging_file,
            level=self.logging_level, format='%(asctime)s %(message)s')

    def run(self):
        """
        Main things happens here.

        Need to implement the threading right here
        """
        sleep_for = int(random() * 100)
        logging.debug('Randomizing the start for %s ' % self.login_username)
        logging.debug('Delaying %s seconds' % sleep_for)
        # time.sleep(sleep_for)
        logging.debug('And here it goes')
        self.login()  # Make the login happen

        while (self.check_time()):
            self.companies()  # Go to the companies page and start the job
            sleep_time = int(random() * 200) + 30
            logging.debug("Sleeping: " + str(sleep_time))
            time.sleep(sleep_time)
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
            datetime.now().hour < self.start_hour + self.len_hour
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
        # opener = urllib2.build_opener(cooki_support, proxy_support)
        # opener = urllib2.build_opener(proxy_support)
        opener = urllib2.build_opener(cooki_support)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]  # Hacking
        urllib2.install_opener(opener)

        def open_http(method, url, values={}):
            if method == "POST":
                return opener.open(url, urllib.urlencode(values))
            else:
                logging.debug('url %s ' % url)
                logging.debug('params % s' % urllib.urlencode(values))
                logging.debug('full %s ' % self.url_with_query(url, values))
                return opener.open(self.url_with_query(url, values))

        return open_http

    def go_absolute(self, _url):
        """
        Absolute go to the page
        """
        self.html = fromstring(self.open_http("GET", _url).read())

    def go(self, page, params=[], cycle=1):
        """
        Method to go to the page
        """
        logging.debug('Going to: ' + page)
        try:
            self.html = fromstring(self.open_http("GET", self.url + page, params).read())
            self.current_url = self.url + page
        except urllib2.URLError:
            logging.debug('Urllib2.URLError : ' + self.url + page)
            time.sleep(100*cycle)  # Sleeping time
            if cycle < 5:
                self.go(page, params, cycle + 1)
            else:
                mailman.write('Cannot connect to the page')
                logging.debug('Connection to the page failed')
                return False
        return True

    def rest_with_response(self, url, request, data=None, cycle=1):
        """
        Rest interface for the crawler API

        Then the page does not respond, returning the 502 error, added a
        listener for that. Waiting ensures, that nothing does drop off, and
        one can immediately respond to such a system fault, because the email
        is deployed to the developer.
        """
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        # conn = httplib.HTTPConnection("cra.baklazanas.lt")
        # conn = httplib.HTTPConnection("localhost:8000")
        conn = httplib.HTTPConnection(settings.rest_url)
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        raw_response = response.read()
        conn.close()
        if response.status != 502:
            # ALL_OK
            if response.status == 200 and request.upper() == 'GET':
                return json.loads(raw_response)
            # CREATED
            elif response.status == 201 and request.upper() == 'POST':
                return json.loads(raw_response)
            # ALL_OK
            elif response.status == 200 and request.upper() == 'PUT':
                return json.loads(raw_response)
            # DELETED
            elif response.status == 204 and request.upper() == 'DELETE':
                return json.loads(raw_response)
            else:
                return None
        else:
            logging.debug('Received 502 error on connecting to\
cra.baklazanas.lt, sleeping')
            time.sleep(1000*cycle)  # Sleeping
            if cycle < 10:
                return self.rest(url, request, data, cycle + 1)
            else:
                mailman.write('Cannot connect to cra.baklazanas.lt, check logs')
                logging.error('Cannot connect to cra.baklazanas.lt')
                return False

    def rest(self, url, request, data=None, cycle=1):
        """
        Rest interface for the crawler API

        Then the page does not respond, returning the 502 error, added a
        listener for that. Waiting ensures, that nothing does drop off, and
        one can immediately respond to such a system fault, because the email
        is deployed to the developer.
        """
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        # conn = httplib.HTTPConnection("cra.baklazanas.lt")
        conn = httplib.HTTPConnection(settings.rest_url)
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        conn.close()
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
            logging.debug('Received 502 error on connecting to\
cra.baklazanas.lt, sleeping')
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

        response = self.rest_with_response('/api/tickers/', 'GET')
        # Name filtering with TEX ticker
        # response = {}
        # response['ticker'] = 'TEX'
        # response['name'] = 'Terex Corporation'
        # New method with v2
        # Name lower filtering with PRE ticker
        # response = {}
        # response['ticker'] = 'PRE'
        # response['name'] = 'PartnerRe Ltd.'
        # shuffle(self.alphabet)  # Randomize the list
        logging.debug('Received ticker %s' % response['ticker'])
        logging.debug('Received ticker %s' % response['name'])
        self.letter = str(response['ticker'][0])  # Return the letter
        self.ticker = response['ticker']
        self.name = response['name']
        self.page_number = 1  # also reset the page numbering

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
        # link_previous = self.html.xpath(
        #     '//div[@class="page_nav_bar"][1]/a[text()="previous"]')[0]

        logging.debug('Checking if there are more pages')
        logging.debug(link_last.attrib['href'].split('/')[-1])
        logging.debug(self.page_number)

        if (
            int(link_last.attrib['href'].split("/")[-1]) == self.page_number
        ):
            logging.debug("No more pages available")
            logging.debug("Current Url: " + self.current_url)
            logging.debug("Current login: %s " % self.login_username)
            return False
        else:

            logging.debug("Pages are available")
            logging.debug("Current Url: " + self.current_url)
            logging.debug("Current login: %s " % self.login_username)
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
        if company_index:
            self.go(self.companies_list[company_index]['link'])
            ticker = self.companies_list[company_index]['ticker']
        else:
            ticker = self.ticker

        # table = self.html.xpath('//table[2]/tbody/tr[position()>1]')
        table = self.html.xpath('//table[2]/tr')
        """Select the second table in the page"""

        if len(table) <= 0:
            """
            This only means, that there exists only one table, trying it
            """
            table = self.html.xpath('//table[1]/tr')
            if len(table) <= 0:
                self.mailman.write('Companies target table select fail, please check the logs')
                logging.error("Companies target table select fail")
                logging.debug("Current url: " + self.current_url)
                logging.debug("Table contents\n" + self.html.text_content())
                return False

        self.target_price_list = []

        for entry in table:
            # items = entry.text_content().replace('\t', '').split('\n')[:-1]
            items = entry.getchildren()
            """Split the table entry row into places"""
            prices = re.findall(
                r'[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', items[3].text_content().replace('\t', ''))
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

            # logging.debug('Plain data: ' + entry.text_content().strip())
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

            logging.debug("Filtered data: " + json.dumps(item))

            self.target_price_list.append(item)
            """Append to the buffer"""

        if len(self.target_price_list) >= 1:
            return True
        else:
            self.mailman.write('Target Price list fail, please check the logs')
            logging.error("Target price list fail")
            logging.debug("Current url: " + self.current_url)
            logging.debug("Data\n" + json.dumps(self.target_price_list))
            return False

    def companies_parse_list(self, version=1):
        """
        Parse companies list
        """
        if version == 2:
            links = self.html.xpath('//div[@class="block"]//a')
        else:
            links = self.html.xpath('//div[@id="company-list"]//a')

        if len(links) < 1:
            self.mailman.write('Company-list selector link fail, please check the logs')
            logging.error("company-list links select fail")
            logging.debug("Current url: " + self.current_url)
            logging.debug("Current login: %s " % self.login_username)
            return False

        self.companies_list = []

        for link in links:
            logging.debug(link.text)
            item = {
                'name': " ".join(re.findall('\S+', link.text)[:-1]),
                'market': re.findall('\w+', re.findall('\S+', link.text)[-1])[0],
                'ticker': re.findall('\w+', re.findall('\S+', link.text)[-1])[1],
                'link': link.attrib['href']
            }
            self.companies_list.append(item)

        if len(self.companies_list) >= 1:
            return True
        else:
            self.mailman.write('Companies list length fail, please check the logs')
            logging.error("Companies list length fail")
            logging.debug("Current url: " + self.current_url)
            logging.debug("Current login: %s " % self.login_username)
            return False

    def digesture_companies_list(self):
        """
        Method to scroll the companies list
        """

        # something_was_sent = False
        for company_index, company in enumerate(self.companies_list):
            company_name_form_page = re.sub('\W+', '', company['name'].lower())
            company_name_from_api = re.sub('\W+', '', self.name.lower())
            company_ticker_from_page = company['ticker']
            company_ticker_from_api = self.ticker
            logging.debug('Company having %s, given %s' % (company_name_form_page, company_name_from_api))
            logging.debug('Ticker having %s, given %s' % (company_ticker_from_page, company_ticker_from_api))
            if company_ticker_from_page == company_ticker_from_api:
                logging.debug('Ticker equals')
            else:
                logging.debug('Ticker does not equals')

            if company_name_form_page == company_name_from_api:
                logging.debug('Name equals')
            else:
                logging.debug('Name not equals')

            if company_ticker_from_page == company_ticker_from_api and company_name_form_page == company_name_from_api:
                response = True
            else:
                response = False

            if response:
                """
                Feed the API with data
                """
                logging.debug("Ticker %s exists and needs data, making the data happen" % company['ticker'])
                if self.targetprice_parse_list(company_index):
                    if self.send_target_prices():
                        return True
                else:
                    logging.error("Ticker target price list fail")
                    logging.debug("Current url: " + self.current_url)
                    logging.debug("Current login: %s " % self.login_username)
            else:
                """
                API said it's ok, go on to the next one
                """
                # logging.debug("Ticker %s does not exist or is very confidential with data" % company['ticker'])
                # logging.debug("Current login: %s " % self.login_username)
                logging.debug('Skip %s ' % company['ticker'])

        return False

    def companies(self):
        """
        Method to crawl the companies page
        """
        # self.go(
            # self.companies_page
            # + '/' + self.letter + '/' + str(self.page_number)
        # )  # Go the companies list page, with specific letter and page number

        self.shuffle_letter()
        self.search()

        logging.debug('Ticker %s' % self.ticker)

        if self.companies_parse_list(version=2):
            logging.debug('Companies list found')
            if self.digesture_companies_list():  # Scroll through every company and sent data
                logging.debug('Something was sent')
        elif self.targetprice_parse_list():
            logging.debug('Target price list found')
            if self.send_target_prices():
                logging.debug('Target price sent, ticker %s' % self.ticker)
                return True
        else:
            logging.debug('No results found')

        # self.companies_parse_list()  # Make the list of companies in the page
        # if self.digesture_companies_list():  # Scroll through every company and check with server
        #     """Check if any company in the list was good for the serve"""
        #     logging.debug("Some target price data was send from the list")
        #     logging.debug("Continue with the next letter from the big list")
        #     self.shuffle_letter()  # Shuffle the random letter
        #     logging.debug("Next letter: " + self.letter)
        #     logging.debug("Current login: %s " % self.login_username)
        # else:
        #     """If no companies data was sent -- switch to the next page if available"""
        #     logging.debug("No companies data was send, consider to go to the\
        #         next page or switch to the next letter")
        #     self.go(
        #         self.companies_page
        #         + '/' + self.letter + '/' + str(self.page_number))
        #     if self.companies_next_page_available:  # If there is any more pages
        #         self.page_number = self.page_number + 1  # Add next page
        #         logging.debug("Moving to the next page: " + str(self.page_number))
        #         logging.debug("Current login: %s " % self.login_username)
        #     else:
        #         self.shuffle_letter()  # Shuffle the next letter
        #     return  # Return to main

    def search(self):
        """
        Method to make a search happen
        """
        logging.debug('Making the search')
        # try:
        #     search_form = self.html.forms[0]
        # except:
        #     logging.error('Search form is not found')
        #     return False

        self.go('companies/', {'q': self.ticker})

        # search_form.action = self.url + '/' + search_form.action
        # search_form.fields['q'] = self.ticker

        # submit_values = {'submit': 'Search'}

        # submit_form(
        #     search_form,
        #     extra_values=submit_values, open_http=self.open_http
        # )

    def login(self):
        """
        Method to make a login happen

        Handles all the login information and handling of form submission.
        """
        self.go(self.login_page)
        logging.debug('Login into the system as ' + self.login_username)
        # Login form is right after the search form
        try:
            login_form = self.html.forms[1]
        except:
            self.mailman.write('Login form find fail, please check the logs')
            logging.error("Login form find fail")
            logging.debug("Current login: %s " % self.login_username)
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

        # return self.login_check()

    def login_check(self):
        """
        Checking if the login was successfully
        """
        self.go("my-account")

        if len(self.html.xpath('//a[@href="/login?mode=logout"]')) == 0:
            logging.debug('User %s is not logged in' % self.login_username)
            return False
        else:
            logging.debug('User %s is logged in' % self.login_username)
            return True

if __name__ == '__main__':
    # Set arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--account')
    args = parser.parse_args()
    if args.account == '1':
        print "Running 1 login"
        cra = crawler('arvydas.tamulis@gmail.com', 'liko789')
        cra.run()
    elif args.account == '2':
        print "Running 2 login"
        cra = crawler('trialseoproject@gmail.com', 'saras86')
        cra.run()
    else:
        print args
