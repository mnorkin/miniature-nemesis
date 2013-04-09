from database import database
import rest
import utils
from logger import logger


class Targetpricenumbers():

    def __init__(self):
        """
        Target price numbers
        """
        self.database = database()
        self.logger = logger('Targetpricenumbers')

    def collect_and_send(self, analytic=None, ticker=None):
        """
        Collecting and sending target price number information
        """
        if analytic and ticker:
            number_of_tp_data = self.collect(analytic, ticker)
            if number_of_tp_data and self.send(number_of_tp_data):
                self.logger.debug('Target price numbers sent ok')
                return True
            else:
                self.logger.error('Target price numbers sent fail')
                return False
        else:
            return False

    def collect(self, analytic=None, ticker=None):
        if analytic and ticker:
            number_of_tp = self.database.get_number_of_target_prices(
                analytic,
                ticker)
            data = {
                'number': number_of_tp,
                'analytic_slug': utils.slugify(analytic),
                'ticker_slug': utils.slugify(ticker)
            }
            return data

    def send(self, data=None):
        if data:
            if rest.send("POST", "/api/target_price_numbers/", data):
                return True
            else:
                if rest.send("PUT", "/api/target_price_numbers/", data):
                    return True
                else:
                    return False
        else:
            return False
