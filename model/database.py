"""
The Database
"""
import MySQLdb
import psycopg2
import re
import time
from logger import logger


class database:

    def __init__(self):
        # TODO: tests
        self.cursor = self.connect_to_postgres()
        self.db = self.connect_to_postgres_db()
        self.logger = logger('database')
        self.logger.debug('Starting')

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

    def connect_to_postgres_db(self):
        """
        Connecting to postgresql
        Returning database object
        """
        c_l = "dbname=tp-morbid user=postgres password=sWAgu4e7 host=localhost"
        db = psycopg2.connect(c_l)
        return db

    def connect_to_postgres(self):
        """
        Connecting to postgres
        Returning database cursor
        """
        c_l = "dbname=tp-morbid user=postgres password=sWAgu4e7 host=localhost"
        db = psycopg2.connect(c_l)
        return db.cursor()

    # Password for the postgres: sWAgu4e7

    def get_analytic_names(self, ticker=None):
        """
        Returns the names of analytics

        If the ticker is defined -- returns all the analytics,
        which has any relationship with specific ticker
        """

        if not ticker:
            self.cursor.execute("SELECT DISTINCT ON (analytic) FROM entries")
        else:
            self.cursor.execute("SELECT DISTINCT ON (analytic) FROM entries WHERE ticker='%s'" % re.escape(ticker))

        for row in self.cursor.fetchall():
            yield row[0]

    def get_ticker_number_of_targetprices(self, ticker=None):
        """
        Returns ticker number of target prices
        """

        number_of_tp = 0
        """Number of target prices"""

        query = "SELECT DISTINCT ON (pub_date) COUNT(id) FROM entries \
            WHERE price0 != 0 AND ticker='%s' \
            ORDER BY pub_date DESC" % (re.escape(ticker))

        self.cursor.execute(query)

        number_of_tp = self.cursor.fetchone()[0]

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
            self.cursor.execute("SELECT DISTINCT(ticker) FROM entries")
            """Fetch all existing tickers from the database"""
        else:
            self.cursor.execute("SELECT DISTINCT(ticker) FROM entries WHERE analytic='%s'" % re.escape(analytic))
            """Fetch tickers which analytic works with from the database"""

        for row in self.cursor.fetchall():
            results.append(row[0])

        return results

    # def get_previous_targetprice(self, analytic=None, ticker=None, date=None):
    #     """
    #     Method to return not current, but later target price
    #     """
    #     if analytic and ticker and date:

    #         query = "SELECT date, price0, price1, analytic, ticker \
    #             FROM entries WHERE analytic=\"%s\" AND pub_date < '%s' AND ticker='%s' AND (price0 != 0 OR price1 != 0 ) \
    #             ORDER BY pub_date DESC LIMIT 1" % (analytic, date, ticker)
    #         self.cursor.execute(query)

    #         for row in self.cursor.fetchall():
    #             if row[1] != 0 or row[2] != 0:
    #                 # Checking the price variation (updated price or old)
    #                 if row[2] == 0:
    #                     price = row[1]
    #                 else:
    #                     price = row[2]
    #                 item = {
    #                     'date': time.mktime(row[0].timetuple()),
    #                     'date_human': str(row[0]),
    #                     'price': price,
    #                     'analytic': row[3],
    #                     'ticker': row[4]
    #                 }
    #                 return item
    #     else:
    #         return None

    def return_targetprices(self, analytic=None, ticker=None):
        """
        Complete return of target prices, specified by analytic and ticker
        """
        if analytic and ticker:
            results = []
            query = "SELECT DISTINCT ON (pub_date) pub_date, price0, analytic, ticker \
                FROM entries \
                WHERE analytic=E'%s' AND ticker='%s' AND price0 != 0 \
                AND pub_date < (SELECT max(pub_date) FROM entries WHERE analytic=E'%s' AND ticker='%s') \
                ORDER BY pub_date" % (
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

                # previous_targetprice = self.get_previous_targetprice(row[3], row[4], row[0])
                # Change is calculated in the app, because it needs the
                # Target price data
                change = 0

                item = {
                    'date': time.mktime(row[0].timetuple()),
                    'date_human': str(row[0]),
                    'date_datetime': row[0],
                    'price': row[1],
                    'analytic': row[2],
                    'ticker': row[3],
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
            query = "SELECT DISTINCT ON (analytic) pub_date, price0 analytic, ticker \
                FROM entries \
                WHERE analytic=E'%s' AND ticker='%s' \
                AND price0 != 0 \
                AND pub_date < (SELECT max(pub_date) FROM entries WHERE analytic=E'%s' AND ticker='%s') \
                ORDER BY pub_date" % (
                    re.escape(analytic),
                    re.escape(ticker),
                    re.escape(analytic),
                    re.escape(ticker))
            """Query for the target prices, which are older than the maximum date
                (getting rid of the most recent one, because of model requires
                old data)"""
        elif not analytic and ticker:
            query = "SELECT DISTINCT ON (pub_date) pub_date, price0, analytic, ticker \
                FROM entries \
                WHERE ticker='%s' AND price0 != 0 \
                ORDER BY pub_date ASC" % (re.escape(ticker))
            """Query for the target prices, which belongs only to ticker"""
        elif analytic and not ticker:
            query = "SELECT DISTINCT ON (pub_date) pub_date, price0, analytic, ticker \
                FROM entries \
                WHERE analytic=E'%s' AND price0 != 0 \
                ORDER BY pub_date" % (re.escape(analytic))
            """Query for the target prices, which belongs only to analytic"""
        else:
            # Query to retrieve the most recent target prices of analytic
            query = "SELECT DISTINCT ON (pub_date) pub_date, price0, analytic, ticker \
                FROM entries \
                WHERE pub_date >= NOW() - interval '1 year' AND price0 != 0 \
                ORDER BY pub_date"
        self.cursor.execute(query)

        for row in self.cursor.fetchall():
            change = 0

            # Need to thing how to calculate this change measure
            # previous_targetprice = self.get_previous_targetprice(row[3], row[4], row[0])
            # if previous_targetprice is not None:
            #     change = float((price - previous_targetprice['price']) / previous_targetprice['price']) * 100
            # else:
            # Change is calculated else place
            change = 0

            item = {
                'date': time.mktime(row[0].timetuple()),
                'date_human': str(row[0]),
                'date_datetime': row[0],
                'price': row[1],
                'analytic': row[2],
                'ticker': row[3].strip(),
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
            query = "SELECT COUNT(pub_date) \
                FROM ( \
                    SELECT DISTINCT pub_date FROM entries \
                    WHERE analytic=E'%s' AND ticker='%s' \
                    AND price0 != 0 \
                    AND pub_date < ( \
                            SELECT max(pub_date) FROM entries \
                            WHERE analytic = E'%s' AND ticker='%s' \
                            AND price0 != 0 \
                        ) \
                    ORDER BY pub_date \
                    ) p" % (
                    re.escape(analytic),
                    re.escape(ticker),
                    re.escape(analytic),
                    re.escape(ticker))

            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        else:
            return None

    def get_volatility(self, analytic=None, ticker=None):
        """
        Volatility measure

        Volatility defines how many target prices where not hold 1 YEAR
        """
        number = 0
        if analytic and ticker:
            # Select unique dates, older than a year
            query = "SELECT DISTINCT ON (pub_date) pub_date \
                FROM entries \
                WHERE analytic=E'%s' AND ticker='%s' AND price0 != 0 \
                AND pub_date + INTERVAL '1 year' < NOW() \
                ORDER BY pub_date ASC" % (
                    re.escape(analytic),
                    re.escape(ticker))

            self.cursor.execute(query)

            # Removing bulk
            dates = [x[0] for x in self.cursor.fetchall()]
            # Total number of target prices
            dates_length = len(dates)
            # Iteratation
            for index, pub_date in enumerate(dates):
                if index < dates_length - 1:
                    # If the time length is approx ~250 work days
                    if (dates[index+1] - dates[index]).days > 365:
                        number += 1

            item = {
                'number': number,
                'total': dates_length
            }

            return item
        else:
            return None

    def get_consensus(self, ticker=None):
        """
        All the active target prices min/avg/max
        on the specitic ticker
        """
        if ticker:
            query = "SELECT DISTINCT ON (analytic) analytic, pub_date, price0 \
                FROM ( \
                    SELECT * FROM entries \
                    WHERE ticker = '%s' \
                    AND price0 != 0 \
                    ) p \
                GROUP BY pub_date, analytic, price0 \
                ORDER BY analytic, pub_date desc, price0;" % (
                    re.escape(ticker))
            self.cursor.execute(query)

            data = []

            for row in self.cursor.fetchall():
                data.append(row[2])

            self.logger.debug('ticker %s' % ticker)

            self.logger.debug('data %s' % data)

            try:
                item = {
                    'min': min(data),
                    'avg': sum(data)/len(data),
                    'max': max(data)
                }
            except ValueError:
                item = {
                    'min': 0,
                    'avg': 0,
                    'max': 0
                }

            return item

    def get_beta(self, ticker=None):
        """
        Function to return the beta value
        """
        if ticker:
            query = "SELECT value FROM betas WHERE name='%s' LIMIT 1" % (
                re.escape(ticker))
            if self.cursor.execute(query) != 0:
                row = self.cursor.fetchone()
                try:
                    return row[0]
                except:
                    return None
            else:
                return None
        else:
            return None

    def write_beta(self, ticker=None, beta=None):
        """
        Function to write beta measure to the database (In case of multiple
        processing same ticker )
        """
        self.logger.debug('Received beta: %s' % beta)
        self.logger.debug('ticker %s' % ticker)
        cur = self.db.cursor()  # Make a private cursor, from the db link

        if ticker and beta:
            self.logger.debug("Ticker and beta ok")
            query = "SELECT count(id) FROM betas WHERE name='%s'" % re.escape(ticker)
            cur.execute(query)
            if cur.fetchone()[0] == 0:
                self.logger.debug("Select returned 0 length")
                query = "INSERT INTO betas (name, value) VALUES ('%s', %d)" % (
                    re.escape(ticker),
                    beta)
                """Write beta measure"""
                if cur.execute(query) == 1:
                    self.db.commit()
            else:
                query = "UPDATE betas SET value='%s' WHERE name='%s'" % (
                    beta,
                    re.escape(ticker))
                """Update beta measure"""
                cur.execute(query)
        else:
            return None
