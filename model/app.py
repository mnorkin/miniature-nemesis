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
from volatilities import Volatilities
from targetpricenumbers import Targetpricenumbers
from featureanalytictickers import FeatureAnalyticTickers
from database import database
import rest
from logger import logger
import time
import settings
import os
import json


class App():
    """
    The almighty app
    """

    def __init__(self):
        """
        Initialization of the class
        """
        self.logger = logger('app')

        self.database = database()
        self.stock_quote = stock_quote()

        self.logger.debug('Starting up...')

    def fetch_units(self):
        """
        Fetching all the units to the server
        """
        features = Features

        for index, unit in enumerate(features.units):
            data = features.units[unit]

            if rest.send("POST", "/api/units/", data):
                self.logger.debug('Unit data sent')
            else:
                self.logger.debug('Unit data sent fail')

    def check_stock_database(self):
        """
        Checking stock database in order to get the right format of data

        Right format of data:
        * Increasing date, e.g. from 2001 to 2013 not over wise (this is important)
        """
        self.logger.debug('Start checking stock database')
        data_dir = settings.data_dir

        for stock_data_file in os.listdir(data_dir):
            if stock_data_file != "." and stock_data_file != "..":
                f = open(data_dir + '/' + stock_data_file, 'r')
                try:
                    data = json.loads(f.read())
                except ValueError:
                    data = []

                if type(data) is list and len(data) > 1:
                    # Check if first entry is the biggest entry
                    if data[0]['date'] > data[-1]['date']:
                        self.logger.debug('%s ticker data incorrect' % (
                            stock_data_file.split('.')[0]))
                        ff = open('%s/%s' % (data_dir, stock_data_file), 'w')
                        data.reverse()
                        ff.write(json.dumps(data))

        self.logger.debug('Stock database check finished')

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
                self.logger.debug('Feature data create')
            else:
                if rest.send("PUT", "/api/features/", data):
                    self.logger.debug('Feature data update')
                else:
                    self.logger.error('Feature date update fail')

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
        """

        # self.check_stock_database()

        analytics = Analytics()
        tickers = Tickers()
        feature_analytic_tickers = FeatureAnalyticTickers()
        targetprices = TargetPrices()
        targetpricenumbers = Targetpricenumbers()
        volatilities = Volatilities()

        self.logger.debug('Getting the target prices')

        for target_price in self.database.get_targetprices():
            """
            Get the most recent target prices
            """
            self.logger.debug('Target price %s of %s' % (
                target_price['ticker'], target_price['analytic']))
            ticker_slug = utils.slugify(target_price['ticker'])
            analytic_slug = utils.slugify(target_price['analytic'])

            # Check with server if current calculations are required

            target_data = self.database.return_targetprices(
                target_price['analytic'],
                target_price['ticker']
            )
            if target_data:
                # Only then the data is available -- upload the analytic and
                # ticker data to the server
                analytics.collect_and_send(target_price['analytic'])
                tickers.collect_and_send(target_price['ticker'])
                self.logger.debug(
                    "Enough data for %s ticker, analytic %s" %
                    (target_price['ticker'], target_price['analytic'])
                )
                # Sending volatility measure
                volatilities.collect_and_send(
                    analytic=target_price['analytic'],
                    ticker=target_price['ticker'])
                # Sending target price numbers data
                targetpricenumbers.collect_and_send(
                    analytic=target_price['analytic'],
                    ticker=target_price['ticker'])
                # Getting stock data
                stock_data = self.stock_quote.get_data(target_price['ticker'])
                # Receive the beta
                beta = self.stock_quote.get_beta(target_price['ticker'])
                # Check if stock and beta are okay
                if stock_data and beta:
                    self.logger.debug('Stock data and beta values are okay')

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
                            self.logger.error('Something went wrong with feature analytic ticker update')

                    self.logger.debug("Date %s " % target_price['date'])
                    target_price_date_timestamp = date.fromtimestamp(target_price['date']).timetuple()

                    matches = (x for x in stock_data if x['date'] == time.mktime(target_price_date_timestamp))

                    try:
                        stock_entry = matches.next()
                        target_price['change'] = float((target_price['price'] - stock_entry['close'])/stock_entry['close'])
                        target_price['change'] = target_price['change'] * 100
                        self.logger.debug('Stock entry close price %s' % stock_entry['close'])
                        self.logger.debug('Target price %s' % target_price['price'])
                        self.logger.debug('Change %s' % target_price['change'])
                    except StopIteration:
                        self.logger.debug('Date %s' % target_price['date'])
                        self.logger.debug('Ticker %s' % ticker_slug)
                        self.logger.error('No target price stock date found')
                        target_price['change'] = 0

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

                    # Submitting results to the server
                    # There are entries in the server about the ticker
                    # and analytic, so no problems will appear
                    rest.send(
                        'PUT',
                        '/api/target_price_analytic_ticker/',
                        {
                            'analytic': target_price['analytic'],
                            'ticker': target_price['ticker'],
                            'date': target_price['date_human']
                        })

                else:
                    self.logger.debug('Stock data and beta fail')
                    self.logger.debug('Beta %s' % beta)

            else:
                self.logger.debug(
                    "Not enought data for %s on %s, skipping" %
                    (target_price['ticker'], target_price['analytic'])
                )


if __name__ == '__main__':
    app = App()
    app.fetch_units()
    app.fetch_features()
    app.main()
