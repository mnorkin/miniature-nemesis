#!/usr/bin/env python
import json
from logger import logger
import psycopg2
from os import listdir
from os import path
from os.path import isfile, join
import time


class importer():

    def __init__(self):
        """
        Initializatio of importer
        """
        self.logger = logger("Importer")
        self.db_config = {
            'db_name': 'tp-morbid',
            'db_username': 'postgres',
            'db_password': 'sWAgu4e7',
            'db_host': 'localhost'
        }
        self.cursor = self.connect_to_postgres()
        self.db = self.connect_to_postgres_db()
        self.absolute_path = path.dirname(path.realpath(__file__))
        self.data_dir = self.absolute_path + '/data/'

    def connect_to_postgres_db(self):
        """
        Connecting to postgresql
        Returning database object
        """
        c_l = "dbname=%(db_name)s \
        user=%(db_username)s \
        password=%(db_password)s \
        host=%(db_host)s" % self.db_config
        db = psycopg2.connect(c_l)
        return db

    def connect_to_postgres(self):
        """
        Connecting to postgres
        Returning database cursor
        """
        c_l = "dbname=%(db_name)s \
        user=%(db_username)s \
        password=%(db_password)s \
        host=%(db_host)s" % self.db_config
        db = psycopg2.connect(c_l)
        return db.cursor()

    def main(self):
        """
        The main gear
        """
        start_time = time.time()
        cur = self.db.cursor()
        for f in listdir(self.data_dir):
            if isfile(join(self.data_dir, f)):
                ticker = f.split('.')[0]
                print time.time() - start_time, "s for ", ticker
                start_time = time.time()
                ff = open(self.data_dir+f, 'r')
                json_data = json.loads(ff.read())
                print ticker
                for json_line in json_data:
                    query = "INSERT INTO stocks (ticker, pub_date, price_open, price_close, price_low, price_high) \
                        VALUES (E'%s', '%s', %s, %s, %s, %s)" % (
                            ticker,
                            json_line['date'],
                            json_line['price_open'],
                            json_line['price_close'],
                            json_line['price_low'],
                            json_line['price_high']
                    )
                    if cur.execute(query) == 1:
                        self.db.commit()

if __name__ == '__main__':
    im = importer()
    im.main()
