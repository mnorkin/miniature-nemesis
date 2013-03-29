#!/usr/bin/python2
"""
Main application
"""

import datetime
from datetime import date
from stock_quote import stock_quote
import utils
from features import Features
from analytics import Analytics
from tickers import Tickers
from targetprices import TargetPrices
from featureanalytictickers import FeatureAnalyticTickers
from database import database
import rest
import logging
import os


class App():
    """
    The almighty app
    """

    def __init__(self):
        """
        Initialization of the class
        """
        self.absolute_path = os.path.dirname(os.path.realpath(__file__))
        self.logging_file = self.absolute_path + '/logs/' + date.today().isoformat() + '.log'
        self.logging_level = logging.DEBUG
        logging.basicConfig(
            filename=self.logging_file,
            level=self.logging_level, format='%(asctime)s %(message)s')

        self.database = database()
        self.stock_quote

        logging.debug('Starting up...')

    def fetch_units(self):
        """
        Fetching all the units to the server
        """
        features = Features

        for index, unit in enumerate(features.units):
            data = features.units[unit]

            if rest.send("POST", "/api/units/", data):
                logging.debug('Unit data sent')
            else:
                logging.debug('Unit data sent fail')

    def fetch_features(self):
        """
        Fetching all the features to the server
        """
        feature = Features()
        for feature_slug in feature.features:

            data = {
                'feature_slug': feature_slug,
                'name': feature.features[feature_slug]['name'],
                'unit_id': feature.features[feature_slug]['unit_id'],
                'position': feature.features[feature_slug]['position'],
                'display_in_frontpage':
                feature.features[feature_slug]['display_in_frontpage'],
                'description': ''
            }

            if rest.send("POST", "/api/features/", data):
                logging.debug('Feature data create')
            else:
                if rest.send("PUT", "/api/features/", data):
                    logging.debug('Feature data update')
                else:
                    logging.error('Feature date update fail')

    def main(self):
        """
        Main object

        First things to do on fresh copy:
        * fetch_units
        * fetch_features

        Logic:
        * Main app is launched with contrab, then another crontab has fetched
        new target prices
        * Then this appears:
            * Get the target prices
            * Fetch analytic and ticker data, which is in target price list to
            the front-end
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

        logging.debug('Getting the target prices')

        for target_price in self.database.get_targetprices():
            """
            Get the most recent target prices
            """
            logging.debug('Target price %s of %s' % (
                target_price['ticker'], target_price['analytic']))
            ticker_slug = utils.slugify(target_price['ticker'])
            analytic_slug = utils.slugify(target_price['analytic'])

            analytics.collect_and_send(target_price['analytic'])
            tickers.collect_and_send(target_price['ticker'])

            target_data = self.database.return_targetprices(
                target_price['analytic'],
                target_price['ticker']
            )
            if target_data.__len__() > 1:
                logging.debug(
                    "Enough data for %s ticker, analytic %s" %
                    (target_price['ticker'], target_price['analytic'])
                )
                stock_data = self.stock_quote.get_data(target_price['ticker'])
                beta = self.stock_quote.get_beta(target_price['ticker'])
                if stock_data and beta:

                    features = Features(
                        target_data=target_data,
                        stock_data=stock_data,
                        beta=beta,
                        plot=False,
                        calculate=True
                    )
                    features_values = features.values()
                    [foo.update({
                        'ticker_slug': ticker_slug,
                        'analytic_slug': analytic_slug})
                        for foo in features_values]

                    if features_values:
                        if not feature_analytic_tickers.send(features_values):
                            logging.error('Something went wrong with feature\
analytic ticker update')
                    _date = datetime.datetime.fromtimestamp(
                        target_price['date']
                    )
                    data = {
                        'date': _date.strftime('%Y-%m-%d'),
                        'price': target_price['price'],
                        'ticker_slug': ticker_slug,
                        'analytic_slug': analytic_slug,
                        'change': target_price['change']
                    }

                    targetprices.send(data)

            else:
                logging.debug(
                    "Not enought data for %s on %s, skipping" %
                    (target_price['ticker'], target_price['analytic'])
                )


if __name__ == '__main__':
    app = App()
    app.fetch_units()
    app.fetch_features()
    app.main()
