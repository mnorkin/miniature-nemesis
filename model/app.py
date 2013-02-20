#!/usr/bin/python2
"""
App logic

Then the new target price comes by, filter all the old ones and calculate all the features by standart technique.

TODO:
* Make a trigger for the app to fetch the target price data (this thing needs all the data available from the database on specific stock)
* Pass all the data from the trigger to this app 
* Get the stock data from the yahoo (done)
* Calculate what is needed (done)
* Pass the arguments with the feature identification to the main database (almost done)
"""

import unidecode
import datetime
import stock_quote
import utils
from features import Features
from analytics import Analytics
from tickers import Tickers
from targetprices import TargetPrices
from featureanalytictickers import FeatureAnalyticTickers
import database
import inspect
import rest

def fetch_target_prices():
  """
  Fetching current target prices to the server
  """

  analytics = Analytics()
  tickers = Tickers()

  for target_price in database.get_targetprices():
    date = targetprice['date']
    price = targetprice['date']
    ticker_slug = utils.slugify(targetprice['ticker'])
    analytic_slug = utils.slugify(targetprice['analytic'])

    data = {'date': date,
      'price': price,
      'ticker_slug': ticker_slug,
      'analytic_slug': analytic_slug}

    if rest.send("POST","/api/target_prices/", data):
      """Trying to send POST"""
      if utils.DEBUG:
        print "Target price data sent"
      return True
    else:
      # The fail can be only, then the front-end does not have ticker_slug, analytic_slug, so need to update that information, TODO
      if utils.DEBUG:
        print "Target price data sent fail, trying fixing"

      if analytic.fetch(targetprice['analytic']):
        """Sending analytic data"""
        if utils.DEBUG:
          print "Was missing analytics data, trying to fetch target data again"
        """Repeat the target price fetch data process"""
        self.fetch_target_prices()
      else:
        if utils.DEBUG:
          print "Analytic data was not missing"

      if tickers.fetch(targetprice['ticker']):
        """Sending ticker data"""
        if utils.DEBUG:
          print "Was missing ticker data, trying to fetch target data again"
        """Repeat the target price fetch data process"""
        self.fetch_target_prices()
      else:
        if utils.DEBUG:
          print  "Ticker data was not missing"
      
      return False

def fetch_units():
  """
  Fetching all the units to the server

  TODO:
  * Everything
  """
  features = Features

  for index, unit in enumerate(features.units):
    data = features.units[unit]

    if rest.send("POST","/api/units/", data):
      """Trying to send POST"""
      if utils.DEBUG:
        print "Unit data sent"
    else:
      print "Unit data sent fail"

def fetch_features():
  """
  Fetching all the features to the server
  """
  feature = Features()
  for feature_index, feature_slug in enumerate(feature.features):
    
    data = {'feature_slug': feature_slug,
      'name': feature.features[feature_slug]['name'], 
      'unit_id': feature.features[feature_slug]['unit_id'],
      'display_in_frontpage': feature.features[feature_slug]['display_in_frontpage'],
      'description': ''}

    if rest.send("POST", "/api/features/", data):
      """Trying to send POST"""
      if utils.DEBUG:
        print "Feature data create"
    else:
      if rest.send("PUT", "/api/features/", data):
        """Trying to send PUT"""
        if utils.DEBUG:
          print "Feature data update"
      else:
        # Something wrong on the front-end side
        if utils.DEBUG:
          print "Feature data update fail, nothing to try"

def main():
  """
  Main object 

  First things to do on fresh copy:
  * fetch_units
  * fetch_features

  Logic:
  * Main app is launched with contrab, then another crontab has fetched new target prices
  * Then this appears:
    * Get the target prices
    * Fetch analytic and ticker data, which is in target price list to the front-end
    * Calculate all the features and fetch them to the front-end
    * Finally, fetch the target price data to the front-end
  TODO:
  * Send the feature analytic ticker data
  * Modify API to digest multiple data input 
  """

  analytics = Analytics()
  tickers = Tickers()
  feature_analytic_tickers = FeatureAnalyticTickers()
  targetprices = TargetPrices()

  feature_analytic_ticker_data = []

  for target_price in database.get_targetprices():
    """
    Get the most recent target prices
    """
    date = target_price['date']
    price = target_price['price']
    ticker_slug = utils.slugify(target_price['ticker'])
    analytic_slug = utils.slugify(target_price['analytic'])

    # if not utils.DEBUG:
    analytics.fetch(target_price['analytic'])
    """Fetch analytics data"""
    # if not utils.DEBUG:
    tickers.fetch(target_price['ticker'])
    """Fetch ticker data"""
    target_data = database.get_targetprices(target_price['analytic'], target_price['ticker'])
    """Get all historical data of analytic and ticker relationship"""
    if target_data.__len__() > 1:
      if utils.DEBUG:
        print "Enough data for ", target_price['ticker'], " on ", target_price['analytic']
      """If we have any history data at all"""
      stock_data = stock_quote.get_data(target_price['ticker'])
      """Get stock data of ticker"""
      if stock_data:
        """Check if there is any stock data (happens, then ticker is too old or invalid)"""
        features = Features(target_data, stock_data, False, True)
        """Get all and calculate the defined features"""
        features_values = features.values()
        [ x.update({'ticker_slug': ticker_slug, 'analytic_slug': analytic_slug}) for x in features_values ]

        if not feature_analytic_tickers.send(features_values):
          if utils.DEBUG:
            print "Something went wrong with feature analytic ticker update"

      """After features goes target prices"""
      data = {'date': datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d'),
        'price': price,
        'ticker_slug': ticker_slug,
        'analytic_slug': analytic_slug,
        'change': target_price['change']}

      targetprices.send(data)

    else:
      if utils.DEBUG:
        print "Not enough data for ", target_price['ticker'], " on ", target_price['analytic']
        print "Skipping"


if __name__ == '__main__':
  main()