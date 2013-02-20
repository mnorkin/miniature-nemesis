"""
The Target Prices
"""

import rest
import utils

class TargetPrices:

  def send(self,data=None):

    if data:

      if rest.send("POST","/api/target_prices/", data):
        """Trying to send POST"""
        if utils.DEBUG:
          print "Target price data sent"
        return True
      else:
        if rest.send("PUT", "/api/target_prices/", data):
          if utils.DEBUG:
            print "Target Price data update"
          return True
        else:
          if utils.DEBUG:
            print "Target price data sent fail"
          return False
    else:
      return False