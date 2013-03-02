"""
The Feature Analytic Tickers
"""

import rest
import utils


class FeatureAnalyticTickers:

    def send(self, big_data=None):
        """
        Method to send feature Analytic ticker data
        """

        all_data_sent = True

        if big_data:

            for data in big_data:
                if rest.send("POST", "/api/feature_analytic_tickers/", data):
                    """Trying to send POST"""
                    if utils.DEBUG:
                        print "FeatureAnalyticTicker data create"
                else:
                    if rest.send("PUT", "/api/feature_analytic_tickers/", data):
                        """Trying to send PUT"""
                        if utils.DEBUG:
                            print "FeatureAnalyticTicker data update"
                    else:
                        all_data_sent = False
                        # Literally, something should be wrong on front-end side, if this does not work
                        # Although at this point can be lack of unit definition, make a unit update and try again
                        if utils.DEBUG:
                            print "FeatureAnalyticTicker data update fail, nothing else to try"

            return all_data_sent
        else:
            return False
