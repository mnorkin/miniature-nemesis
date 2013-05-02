#!/usr/bin/python2
import unittest
from database import database
from stock_quote import stock_quote
from features import Features


class feature_test(unittest.TestCase):
    """
    Feature testing
    """

    def setUp(self):
        """
        Database and stock market query
        """
        self.database = database()
        self.stock_quote = stock_quote()
        self.analytic = 'Oppenheimer'
        self.ticker = 'USB'
        self.beta = 0.98  # From yahoo
        self.target_data = self.database.return_targetprices(
            ticker=self.ticker,
            analytic=self.analytic
        )
        self.stock_data = self.stock_quote.get_data(
            self.ticker
        )
        self.features = Features(
            target_data=self.target_data,
            stock_data=self.stock_data,
            beta=self.beta
        )

    def tearDown(self):
        """
        Collect the toys and go home
        """
        pass

    def test_number_of_targetprices(self):
        self.assertEqual(
            len(self.target_data),
            4,
            "Number of target prices is higher than expected")

    def test_accuracy(self):
        """
        Testing Accuracy

        Alpha
        """
        self.assertEqual(
            self.features.accuracy(),
            50,
            "Accuracy calculation fail"
        )

    def test_aggresiveness(self):
        """
        Testing Aggresiveness calculations
        """
        measure = self.features.aggressiveness()
        self.assertEqual(
            measure,
            48.48,
            "Aggresiveness calculation fail %s, to %s" % (
                48.48,
                measure
            )
        )

    def test_impact_to_market(self):
        """
        Testing Impact to market calculations
        """
        measure = self.features.impact_to_market()
        self.assertEqual(
            measure,
            3.84,
            'Impact to market calculations fail %s, to %s' % (
                3.84,
                measure
            )
        )

    def test_profitability(self):
        """
        Testing profitability calculations
        """
        measure = self.features.profitability()
        self.assertEqual(
            measure,
            25.61,
            "Profitability failure %s, to %s" % (
                25.61,
                measure
            )
        )

    def test_proximity(self):
        """
        Testing proximity calculations

        Beta
        """
        measure = self.features.proximity()
        self.assertEqual(
            measure,
            10.35,
            "Proximity fail %s, to %s" % (
                10.35,
                measure
            )
        )

    def test_reach_time(self):
        """
        Testing reach time calculations
        """
        measure = self.features.reach_time()
        self.assertEqual(
            measure,
            36,
            "Reach time calculations fail %s, to %s" % (
                36,
                measure
            )
        )

    def volatility(self):
        """
        Testing volatility
        """
        measure = self.database.get_volatility(
            ticker=self.ticker,
            analytic=self.analytic
        )
        self.assertEqual(
            measure['total'],
            4,
            "Total number of tp is not okay"
        )
        self.assertEqual(
            measure['number'],
            3,
            "Volatility number is not okay"
        )

if __name__ == '__main__':
    unittest.main()
