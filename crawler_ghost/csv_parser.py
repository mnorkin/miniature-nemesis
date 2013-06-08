import csv  # CSV reading
import random  # Shuffle


class csv_parser:
    """
    CSV Parser class

    Header-less CSV parser, designed specifically for Target Price Project

    Output is sorted shuffle, if not specified otherwise
    """

    def __init__(
        self, input_file=None, output_file=None,
        delimiter=';', sort_method='shuffle'
    ):
        """
        Class initialization
        """

        self.loader = []
        self.input_file = input_file
        self.delimiter = delimiter
        self.sort_method = sort_method

    def data(self):
        """
        Method for automated work
        """
        self.sort()
        return self.loader

    def read(self):
        """
        CSV read from file method
        """

        if self.input_file:
            try:
                with open(self.input_file, 'rb') as csv_file:

                    item = {}
                    stock_reader = csv.reader(
                        csv_file,
                        delimiter=self.delimiter
                    )

                    for row in stock_reader:
                        """
                        Fetch the ticker information to the dictionary
                        """
                        item = {
                            'ticker': row[1],
                            'name': row[0],
                        }

                        if item['ticker'].isalpha():
                            """
                            Check if there are not any irregularities with the
                            ticker name
                            """
                            self.loader.append(item)

                return True
            except IOError:
                return False
        return None

    def sort(self):
        """
        Available CSV sorting:
        * alphabetically
        * shuffle
        """
        if self.loader.__len__() > 1:
            if self.sort_method == 'alphabetically':
                self.loader = sorted(
                    self.loader, key=lambda item: item['ticker'])
                return True
            elif self.sort_method == 'shuffle':
                random.shuffle(self.loader)
                return True
            else:
                return False
        return False
