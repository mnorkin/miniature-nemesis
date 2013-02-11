import urllib as u
import string
import datetime, time

def get_data(ticker):
  data = []
  url = 'http://ichart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&ignore=.csv' % (ticker, 0, 1, 2006)
  f = u.urlopen(url,proxies = {})
  rows = f.readlines()
  for r in rows[1:]:
    values = r.split(',')
    stock_date = time.mktime(datetime.datetime.strptime(values[0], '%Y-%m-%d').timetuple())
    stock_open = float(values[1])
    stock_high = float(values[2])
    stock_low = float(values[3])
    stock_close = float(values[4])
    item = {'date' : stock_date, 
      'open' : stock_open, 
      'high' : stock_high, 
      'low' : stock_low, 
      'close' : stock_close};
    data.append(item)
  data.reverse()
  return data