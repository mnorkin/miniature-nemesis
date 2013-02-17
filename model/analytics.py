import database
import rest
import utils

class Analytics:
  """
  Analytic object
  """

  def fetch(analytic=None):
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

      
  def collect(analytic=None):
    """
    Method to collect analytic data
    """
    if analytic:
      analytic_data = database.get_analytics(analytic)
      number_of_companies = 0
      number_of_tp = 0
      last_target_price = 0
      volatility = 0 # TODO
      slug = utils.slugify(str(analytic))
      for ticker in database.get_tickers(analytic):
        # Get all the tickers
        number_of_companies = number_of_companies + 1
        for targetprice in database.get_targetprices(analytic, ticker):
          number_of_tp = number_of_tp + 1

          if last_target_price == 0:
            last_target_price = targetprice['price']

      data = {'name': analytic, 
        'number_of_companies': number_of_companies, 
        'number_of_tp': number_of_tp,
        'last_target_price': last_target_price,
        'volatility': volatility,
        'slug': slug}

      return data
    else:
      return None

  def send(data=None):
    """
    Method to send analytic data
    """

    if data:
      if rest.send("POST","/api/analytics/", data):
        """Trying to send POST"""
        if utils.DEBUG:
          print "Analytic data create"
        return True
      else:
        if rest.send("PUT","/api/analytics/", data):
          """Trying to send PUT"""
          if utils.DEBUG:
            print "Analytic data update"
          return True
        else:
          # Literally, something should be wrong on front-end side, if this does not work
          if utils.DEBUG:
            print "Analytic data update fail, nothing else to try"
          return False
    else:
      return False
