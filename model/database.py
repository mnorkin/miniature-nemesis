"""
The Database
"""
import MySQLdb
import re
import time
import utils


class database:

    def __init__(self):
        self.cursor = self.connect_to_mysql()
        self.db = self.connect_to_mysql_db()

    def connect_to_mysql_db(self):
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

    def connect_to_mysql(self):
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

    def get_analytics(self, ticker=None):
        """
        Returns the list of analytics
        """
        # Collect all the analytics

        if not ticker:
            self.cursor.execute("SELECT DISTINCT(`analytic`) FROM `entries`")
        else:
            self.cursor.execute("SELECT DISTINCT(`analytic`) FROM `entries` WHERE `ticket`='%s'" % re.escape(ticker))

        for row in self.cursor.fetchall():
            yield row[0]

    def get_analytic(self, analytic=None):
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

        query = "SELECT COUNT(DISTINCT(`ticket`)) FROM `entries` WHERE `analytic`='%s'" % re.escape(analytic)
        """Number of companies query"""
        self.cursor.execute(query)
        number_of_companies = self.cursor.fetchone()[0]

        query = "SELECT COUNT(DISTINCT(`ticket`)) \
            FROM `entries` \
            WHERE `analytic`='%s' AND (`price0` != 0 OR `price1` != 0) AND `date` + INTERVAL 1 YEAR > NOW()\
            ORDER BY `date` DESC " % re.escape(analytic)
        """Number of target prices query"""

        self.cursor.execute(query)

        number_of_tp = self.cursor.fetchone()[0]

        query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` \
            FROM `entries` \
            WHERE `analytic`='%s' AND (`price0`!=0 OR `price1`!=0) \
            ORDER BY `date` DESC LIMIT 1" % (re.escape(analytic))
        """Last target price query"""

        self.cursor.execute(query)

        row = self.cursor.fetchone()

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

        self.cursor.execute(query)

        tp_buffer = []
        """Target price buffer"""

        for row in self.cursor.fetchall():
            volatility_positive += 1
            tp_buffer.append(row)

        for index in range(0, tp_buffer.__len__()-1):
            """Loop through all the entries, sorted by name"""
            if tp_buffer[index][0] == tp_buffer[index+1][0]:
                """Check if the ticker names are the same"""
                if utils.workdaysub(tp_buffer[index][1], tp_buffer[index+1][1]) < 250:
                    volatility_negative += 1

        item = {
            'volatility_negative': volatility_negative,
            'volatility_positive': volatility_positive
        }

        return item

    def get_ticker(self, ticker=None):
        """
        Returns the ticker information
        """

        number_of_tp = 0
        """Number of target prices"""

        query = "SELECT `date`, `analytic` FROM `entries` \
            WHERE (`price1`!=0 OR `price0` != 0 ) AND `ticket`='%s' \
            GROUP BY `ticket`, `date` \
            ORDER BY `date` DESC" % (re.escape(ticker))

        self.cursor.execute(query)

        number_of_tp = self.cursor.fetchall().__len__()

        item = {
            "number_of_tp": number_of_tp
        }

        return item

    def get_tickers(self, analytic=None):
        """
        Method to get the tickers, which belongs to analytic
        """
        results = []

        if not analytic:
            self.cursor.execute("SELECT DISTINCT(`ticket`) FROM `entries`")
            """Fetch all existing tickers from the database"""
        else:
            self.cursor.execute("SELECT DISTINCT(`ticket`) FROM `entries` WHERE `analytic`='%s'" % re.escape(analytic))
            """Fetch tickers which analytic works with from the database"""

        for row in self.cursor.fetchall():
            results.append(row[0])

        return results

    def get_previous_targetprice(self, analytic=None, ticker=None, date=None):
        """
        Method to return not current, but later target price
        """
        if analytic and ticker and date:

            query = "SELECT `date`, `price0`, `price1`, `analytic`, `ticket` \
                FROM `entries` WHERE `analytic`=\"%s\" AND `date`<'%s' AND `ticket`='%s' AND (`price0` != 0 OR `price1` != 0 ) \
                ORDER BY `date` DESC LIMIT 1" % (analytic, date, ticker)
            self.cursor.execute(query)

            for row in self.cursor.fetchall():
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

    def return_targetprices(self, analytic=None, ticker=None):
        """
        Complete return of target prices, specified by analytic and ticker
        """
        if analytic and ticker:
            results = []
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
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                change = 0
                if row[1] != 0 or row[2] != 0:
                    # Checking the price variation (updated price or old)
                    if row[2] == 0:
                        price = row[1]
                    else:
                        price = row[2]

                    previous_targetprice = self.get_previous_targetprice(row[3], row[4], row[0])
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
                    """Forming the dict"""
                    if item not in results:
                        """Escaping possible duplicates"""
                        results.append(item)

            return results
        else:
            return None

    def get_targetprices(self, analytic=None, ticker=None):
        """
        Method to return the target prices

        On of the ideas is to use the yeild operator to speed things up
        """
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
                WHERE `date` >= '2013-02-01' AND (`price0` != 0 OR `price1` != 0) \
                GROUP BY `analytic`, `date` \
                ORDER BY `date` DESC"
            """Query for the most recent dates"""
        self.cursor.execute(query)

        for row in self.cursor.fetchall():
            change = 0
            if row[1] != 0 or row[2] != 0:
                # Checking the price variation (updated price or old)
                if row[2] == 0:
                    price = row[1]
                else:
                    price = row[2]

                previous_targetprice = self.get_previous_targetprice(row[3], row[4], row[0])
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

    def get_number_of_target_prices(self, analytic=None, ticker=None):
        """
        Returns the target price number of analytic to ticker

        Returns the number of target prices, which are older than a YEAR,
        which makes them include into the calculations
        """
        if analytic and ticker:
            query = "SELECT COUNT(`id`) \
                FROM `entries` \
                WHERE `analytic`='%s' AND `ticket`='%s' AND (`price0` != 0 OR `price1` != 0) \
                AND `date` + INTERVAL 1 YEAR < NOW()" % (
                    re.escape(analytic), re.escape(ticker))
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        else:
            return None

    def get_consensus(self, ticker=None):
        """
        All the active target prices min/avg/max
        """
        if ticker:
            query = "SELECT `price0`, `price1`, `analytic`, `ticker` \
                FROM `entries` \
                WHERE `tiket`= '%s' AND (`price0` != 0 OR `price1` != 0) \
                GROUP BY `analytic`, `date` \
                ORDER BY `date` DESC"
            self.cursor.execute(query)

    def get_beta(self, ticker=None):
        """
        Function to return the beta value
        """
        if ticker:
            query = "SELECT `beta` FROM `tickers` WHERE `name`='%s' LIMIT 1" % (
                re.escape(ticker))
            if self.cursor.execute(query) != 0:
                row = self.cursor.fetchone()
                return row[0]
            else:
                return None
        else:
            return None

    def write_beta(self, ticker=None, beta=None):
        """
        Function to write beta measure to the database (In case of multiple processing same ticker )
        """
        cur = self.db.cursor()  # Make a private cursor, from the db link

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
                    self.db.commit()
            else:
                query = "UPDATE `tickers` SET `beta`='%s' WHERE `name`='%s' LIMIT 1" % (
                    re.escape(beta),
                    re.escape(ticker))
                """Update beta measure"""
                cur.execute(query)
        else:
            return None
