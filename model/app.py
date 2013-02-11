#!/usr/bin/python2
"""
App logic

Then the new target price comes by, filter all the old ones and calculate all the features by standart technique.

TODO:
* Make a trigger for the app to fetch the target price data (this thing needs all the data available from the database on specific stock)
* Pass all the data from the trigger to this app
* Get the stock data from the google (nearly done)
* Calculate what is needed
* Pass the arguments with the feature identification to the main database
"""

import MySQLdb
import re
import unidecode
import datetime, time
import stock_quote
from feature import *
import httplib

# CONFIG
DEBUG = True

def slugify(str):
  """
  Slugify the string
  """
  str = unidecode.unidecode(str).lower()
  str = re.sub(r'\W+', '-', str)

  # Just to be on the safe side
  if str[str.__len__()-1] == '-':
    str = str[:-1]

  return str

def connect_to_mysql():
  """
  Connecting to the database
  """

  db = MySQLdb.connect(host="localhost",
    user="root",
    passwd="classic",
    db="morbid")

  return db.cursor()

def get_all_analytics():
  """
  Returns the list of analytics
  """
  cur = connect_to_mysql()
  # Collect all the analytics
  if not DEBUG:
    cur.execute("SELECT DISTINCT(`analytic`) FROM `entries`")
  else:
    cur.execute("SELECT DISTINCT(`analytic`) FROM `entries` LIMIT 1")

  results = []

  for row in cur.fetchall():
    results.append(row[0])

  return results

def get_tickers(analytic):
  """
  Method to get the tickers, which belongs to analytic
  """
  cur = connect_to_mysql()

  results = []
  if not DEBUG:
    cur.execute("SELECT DISTINCT(`ticket`) FROM `entries` WHERE `analytic`='%s'" % re.escape(analytic))
  else:
    # cur.execute("SELECT DISTINCT(`ticket`) FROM `entries` WHERE `analytic`='%s' LIMIT 1,5" % re.escape(analytic))
    cur.execute("SELECT DISTINCT(`ticket`) FROM `entries` WHERE `analytic`='%s' LIMIT 1,10" % re.escape(analytic))

  for row in cur.fetchall():
    results.append(row[0])

  return results


def get_targetprices(analytic, ticker):
  """
  Method to return the target prices
  """
  cur = connect_to_mysql()
  results = []
  query = "SELECT `date`, `price0`, `price1` FROM `entries` WHERE `analytic`='%s' AND `ticket`='%s' ORDER BY `date`" % (re.escape(analytic), re.escape(ticker))

  cur.execute(query)

  for row in cur.fetchall():
    if row[1] != 0 or row[2] != 0:
      # Checking the price variation (updated price or old)
      if row[2] == 0:
        price = row[1]
      else:
        price = row[2]
      item = {'date': time.mktime(row[0].timetuple()), 'price': price}
      """Forming the dict"""
      if item not in results:
        """Escaping possible duplicates"""
        results.append(item)

  return results

def form_request():
  conn = httplib.HTTPConnection("127.0.0.1:8000")
  conn.request("GET", "/feature_write")

def main():
  """
  Main thread
  """
  cur = connect_to_mysql()
  
  for analytic in get_all_analytics():
    for ticker in get_tickers(analytic):
      target_data = get_targetprices(analytic, ticker)
      stock_data = stock_quote.get_data(ticker)
      if target_data.__len__() > 1:
        feature = Feature(target_data, stock_data)
        print feature.profitability()
      else:
        if DEBUG:
          print 'Not enough target price data for %s ticker' % ticker

if __name__ == '__main__':
  main()