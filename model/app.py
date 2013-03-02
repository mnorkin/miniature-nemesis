#!/usr/bin/python2
"""
Main application
"""

import datetime
import stock_quote
import utils
from features import Features
from analytics import Analytics
from tickers import Tickers
from targetprices import TargetPrices
from featureanalytictickers import FeatureAnalyticTickers
import database
import rest


def fetch_units():
    """
    Fetching all the units to the server

    TODO:
    * Everything
    """
    features = Features

    for index, unit in enumerate(features.units):
        data = features.units[unit]

        if rest.send("POST", "/api/units/", data):
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

        data = {
            'feature_slug': feature_slug,
            'name': feature.features[feature_slug]['name'],
            'unit_id': feature.features[feature_slug]['unit_id'],
            'display_in_frontpage': feature.features[feature_slug]['display_in_frontpage'],
            'description': ''
        }

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

    for target_price in database.get_targetprices():
        """
        Get the most recent target prices
        """
        date = target_price['date']
        price = target_price['price']
        ticker_slug = utils.slugify(target_price['ticker'])
        analytic_slug = utils.slugify(target_price['analytic'])

        analytics.fetch(target_price['analytic'])
        """Fetch analytics data"""
        tickers.fetch(target_price['ticker'])
        """Fetch ticker data"""
        target_data = database.get_targetprices(target_price['analytic'], target_price['ticker'])
        """Get all historical data of analytic and ticker relationship"""
        if target_data.__len__() > 1:
            if utils.DEBUG:
                print "Enough data for ", target_price['ticker'], " on ", target_price['analytic']
            """If we have any history data at all"""
            stock_data = stock_quote.get_data(target_price['ticker'])
            beta = stock_quote.get_beta(target_price['ticker'])
            """Get stock data of ticker"""
            if stock_data and beta:
                """Check if there is any stock data (happens, then ticker is too old or invalid)"""
                features = Features(target_data, stock_data, beta, False, True)
                """Get all and calculate the defined features"""
                features_values = features.values()
                [foo.update({'ticker_slug': ticker_slug, 'analytic_slug': analytic_slug}) for foo in features_values]

                if features_values:
                    if not feature_analytic_tickers.send(features_values):
                        if utils.DEBUG:
                            print "Something went wrong with feature analytic ticker update"

                """Do not send any target price data, unless there is stock data"""
                """After features goes target prices"""
                data = {
                    'date': datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d'),
                    'price': price,
                    'ticker_slug': ticker_slug,
                    'analytic_slug': analytic_slug,
                    'change': target_price['change']
                }

                targetprices.send(data)

        else:
            if utils.DEBUG:
                print "Not enough data for ", target_price['ticker'], " on ", target_price['analytic']
                print "Skipping"


if __name__ == '__main__':
    main()
