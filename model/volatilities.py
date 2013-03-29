from database import database
import rest
import utils
import os
import logging
from datetime import date


class volatilities():
    """
    Volatility calculations
    """
    def __init__(self, arg):
        super(volatilities, self).__init__()
        self.database = database()
        self.absolute_path = os.path.dirname(os.path.realpath(__file__))
        self.logging_file = self.absolute_path + '/logs/' + date.today().isoformat() + '.log'
        self.logging_level = logging.DEBUG
        logging.basicConfig(
            filename=self.logging_file,
            level=self.logging_level, format='%(asctime)s %(message)s')

    def collect_and_send(self, analytic=None, ticker=None):
        """
        Making collection and sending happen
        """
        if analytic and ticker:
            volatility_data = self.collect(analytic, ticker)
            item = {
                'analytic_slug': utils.slugify(analytic),
                'ticker_slug': utils.slugify(ticker),
                'number': volatility_data['number'],
                'total': volatility_data['total']
            }
            if item and self.send(item):
                logging.debug('Volatility data send')
                return True
            else:
                logging.error('Volatility data fail')
                return False
        else:
            return False

    def collect(self, analytic=None, ticker=None):
        """
        Making collection happen
        """
        if analytic and ticker:
            return self.database.get_volatility(analytic, ticker)
        else:
            return None

    def send(self, data=None):
        """
        Making send happen
        """
        if data:
            if rest.send("POST", "/api/volatility/", data):
                return True
            else:
                if rest.send("PUT", "/api/volatility/", data):
                    return True
                else:
                    return False
        else:
            return False
