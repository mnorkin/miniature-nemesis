"""
The Stock_Quete
"""
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

def get_ticker_data(ticker):
  data = []
  url = 'http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=nb3x&e=.csv' % (ticker)
  f = u.urlopen(url, proxies = {})
  rows = f.readlines()
  return rows
  r = rows[0]
  """Get the first entry"""
  r = r[:-2].split(",")
  """Remove the `\r\n` and split by comma"""
  item = {"long_name": r[0],
    "last_stock_price": r[1],
    "stock_exchange": r[2]}

  return item