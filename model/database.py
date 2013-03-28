"""
The Database
"""
import MySQLdb
import re
import datetime
import time
import utils


def connect_to_mysql_db():
    """
    Connecting to mysql and return database
    """

    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="classic",
        db="morbid"
    )

    return db


def connect_to_mysql():
    """
    Connecting to the database
    """

    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="classic",
        db="morbid"
    )

    return db.cursor()


def get_analytics(ticker=None):
    """
    Returns the list of analytics
    """
    cur = connect_to_mysql()
    # Collect all the analytics

    if not ticker:
        cur.execute("SELECT DISTINCT(`analytic`) FROM `entries`")
    else:
        cur.execute("SELECT DISTINCT(`analytic`) FROM `entries` WHERE `ticket`='%s'" % re.escape(ticker))

    results = []

    for row in cur.fetchall():
        results.append(row[0])

    return results


def get_analytic(analytic=None):
    """
    Method to return the data of analytic
    """

    number_of_companies = 0
    """Number of companies"""
    number_of_tp = 0
    """Number of target prices"""
    last_target_price = 0
    """Last target price"""
    volatility_positive = 0
    """ Positive volatility
        Equals to total amount of target prices"""
    volatility_negative = 0
    """ Negative volatility
        Equals to total amount of target prices,
        which failed to be valid 250 days"""

    cur = connect_to_mysql()

    query = "SELECT COUNT(DISTINCT(`ticket`)) FROM `entries` WHERE `analytic`='%s'" % re.escape(analytic)
    """Number of companies query"""
    cur.execute(query)
    number_of_companies = cur.fetchone()[0]

    query = "SELECT COUNT(DISTINCT(`ticket`)) \
        FROM `entries` \
        WHERE `analytic`='%s' AND (`price0` != 0 OR `price1` != 0) AND `date` + INTERVAL 1 YEAR > NOW()\
        ORDER BY `date` DESC " % re.escape(analytic)
    """Number of target prices query"""

    cur.execute(query)

    number_of_tp = cur.fetchone()[0]

    query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` \
        FROM `entries` \
        WHERE `analytic`='%s' AND (`price0`!=0 OR `price1`!=0) \
        ORDER BY `date` DESC LIMIT 1" % (re.escape(analytic))
    """Last target price query"""

    cur.execute(query)

    row = cur.fetchone()

    if row[1] != 0 or row[2] != 0:
        if row[2] == 0:
            price = row[1]
        else:
            price = row[2]
    else:
        price = 0

    last_target_price = price

    query = "SELECT `ticket`, `date` \
        FROM `entries` \
        WHERE `analytic`='%s' AND (`price0` != 0 OR `price1` != 0) \
        GROUP BY `ticket`, `date`\
        ORDER BY `ticket` ASC" % re.escape(analytic)
    """Positive volatility query"""

    cur.execute(query)

    tp_buffer = []
    """Target price buffer"""

    for row in cur.fetchall():
        volatility_positive += 1
        tp_buffer.append(row)

    for index in range(0, tp_buffer.__len__()-1):
        """Loop through all the entries, sorted by name"""
        if tp_buffer[index][0] == tp_buffer[index+1][0]:
            """Check if the ticker names are the same"""
            if utils.workdaysub(tp_buffer[index][1], tp_buffer[index+1][1]) < 250:
                volatility_negative += 1

    item = {
        'number_of_companies': number_of_companies,
        'number_of_tp': number_of_tp,
        'last_target_price': last_target_price,
        'volatility_negative': volatility_negative,
        'volatility_positive': volatility_positive
    }

    return item


def get_ticker(ticker=None):
    """
    Returns the ticker information
    """
    con = connect_to_mysql()

    number_of_tp = 0
    """Number of target prices"""

    query = "SELECT `date`, `analytic` FROM `entries` \
        WHERE (`price1`!=0 OR `price0` != 0 ) AND `ticket`='%s' \
        GROUP BY `ticket`, `date` \
        ORDER BY `date` DESC" % (re.escape(ticker))

    con.execute(query)

    number_of_tp = con.fetchall().__len__()

    item = {
        "number_of_tp": number_of_tp
    }

    return item


def get_tickers(analytic=None):
    """
    Method to get the tickers, which belongs to analytic
    """
    cur = connect_to_mysql()

    results = []

    if not analytic:
        cur.execute("SELECT DISTINCT(`ticket`) FROM `entries`")
        """Fetch all existing tickers from the database"""
    else:
        cur.execute("SELECT DISTINCT(`ticket`) FROM `entries` WHERE `analytic`='%s'" % re.escape(analytic))
        """Fetch tickers which analytic works with from the database"""

    for row in cur.fetchall():
        results.append(row[0])

    return results


def get_previous_targetprice(analytic=None, ticker=None, date=None):
    """
    Method to return not current, but later target price
    """
    cur = connect_to_mysql()
    if analytic and ticker and date:

        query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` \
            FROM `entries` WHERE `analytic`=\"%s\" AND `date`<'%s' AND `ticket`='%s' AND (`price0` != 0 OR `price1` != 0 ) \
            ORDER BY `date` DESC LIMIT 1" % (analytic, date, ticker)
        cur.execute(query)

        for row in cur.fetchall():
            if row[1] != 0 or row[2] != 0:
                # Checking the price variation (updated price or old)
                if row[2] == 0:
                    price = row[1]
                else:
                    price = row[2]
                item = {
                    'date': time.mktime(row[0].timetuple()),
                    'date_human': str(row[0]),
                    'price': price,
                    'analytic': row[3],
                    'ticker': row[4]
                }
                return item
    else:
        return None


def get_targetprices(analytic=None, ticker=None):
    """
    Method to return the target prices

    On of the ideas is to use the yeild operator to speed things up
    """
    cur = connect_to_mysql()
    results = []
    if analytic and ticker:
        query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` \
            FROM `entries` \
            WHERE `analytic`='%s' AND `ticket`='%s' \
            AND (`price0`!=0 OR `price1` !=0) \
            AND `date` < (SELECT max(`date`) FROM `entries` WHERE `analytic`='%s' AND `ticket`='%s') \
            ORDER BY `date`" % (
                re.escape(analytic),
                re.escape(ticker),
                re.escape(analytic),
                re.escape(ticker))
        """Query for the target prices, which are older than the maximum date
            (getting rid of the most recent one, because of model requires
            old data)"""
    elif not analytic and ticker:
        query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` \
            FROM `entries` \
            WHERE `ticket`='%s' AND (`price0` !=0 OR `price1`!=0) \
            ORDER BY `date` ASC" % (re.escape(ticker))
        """Query for the target prices, which belongs only to ticker"""
    elif analytic and not ticker:
        query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` \
            FROM `entries` \
            WHERE `analytic`='%s' AND (`price0`!=0 OR `price1`!=0) \
            ORDER BY `date`" % (re.escape(analytic))
        """Query for the target prices, which belongs only to analytic"""
    else:
        query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` \
            FROM `entries` \
            WHERE `date` >= '2012-11-01' AND (`price0` != 0 OR `price1` != 0) \
            GROUP BY `analytic`, `date` \
            ORDER BY `date` DESC"
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

            previous_targetprice = get_previous_targetprice(row[3], row[4], row[0])
            if previous_targetprice is not None:
                change = float((price - previous_targetprice['price']) / previous_targetprice['price']) * 100
            else:
                change = 0

            item = {
                'date': time.mktime(row[0].timetuple()),
                'date_human': str(row[0]),
                'date_datetime': row[0],
                'price': price,
                'analytic': row[3],
                'ticker': row[4],
                'change': round(change, 2)
            }
            yield item
            """Forming the dict"""
            if item not in results:
                """Escaping possible duplicates"""
                results.append(item)

    # return results


def get_consensus(ticker=None):
    """
    Consensus measure calculation
    """

    measures = []
    """The averages of target prices per day"""
    evaluated_results = []
    """Constructed consensus measure"""
    if ticker:
        target_prices = get_targetprices(ticker=ticker)
        if target_prices:
            """Form a pretty order or target prices"""
            pretty_target_prices = {}
            for target_price in target_prices:
                if target_price['analytic'] not in pretty_target_prices.keys():
                    pretty_target_prices[target_price['analytic']] = list()
                pretty_target_prices[target_price['analytic']].append(target_price)

            today = datetime.datetime.now()
            """Get today date"""
            start_date = datetime.date(2006, 1, 1)
            """Start date"""
            end_date = datetime.date(today.year, today.month, today.day)
            """End date"""
            total_days = utils.workdaysub(start_date, end_date)
            """Total number of work days"""
            results = []
            """Target prices per analytic"""
            for target_price in pretty_target_prices:
                """Loop through every available ticker target price"""
                bulk = [0.0]*(total_days)
                for tp in pretty_target_prices[target_price]:
                    """Get the record"""
                    start_index = utils.workdaysub(start_date, tp['date_datetime'])
                    end_index = start_index + 250
                    # print "Start index:", start_index, "end index:", end_index, "price:", tp['price']
                    bulk[start_index:end_index] = [tp['price']]*(end_index-start_index)
                results.append(bulk)

            for row in zip(*results):
                """Transpose the results, so that every index would have a number of total target prices"""
                row_length = (len(row) - row.count(0))
                """Calculate the total amount of defined target prices and drop entries with zeros"""
                if row_length != 0:
                    """Append the mean of target prices devided by total amount of target prices on that day"""
                    measures.append(round(sum(row)/row_length, 2))

            window_length = 90
            for j in range(window_length, len(measures)-window_length):
                evaluated_results.append(round(sum(measures[j:window_length+j])/90, 2))

            item = {
                'consensus_min': min(evaluated_results),
                'consensus_avg': evaluated_results[-1],
                'consensus_max': max(evaluated_results)
            }

            return item

        else:
            return None
    else:
        return None


def get_beta(ticker):
    """
    Function to return the beta value
    """
    cur = connect_to_mysql()

    if ticker:
        query = "SELECT `beta` FROM `tickers` WHERE `name`='%s' LIMIT 1" % (
            re.escape(ticker))
        if cur.execute(query) != 0:
            row = cur.fetchone()
            return row[0]
        else:
            return None
    else:
        return None


def write_beta(ticker, beta):
    """
    Function to write beta measure to the database (In case of multiple processing same ticker )
    """
    db = connect_to_mysql_db()

    cur = db.cursor()

    if ticker and beta:
        print "Ticker and beta ok"
        query = "SELECT `id` FROM `tickers` WHERE `name`='%s' LIMIT 1" % re.escape(ticker)
        if cur.execute(query) == 0:
            print "Select returned 0"
            query = "INSERT INTO `tickers` (`name`, `beta`) VALUES ('%s', %s)" % (
                re.escape(ticker),
                beta)
            """Write beta measure"""
            if cur.execute(query) == 1:
                db.commit()
        else:
            query = "UPDATE `tickers` SET `beta`='%s' WHERE `name`='%s' LIMIT 1" % (
                re.escape(beta),
                re.escape(ticker))
            """Update beta measure"""
            cur.execute(query)
    else:
        return None
