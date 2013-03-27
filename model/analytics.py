import database
import rest
import utils


class Analytics:
    """
    Analytic object
    """

    def collect_and_send(self, analytic=None):
        """
        Fetching analytics data to the server

        If analytic is defined -- sending the data of specific analytic
        """

        if not analytic:
            for analytic in database.get_analytics():
                analytic_data = self.collect(analytic)
                if analytic_data and not self.send(analytic_data):
                    return False
                """If there was error at any step -- return"""
            return True
            """If everything was ok -- return true"""
        else:
            """
            Get specific analytic data and parse it to the front-end
            """
            analytic_data = self.collect(analytic)
            if analytic_data and self.send(analytic_data):
                return True
                """If everything was okay -- return true"""
            else:
                return False
                """If something went wrong -- return false"""

    def collect(self, analytic=None):
        """
        Method to collect analytic data
        """
        if analytic:
            analytic_stats = database.get_analytic(analytic)
            analytic_data = database.get_analytics(analytic)
            number_of_companies = analytic_stats['number_of_companies']
            try:
                number_of_tp = analytic_data['number_of_tp']
            except TypeError:
                number_of_tp = 0
            last_target_price = analytic_stats['last_target_price']
            volatility_positive = analytic_stats['volatility_positive']
            volatility_negative = analytic_stats['volatility_negative']
            slug = utils.slugify(str(analytic))

            for ticker in database.get_tickers(analytic):
                # Get all the tickers
                number_of_companies = number_of_companies + 1
                for targetprice in database.get_targetprices(analytic, ticker):
                    number_of_tp = number_of_tp + 1

                    if last_target_price == 0:
                        last_target_price = targetprice['price']

            data = {
                'name': analytic.replace('"', ''),
                'number_of_companies': number_of_companies,
                'number_of_tp': number_of_tp,
                'last_target_price': last_target_price,
                'volatility_positive': volatility_positive,
                'volatility_negative': volatility_negative,
                'slug': slug
            }

            return data
        else:
            return None

    def send(self, data=None):
        """
        Method to send analytic data
        """

        if data:
            if rest.send("POST", "/api/analytics/", data):
                return True
            else:
                if rest.send("PUT", "/api/analytics/", data):
                    return True
                else:
                    # Literally, something should be wrong on front-end side,
                    # if this does not work
                    return False
        else:
            return False
