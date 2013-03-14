#!/usr/bin/python2
"""
Crawler
"""
from lxml.html import parse  # Page parser
# from lxml.html import submit_form # Form submit
from random import shuffle
import json
import httplib


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
        if self.debug:
            self.url = 'http://mstock.lt/'
            self.companies_page = 'list.html'

    def rest(self, url, request, data):
        """
        Rest interface for the crawler API
        """
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        conn = httplib.HTTPConnection("localhost:8000")
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        conn.close()
        if response.status == 200 and request.upper() == 'GET':  # ALL_OK
            return json.loads(response.read())
        elif response.status == 201 and request.upper() == 'POST':  # CREATED
            return json.loads(response.read())
        elif response.status == 200 and request.upper() == 'PUT':  # ALL_OK
            return json.loads(response.read())
        elif response.status == 204 and request.upper() == 'DELETE':  # DELETED
            return json.loads(response.read())
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

    def companies_parse_list(self):
        """
        Parse companies list
        """
        links = self.html.xpath('//div[@id="company-list"]//a')

        companies_list = []

        for link in links:
            item = {
                'name': link.text.split("(")[0].strip(),
                'market': link.text.split("(")[1].split(")")[0].split(":")[0],
                'ticker': link.text.split("(")[1].split(")")[0].split(":")[1],
                'link': link.attrib['href']
            }
            companies_list.append(item)
        return companies_list

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
        companies_list = self.companies_parse_list()
        response = self.rest("tickers/", "GET", companies_list[0])
        if response:
            print response

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

        login_form.fields['username'] = ''
        login_form.fields['password'] = ''

if __name__ == '__main__':
    print "Direct call"
    cra = crawler()
    print cra.companies()
