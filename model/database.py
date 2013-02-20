"""
The Database 
"""
import MySQLdb
import re
import datetime, time
import utils

def connect_to_mysql():
  """
  Connecting to the database
  """

  db = MySQLdb.connect(host="localhost",
    user="root",
    passwd="classic",
    db="morbid")

  return db.cursor()

def get_analytics(ticker=None):
  """
  Returns the list of analytics
  """
  cur = connect_to_mysql()
  # Collect all the analytics

  if not utils.DEBUG:
    if not ticker:
      cur.execute("SELECT DISTINCT(`analytic`) FROM `entries`")
    else:
      cur.execute("SELECT DISTINCT(`analytic`) FROM `entries` WHERE `ticket`='%s'" % re.escape(ticker))
  else:
    if not ticker:
      cur.execute("SELECT DISTINCT(`analytic`) FROM `entries` LIMIT 5,1")
    else:
      cur.execute("SELECT DISTINCT(`analytic`) FROM `entries` WHERE `ticket`='%s' LIMIT 5,1" % re.escape(ticker))

  results = []

  for row in cur.fetchall():
    results.append(row[0])

  return results

def get_tickers(analytic=None):
  """
  Method to get the tickers, which belongs to analytic
  """
  cur = connect_to_mysql()

  results = []
  if not utils.DEBUG:
    if not analytic:
      cur.execute("SELECT DISTINCT(`ticket`) FROM `entries`")
      """Fetch all existing tickers from the database"""
    else:
      cur.execute("SELECT DISTINCT(`ticket`) FROM `entries` WHERE `analytic`='%s'" % re.escape(analytic))
      """Fetch tickers which analytic works with from the database"""
  else:
    if not analytic:
      cur.execute("SELECT DISTINCT(`ticket`) FROM `entries` LIMIT 1,10")
    else:
      cur.execute("SELECT DISTINCT(`ticket`) FROM `entries` WHERE `analytic`='%s' LIMIT 1,10" % re.escape(analytic))

  for row in cur.fetchall():
    results.append(row[0])

  return results

def get_previous_targetprice(analytic=None, ticker=None):
  """
  Method to return not current, but later target price
  """
  cur = connect_to_mysql()
  if analytic and ticker:

    query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` FROM `entries` WHERE `analytic`='%s' and `ticket`='%s' AND (`price0` != 0 OR `price1` != 0 ) ORDER BY `date` DESC LIMIT 1,1" %(analytic, ticker)
    cur.execute(query)

    for row in cur.fetchall():
      if row[1] != 0 or row[2] != 0:
        # Checking the price variation (updated price or old)
        if row[2] == 0:
          price = row[1]
        else:
          price = row[2]
        item = {'date': time.mktime(row[0].timetuple()), 
          'price': price,
          'analytic': row[3],
          'ticker': row[4]}
        return item
  else:
    return None
  

def get_targetprices(analytic=None, ticker=None):
  """
  Method to return the target prices
  """
  cur = connect_to_mysql()
  results = []
  if analytic and ticker:
    query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` FROM `entries` WHERE `analytic`='%s' AND `ticket`='%s' AND (`price0`!=0 OR `price1` !=0) AND `date` < (SELECT max(`date`) FROM `entries`) ORDER BY `date`" % (re.escape(analytic), re.escape(ticker))
    """Query for the target prices, which are older than the maximum date (getting rid of the most recent one, because of model requires old data)"""
  elif not analytic and ticker:
    query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` FROM `entries` WHERE `ticket`='%s' AND (`price0` !=0 OR `price1`!=0) ORDER BY `date`" % (re.escape(ticker))
    """Query for the target prices, which belongs only to ticker"""
  elif analytic and not ticker:
    query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` FROM `entries` WHERE `analytic`='%s' AND (`price0`!=0 OR `price1`!=0) ORDER BY `date`" % (re.escape(analytic))
    """Query for the target prices, which belongs only to analytic"""
  else:
    query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` FROM `entries` WHERE `date`=(SELECT max(`date`) FROM `entries`) AND (`price0`!=0 OR `price1` != 0)"
    """Query for the most recent dates"""
  cur.execute(query)

  for row in cur.fetchall():
    change = 0
    if row[1] != 0 or row[2] != 0:
      # Checking the price variation (updated price or old)
      if row[2] == 0:
        price = row[1]
      else:
        price = row[2]
        previous_targetprice = get_previous_targetprice(row[3], row[4])
        if previous_targetprice != None:
          change = float(( price - previous_targetprice['price'] ) / price) * 100
      item = {'date': time.mktime(row[0].timetuple()), 
        'price': price,
        'analytic': row[3],
        'ticker': row[4],
        'change': change}
      """Forming the dict"""
      if item not in results:
        """Escaping possible duplicates"""
        results.append(item)

  return results