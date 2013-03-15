from csv_parser import csv_parser
import rest


def main():
    """
    The almighty feeder
    """
    data = csv_parser(input_file='company_list.csv').data()

    for entry in data:
        item = {
            'name': entry['name'],
            'ticker': entry['ticker'],
            'market': ''
        }
        rest.send('POST', '/api/tickers/', item)

if __name__ == '__main__':
    main()
