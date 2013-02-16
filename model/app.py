#!/usr/bin/python2
"""
App logic

Then the new target price comes by, filter all the old ones and calculate all the features by standart technique.

TODO:
* Make a trigger for the app to fetch the target price data (this thing needs all the data available from the database on specific stock)
* Pass all the data from the trigger to this app
* Get the stock data from the google (nearly done)
* Calculate what is needed
* Pass the arguments with the feature identification to the main database
"""

import unidecode
import stock_quote
import utils
from features import *
from analytics import *
from tickers import *
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

def fetch_features():
  """
  Fetching all the features to the server
  """
  feature = Feature()
  for feature_index, feature_slug in enumerate(feature.features):
    feature_id = feature.features[feature_slug]['id']
    feature_name = feature.features[feature_slug]['name']
    feature_unit_id = feature.features[feature_slug]['unit']
    
    data = {'name': feature.features[feature_slug]['name'], 
      'unit_id': feature.features[feature_slug]['unit'],
      'display_in_frontpage': feature.features[feature_slug]['display_in_frontpage'],
      'description': ''}

    if rest.send("POST", "/api/features/", data):
      """Trying to send POST"""
      if utils.DEBUG:
        print "Feature data create"
      return True
    else:
      if rest.send("PUT", "/api/features/", data):
        """Trying to send PUT"""
        if utils.DEBUG:
          print "Feature data update"
        return True
      else:
        # Something wrong on the front-end side
        if utils.DEBUG:
          print "Feature data update fail, nothing to try"
        return False
      
def fetch_featureanalytictickers():
  """
  Fetching the features to the server, which has the target prices

  * A big TODO
  """

  for targetprice in database.get_targetprices():
    """Get this date target prices"""
    target_data = database.get_targetprices(targetprice['analytic'], targetprice['ticker'])
    """Get all the target prices in before the current target price"""
    if target_data.__len__() > 1:
      """Check if there is any data"""
      stock_data = stock_quote.get_data(targetprice['ticker'])
      """Catch all the stocks"""
      features = Features(target_data, stock_data)
      """Calculate the features"""
      for feature_method in inspect.getmembers(features, predicate=inspect.ismethod):
        print feature_method[0]
        # eval('feature.' + feature_method[0])


  # for analytic in get_analytics():
  #   for ticker in get_tickers(analytic):
  #     target_date = get_targetprices(analytic, ticker)
  #     stock_data = stock_quote.get_data(ticker)
  #     if target_data.__len__() > 1:
  #       feature = Feature(target_data, stock_data)
  #     else:
  #       if DEBUG:
  #         print 'Not enough target price data for %s ticker' % ticker

def main():
  """
  Main object 

  Logic:
  * Main app is launched, then the crontab has fetched new target prices
  * Then this appears:
    * Get the target prices
    * Fetch analytic and ticker data, which is in target price list to the front-end
    * Calculate all the features and fetch them to the front-end
    * Finally, fetch the target price data to the front-end
  """

if __name__ == '__main__':
  main()