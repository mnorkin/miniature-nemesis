"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

The test manager, just to be on the safe side of the road
"""

from django.test import TestCase


# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

class ModelTest(TestCase):
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

class UrlTest(TestCase):
  """
  Url tester
  """

  def test_index(self):
    """
    Test for the index page
    """
    pass

  def test_analytic(self):
    """
    Test for the analytic page
    """
    pass

  def test_ticker(self):
    """
    Test for the ticker page
    """
    pass