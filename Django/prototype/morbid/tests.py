"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

The test manager, just to be on the safe side of the road
"""

from django.utils import unittest
from django.test.client import Client
from morbid.models import Analytic
from morbid.models import Ticker
from morbid.models import TargetPrice
from morbid.models import FeatureAnalyticTickerCheck
from morbid.utils import ticker_analytics
from morbid.utils import recent_target_data
from morbid.utils import old_data_exists


class TestSequence(unittest.TestCase):
    pass


def equal_test_genereator(num_1, num_2):
    """
    Check if the desired numbers are equal
    """
    def test(self):
        self.assertEqual(num_1, num_2)
    return test


class TickerTargetPriceNumbersTest(unittest.TestCase):
    """
    Testing tickers

    Making sure, that information from the model database reached the front
    end of the project
    """
    def setUp(self):
        """
        Setting up the environment
        """
        self.aapl_analytics = ticker_analytics(
            ticker='AAPL'
        )

        self.c_analytics = ticker_analytics(
            ticker='C'
        )

        self.f_analytics = ticker_analytics(
            ticker='F'
        )

    def test_aapl(self):
        """
        Testing Apple Inc.
        """
        _ticker = 'AAPL'
        for item in self.aapl_analytics:
            model_target_data = recent_target_data(
                ticker=_ticker,
                analytic=item['analytic']
            )
            production_target_data = TargetPrice.objects.filter(
                ticker__name=_ticker,
                analytic__name=item['analytic']
            ).values('date', 'price')

            if old_data_exists(ticker=_ticker, analytic=item['analytic']):
                test_name = 'test_%s' % '_'.join(item['analytic'].lower().split(' '))
                test = equal_test_genereator(len(production_target_data), len(model_target_data))
                setattr(TestSequence, test_name, test)

    def test_c(self):
        """
        Testing Coca-Cola
        """
        _ticker = 'C'
        for item in self.c_analytics:
            model_target_data = recent_target_data(
                ticker=_ticker,
                analytic=item['analytic']
            )
            production_target_data = TargetPrice.objects.filter(
                ticker__name=_ticker,
                analytic__name=item['analytic']
            ).values('date', 'price')

            if old_data_exists(ticker=_ticker, analytic=item['analytic']):
                test_name = 'test_%s' % '_'.join(item['analytic'].lower().split(' '))
                test = equal_test_genereator(len(production_target_data), len(model_target_data))
                setattr(TestSequence, test_name, test)

    def test_f(self):
        """
        Testing Coca-Cola
        """
        _ticker = 'F'
        for item in self.f_analytics:
            model_target_data = recent_target_data(
                ticker=_ticker,
                analytic=item['analytic']
            )
            production_target_data = TargetPrice.objects.filter(
                ticker__name=_ticker,
                analytic__name=item['analytic']
            ).values('date', 'price')

            if old_data_exists(ticker=_ticker, analytic=item['analytic']):
                test_name = 'test_%s' % '_'.join(item['analytic'].lower().split(' '))
                test = equal_test_genereator(len(production_target_data), len(model_target_data))
                setattr(TestSequence, test_name, test)


class FeaturesCheckTest(unittest.TestCase):
    """
    Testing Feature Checks

    Firstly, the data is calculated with the model (python), then the matlab
    implementation is used, in order to calculate same features again (but not
    all).

    The essence of this test is to make sure, that the results are the same
    from different platforms
    """
    def setUp(self):
        self.features_checks = FeatureAnalyticTickerCheck.objects.all().values_list(
            'feature_analytic_ticker__value',
            'value'
        )

    def test_features(self):
        """
        Testing
        """
        for item in self.features_checks:
            self.assertEqual(item[0], item[1], 'Features are not equal')


class TickerTest(unittest.TestCase):
    """
    Testing ticker model
    """
    def setUp(self):
        pass


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
            name='AAPL',
            long_name='Apple Inc.'
        )

        # Saving everything
        self.goldman.save()
        self.jp.save()
        self.aapl.save()


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

        response = self.client.get('/analytic/rbc-capital-markets/')
        """Testing specific request"""
        self.assertEqual(response.status_code, 200)

    def test_ticker(self):
        """
        Test for the ticker page
        """
        response = self.client.get('/ticker/')
        """Testing general request"""
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/ticker/agn/')
        """Testing specific request"""
        self.assertEqual(response.status_code, 200)
