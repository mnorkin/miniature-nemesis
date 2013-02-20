import utils
import database
import rest
import stock_quote

class Tickers:
  """
  Ticker object
  """

  def fetch(self,ticker=None):
    """
    Fetching ticker information to the server
    """
    if not ticker:
      for ticker in database.get_all_tickers():
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
      ticker_yahoo = stock_quote.get_ticker_data(ticker)
      name = ticker
      long_name = ticker_yahoo['long_name']
      last_stock_price = ticker_yahoo['last_stock_price']
      number_of_analytics = database.get_analytics(ticker).__len__()
      number_of_tp = database.get_tickers(ticker).__len__()
      consensus_min = 0 # TODO
      consensus_avg = 0 # TODO
      consensus_max = 0 # TODO
      slug = utils.slugify(ticker)

      data = {'name': name,
        'long_name': long_name,
        'last_stock_price': last_stock_price,
        'number_of_analytics': number_of_analytics,
        'number_of_tp': number_of_tp,
        'consensus_min': consensus_min,
        'consensus_avg': consensus_avg,
        'consensus_max': consensus_max,
        'slug': slug}
      return data
    else:
      return None

  def send(self, data=None):
    """
    Sending data to the API
    """
    
    if data:
      if rest.send("POST","/api/tickers/", data):
        """Trying to send POST"""
        if utils.DEBUG:
          print "Ticker data create"
        return True
      else:
        if rest.send("PUT","/api/tickers/", data):
          """Trying to send PUT"""
          if utils.DEBUG:
            print "Ticker data update"
          return True
        else:
          # Literally, something would be wrong on the front-end side, if this does not work
          if utils.DEBUG:
            print "Ticker data update fail, nothing else to try"
          return False
    else:
      return False