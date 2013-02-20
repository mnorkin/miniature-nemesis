"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

The test manager, just to be on the safe side of the road
"""

from django.utils import unittest
from django.test.client import Client

class ModelTest(unittest.TestCase):
  """
  Model test
  """
  def test_unit_fields(self):
    """
    Test for the unit fields
    """
    pass

  def test_feature_fields(self):
    """
    Test for the unit fields
    """
    pass

  def test_ticker_fields(self):
    """
    Test for the ticker fields
    """
    pass

  def test_analytic_fields(self):
    """
    Test for the analytic fields
    """
    pass

  def test_featureanalyticticker_fields(self):
    """
    Test for the feature analytic ticker fields
    """
    pass

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
    