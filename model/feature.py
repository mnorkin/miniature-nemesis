from plot import Plot
import datetime

DEBUG = True

class Feature:

  target_data = []
  """Target price data"""
  stock_data = []
  """Stock price data"""

  def __init__(self, target_data, stock_data):
    """
    Initialization of the class
    * Pass the arguments to fetch the target price data
    """
    self.target_data = target_data
    self.stock_data = stock_data

    

  def accuracy(self):
    """
    Accuracy measure
    """

    plot = Plot()

    results = []
    
    local_target_data = [ [ self.target_data[i]['date'], self.target_data[i]['price'] ] for i in range(0, self.target_data.__len__()) ]
    stock_dates = [ self.stock_data[i]['date'] for i in range(0, self.stock_data.__len__()) ]
    stock_highs = [ self.stock_data[i]['high'] for i in range(0, self.stock_data.__len__()) ]
    stock_lows = [ self.stock_data[i]['low'] for i in range(0, self.stock_data.__len__()) ]

    plot.plot_continue( [ [ self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__()) ] )

    print self.target_data.__len__()

    for target_entry in local_target_data:
      measure = 0
      target_date = target_entry[0]
      target_price = target_entry[1]
      start_index = next( i for i, x in enumerate(stock_dates) if x == target_date )
      end_index = start_index+249

      if end_index > stock_dates.__len__():
        end_index = stock_dates.__len__()-1

      if DEBUG:
        print ( datetime.datetime.fromtimestamp(stock_dates[start_index]), 
          datetime.datetime.fromtimestamp(stock_dates[end_index]), 
          datetime.datetime.fromtimestamp(stock_dates[0]), 
          datetime.datetime.fromtimestamp(stock_dates[stock_dates.__len__()-1]) )

      plot.plot_continue([[stock_dates[start_index], target_price], [stock_dates[end_index], target_price]], 'b')

      for j in range(start_index, end_index):
        if stock_highs[j] >= target_price and stock_highs[j-1] < target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Stock high %d %d" % (stock_highs[j-1], stock_highs[j])
          measure = 1
        elif stock_lows[j] >= target_price and stock_lows[j-1] < target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Low high %d %d" % (stock_lows[j-1], stock_lows[j])
          measure = 1
        elif stock_highs[j] <= target_price and stock_highs[j-1] > target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Stock high %d %d" % (stock_highs[j-1], stock_highs[j])
          measure = 1
        elif stock_lows[j] <= target_price and stock_lows[j-1] > target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Low high %d %d" % (stock_lows[j-1], stock_lows[j])

          measure = 1

      results.append(float(measure))
      print results

    result = float(sum(results)/local_target_data.__len__())
    return round(result,2);

  def closeness(self):
    """
    Closeness measure
    """
    measure = 0

    return measure

  def difference(self):
    """
    Difference measure
    """
    measure = 0

    return measure

  def profitability(self):
    """
    Profitability measure
    """
    measure = 0

    return measure

  def max_profitability(self):
    """
    Maximum profitability measure
    """
    measure = 0

    return measure

  def impact_to_market(self):
    """
    Impart to the market measure
    """
    measure = 0

    return measure

  def reach_time(self):
    """
    Reach time measure
    """
    measure = 0

    return measure