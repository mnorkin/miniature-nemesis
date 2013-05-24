"""
Tickers display takes the list of tickers and passes it to the server.
This work is necessary in order to filter out the big list of tickers.
"""
from csv_parser import csv_parser
import rest

DATA_PATH = '/home/maksim/Work/Morbid/sp_500_data/tickers.csv'


def main():
    """
    Making tickers display filter
    """
    csvp = csv_parser(
        input_file=DATA_PATH,
        delimiter=';'
    )

    items = csvp.data()

    for item in items:
        print item
        rest.send('PUT', '/api/tickers/', item)


if __name__ == '__main__':
    main()
