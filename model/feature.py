from plot import Plot
import datetime

DEBUG = True

class Feature:

  target_data = []
  """Target price data"""
  stock_data = []
  """Stock price data"""
  local_target_data = []
  stock_dates = []
  stock_highs = []
  stock_lows = []
  stock_closes = []
  plot = None

  def __init__(self, target_data, stock_data):
    """
    Initialization of the class
    * Pass the arguments to fetch the target price data
    """
    self.target_data = target_data
    self.stock_data = stock_data

    self.local_target_data = [ [ self.target_data[i]['date'], self.target_data[i]['price'] ] for i in range(0, self.target_data.__len__())]
    self.stock_dates = [self.stock_data[i]['date'] for i in range(0, self.stock_data.__len__())]
    self.stock_highs = [self.stock_data[i]['high'] for i in range(0, self.stock_data.__len__())]
    self.stock_closes = [self.stock_data[i]['close'] for i in range(0, self.stock_data.__len__())]
    self.stock_lows = [self.stock_data[i]['low'] for i in range(0, self.stock_data.__len__())]

    self.plot = Plot()

  def accuracy(self):
    """
    Accuracy measure
    """
    plot = Plot()
    results = []
    
    plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__()) ])

    for target_entry in self.local_target_data:
      measure = 0
      target_date = target_entry[0]
      target_price = target_entry[1]
      start_index = next(i for i, x in enumerate(stock_dates) if x == target_date)
      end_index = start_index+249

      if end_index > self.stock_dates.__len__():
        end_index = self.stock_dates.__len__()-1

      if DEBUG:
        print ( datetime.datetime.fromtimestamp(self.stock_dates[start_index]), 
          datetime.datetime.fromtimestamp(self.stock_dates[end_index]), 
          datetime.datetime.fromtimestamp(self.stock_dates[0]), 
          datetime.datetime.fromtimestamp(self.stock_dates[stock_dates.__len__()-1]) )

      plot.plot_continue([[self.stock_dates[start_index], target_price], [self.stock_dates[end_index], target_price]], 'b')

      for j in range(start_index, end_index):
        if self.stock_highs[j] >= target_price and self.stock_highs[j-1] < target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Stock high %d %d" % (self.stock_highs[j-1], self.stock_highs[j])
          measure = 1
        elif self.stock_lows[j] >= target_price and self.stock_lows[j-1] < target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Low high %d %d" % (self.stock_lows[j-1], self.stock_lows[j])
          measure = 1
        elif stock_highs[j] <= target_price and stock_highs[j-1] > target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Stock high %d %d" % (self.stock_highs[j-1], self.stock_highs[j])
          measure = 1
        elif self.stock_lows[j] <= target_price and self.stock_lows[j-1] > target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Low high %d %d" % (self.stock_lows[j-1], self.stock_lows[j])

          measure = 1

      results.append(float(measure))
      print results

    result = float(sum(results)/self.local_target_data.__len__())
    return round(result,2);

  def closeness(self):
    """
    Closeness measure
    """
    results = []

    self.plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__()) ])

    for index, target_entry in enumerate(self.local_target_data):
      measure = 0
      target_date = target_entry[0]
      target_price = target_entry[1]
      start_index = next(i for i, x in enumerate(self.stock_dates) if x == target_date)
      end_index = start_index+249

      if index < local_target_data.__len__()-1:
        next_start_index = next(i for i, x in enumerate(stock_dates) if x == self.local_target_data[index+1][0])
      else:
        next_start_index = self.stock_dates.__len__()-1

      if end_index > next_start_index:
        end_index = next_start_index

      if DEBUG:
        print "\nStart index: ", start_index, "\nEnd Index: ", end_index, "\nNext start index: ", next_start_index
        print  "\nFrom: ", datetime.datetime.fromtimestamp(self.stock_dates[start_index]), "\nTo: ", datetime.datetime.fromtimestamp(self.stock_dates[end_index]), "\nStock from: ", datetime.datetime.fromtimestamp(self.stock_dates[0]), "\nStock to: ", datetime.datetime.fromtimestamp(self.stock_dates[self.stock_dates.__len__()-1])

      self.plot.plot_continue([[self.stock_dates[start_index], target_price], [self.stock_dates[end_index], target_price]], 'b')

      number_of_entries = range(start_index, end_index).__len__()
      if DEBUG:
        print "\nNumber of entries: ", number_of_entries

      for j in range(start_index, end_index):
        if target_price > self.stock_lows[j] and target_price > self.stock_highs[j]:
          measure = measure + abs(float(stock_highs[j] - target_price))/number_of_entries
        elif target_price < self.stock_lows[j] and target_price < self.stock_highs[j]:
          measure = measure + abs(float(self.stock_lows[j] - target_price))/number_of_entries

      results.append(measure)

      if DEBUG:
        print results

    result = float(sum(results)/self.local_target_data.__len__())
    return round(result, 2)

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
    results = []

    self.plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__()) ])

    for target_entry in self.local_target_data:
      measure = 0
      target_date = target_entry[0]
      target_price = target_entry[1]
      start_index = next(i for i, x in enumerate(self.stock_dates) if x == target_date)
      end_index = start_index+249

      if end_index > self.stock_dates.__len__():
        end_index = self.stock_dates.__len__()-1

      if DEBUG:
        print "\nStart index: ", start_index, "\nEnd Index: ", end_index
        print  "\nFrom: ", datetime.datetime.fromtimestamp(self.stock_dates[start_index]), "\nTo: ", datetime.datetime.fromtimestamp(self.stock_dates[end_index]), "\nStock from: ", datetime.datetime.fromtimestamp(self.stock_dates[0]), "\nStock to: ", datetime.datetime.fromtimestamp(self.stock_dates[self.stock_dates.__len__()-1])

      self.plot.plot_continue([[self.stock_dates[start_index], target_price], [self.stock_dates[end_index], target_price]], 'b')

      start_close_price = self.stock_closes[start_index]
      end_close_price = self.stock_closes[end_index]
      if target_price > start_close_price:
        """
        Long
        """
        measure = (end_close_price - start_close_price)/start_close_price
      elif target_price < start_close_price:
        """
        Short
        """
        measure = (start_close_price - end_close_price)/start_close_price

      results.append(measure)

    result = float(sum(results)/self.local_target_data.__len__())
    return round(result, 2)

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
    results = []

    self.plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__()) ])

    for target_entry in self.local_target_data:
      measure = 0
      target_date = target_entry[0]
      target_price = target_entry[1]
      start_index = next(i for i, x in enumerate(self.stock_dates) if x == target_date)
      end_index = start_index+249

      if end_index > self.stock_dates.__len__():
        end_index = self.stock_dates.__len__()-1

      if DEBUG:
        print ( datetime.datetime.fromtimestamp(self.stock_dates[start_index]), 
          datetime.datetime.fromtimestamp(self.stock_dates[end_index]), 
          datetime.datetime.fromtimestamp(self.stock_dates[0]), 
          datetime.datetime.fromtimestamp(self.stock_dates[self.stock_dates.__len__()-1]) )

      self.plot.plot_continue([[self.stock_dates[start_index], target_price], [self.stock_dates[end_index], target_price]], 'b')

      for j in range(start_index, end_index):
        if self.stock_highs[j] >= target_price and self.stock_highs[j-1] < target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Stock high %d %d" % (self.stock_highs[j-1], self.stock_highs[j])
          measure = j
        elif self.stock_lows[j] >= target_price and self.stock_lows[j-1] < target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Low high %d %d" % (self.stock_lows[j-1], self.stock_lows[j])
          measure = j
        elif self.stock_highs[j] <= target_price and self.stock_highs[j-1] > target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Stock high %d %d" % (self.stock_highs[j-1], self.stock_highs[j])
          measure = j
        elif self.stock_lows[j] <= target_price and self.stock_lows[j-1] > target_price and measure is 0:
          if DEBUG:
            print "Bump"
            print "Target price: %d" % target_price
            print "Low high %d %d" % (self.stock_lows[j-1], self.stock_lows[j])

          measure = j

      results.append(float(measure))
      print results

    result = float(sum(results)/self.local_target_data.__len__())
    return round(result,2);
