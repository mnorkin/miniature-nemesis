from database import database
import rest
import utils
from logger import logger


class Volatilities():
    """
    Volatility calculations
    """
    def __init__(self):
        self.database = database()
        self.logger = logger('Volatilities')

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
                self.logger.debug('Volatility data send')
                return True
            else:
                self.logger.error('Volatility data fail')
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
