import utils
from database import database
import rest
from stock_quote import stock_quote
from logger import logger


class Tickers:
    """
    Ticker object
    """

    def __init__(self):
        self.database = database()
        self.stock_quote = stock_quote()
        self.logger = logger('tickers')

    def collect_and_send(self, ticker=None):
        """
        Fetching ticker information to the server
        """
        if not ticker:
            for ticker in self.database.get_all_tickers():
                ticker_data = self.collect(ticker)
                if ticker_data and not self.send(ticker_data):
                    return False
            return True
        else:
            ticker_data = self.collect(ticker)
            if ticker_data and self.send(ticker_data):
                return True
            else:
                return False

    def collect(self, ticker=None):
        """
        Collecting ticker data
        """
        if ticker:
            ticker_consensus = self.database.get_consensus(ticker)
            # ticker_yahoo = self.stock_quote.get_ticker_data(ticker)
            name = ticker
            long_name = ''
            # long_name = ticker_yahoo['long_name']
            # last_stock_price = ticker_yahoo['last_stock_price']
            last_stock_price = 0
            consensus_min = ticker_consensus['min']
            consensus_avg = ticker_consensus['avg']
            consensus_max = ticker_consensus['max']
            slug = utils.slugify(ticker)

            data = {
                'name': name,
                'long_name': long_name.replace('"', ''),
                'last_stock_price': last_stock_price,
                'consensus_min': consensus_min,
                'consensus_avg': consensus_avg,
                'consensus_max': consensus_max,
                'display': 0,
                'slug': slug
            }
            return data
        else:
            return None

    def send(self, data=None):
        """
        Sending data to the API
        """

        if data:
            if rest.send("POST", "/api/tickers/", data):
                """Trying to send POST"""
                self.logger.debug("Ticker data create")
                return True
            else:
                if rest.send("PUT", "/api/tickers/", data):
                    """Trying to send PUT"""
                    self.logger.debug("Ticker data update")
                    return True
                else:
                    # Literally, something would be wrong on the front-end side, if this does not work
                    self.logger.error("Ticker data update fail, nothing else to try")
                    return False
        else:
            return False
