import unittest
from csv_parser import csv_parser


class csv_parser_test(unittest.TestCase):
    """
    Unit test for the CSV parser
    """
    def setUp(self):
        """
        Setting up working environment
        """
        self.csv_parser_direct = csv_parser(
            input_file='company_list.csv', output_file='digested_list.csv')

        self.csv_praser_sort_a = csv_parser(
            input_file='company_list.csv',
            output_file="digested_list_sort_a.csv",
            sort_method='alphabetically')

        self.csv_praser_sort_s = csv_parser(
            input_file='company_list.csv',
            output_file='digested_list_sort_b.csv',
            sort_method='shuffle')

        self.csv_praser_sort_ex = csv_parser(
            input_file='company_list.csv',
            output_file='digested_list.csv',
            sort_method='foo')

        self.csv_praser_input_io = csv_parser(
            input_file='company_list_io.csv',
            output_file='digested_list_sort_b.csv')

        self.csv_parser_data = csv_parser(
            input_file='company_list.csv',
            sort_method='shuffle')

    def tearDown(self):
        self.csv_parser_direct = None
        self.csv_parser_sort_a = None
        self.csv_parser_sort_s = None
        self.csv_parser_sort_ex = None
        self.csv_praser_data = None

    def test_data(self):
        self.assertGreater(
            self.csv_parser_data.data().__len__(),
            1, 'Data return length fail')

    def test_read(self):
        self.assertEqual(self.csv_parser_direct.read(), True, 'Reading fail')
        self.assertEqual(
            self.csv_praser_input_io.read(), False, 'IOError fail')

    def test_sort(self):
        """
        Testing sorting
        """
        self.csv_parser_direct.read()
        self.csv_praser_sort_a.read()
        self.csv_praser_sort_s.read()
        old_loader = self.csv_praser_sort_a.loader
        self.csv_praser_sort_a.sort()
        self.assertEqual(
            self.csv_praser_sort_a.loader[1]['ticker'][0],
            'A', 'Alphabetical sort fail')

        self.assertNotEqual(
            old_loader,
            self.csv_praser_sort_a.loader, 'Alphabetical sort fail')

        self.csv_praser_sort_s.sort()

        self.assertNotEqual(
            self.csv_parser_direct.loader[10]['ticker'],
            self.csv_praser_sort_s.loader[10]['ticker'], 'Shuffle sort fail')

        self.csv_praser_sort_ex.read()
        self.assertEquals(
            self.csv_praser_sort_ex.sort(), False, 'Not existing sort fail')

    def test_write(self):
        """
        Testing write
        """
        self.assertEqual(
            self.csv_parser_direct.write(), True, 'Writing fail')

if __name__ == '__main__':
    unittest.main()
