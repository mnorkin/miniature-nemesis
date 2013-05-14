"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

The test manager, just to be on the safe side of the road
"""

from django.utils import unittest
from django.test.client import Client
from morbid.models import Analytic
from morbid.models import Ticker


class AnalyticTest(unittest.TestCase):
    """
    Testing `last_target_price`
    """
    def setUp(self):
        """
        Setting up the environment
        """
        self.goldman = Analytic(
            name='Goldman',
            slug='goldman'
        )

        self.jp = Analytic(
            name='JP',
            slug='jp'
        )
        self.aapl = Ticker(
        )


class UrlTest(unittest.TestCase):
    """
    Url tester
    """

    def setUp(self):
        self.client = Client()

    def test_index(self):
        """
        Test for the index page
        """
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_analytic(self):
        """
        Test for the analytic page
        """
        response = self.client.get('/analytic/')
        """Testing general request"""
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/analytic/rbc-capital-markets')
        """Testing specific request"""
        self.assertEqual(response.status_code, 200)

    def test_ticker(self):
        """
        Test for the ticker page
        """
        response = self.client.get('/ticker/')
        """Testing general request"""
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/ticker/agn')
        """Testing specific request"""
        self.assertEqual(response.status_code, 200)
