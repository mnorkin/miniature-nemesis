"""
The Feature
"""
# from plot import Plot
import datetime
import utils
import inspect
import array
from stock_quote import stock_quote
from logger import logger


class Features:

    target_data = []
    """Target price data"""
    stock_data = []
    """Stock price data"""
    market_data = []
    """Market data"""
    local_target_data = []
    stock_dates = []
    stock_highs = array.array('f')
    stock_lows = array.array('f')
    stock_closes = array.array('f')
    _plot = None
    _show_plot = False
    calculated_feature_data = []
    beta = 1

    # Units of measurement
    units = {
        'percent': {
            'unit_id': 1,
            'name': 'Percent',
            'value': '%'
        },
        'days': {
            'unit_id': 2,
            'name': 'Days',
            'value': 'd'
        }
    }

    # Features
    features = {
        'accuracy':
        {
            'name': 'Accuracy',
            'display_in_frontpage': 1,
            'unit_id': 1,
            'position': 1
        },
        'proximity':
        {
            'name': 'Proximity',
            'display_in_frontpage': 0,
            'unit_id': 1,
            'position': 2
        },
        'profitability':
        {
            'name': 'Profitability',
            'display_in_frontpage': 1,
            'unit_id': 1,
            'position': 3
        },
        'aggressiveness':
        {
            'name': 'Aggressiveness',
            'display_in_frontpage': 0,
            'unit_id': 1,
            'position': 4
        },
        'reach_time':
        {
            'name': 'Reach time',
            'display_in_frontpage': 1,
            'unit_id': 2,
            'position': 5
        },
        'impact_to_market':
        {
            'name': 'Impact to market',
            'display_in_frontpage': 0,
            'unit_id': 1,
            'position': 6
        }
    }

    def __init__(
        self,
        target_data=None,
        stock_data=None,
        beta=None,
        plot=False,
        calculate=False
    ):
        """
        Initialization of the class
        * Pass the arguments to fetch the target price data
        """
        self.logger = logger('Features')
        self.stock_quote = stock_quote()

        if target_data and stock_data:
            self.logger.info('TP and Stock data ok')

            self.target_data = target_data
            self.stock_data = stock_data

            self.market_data = self.stock_quote.get_data('^GSPC')

            self.local_target_data = [[self.target_data[i]['date'], self.target_data[i]['price']] for i in range(0, self.target_data.__len__())]
            self.stock_dates = [self.stock_data[i]['date'] for i in range(0, self.stock_data.__len__())]
            self.stock_highs = [self.stock_data[i]['high'] for i in range(0, self.stock_data.__len__())]
            self.stock_closes = [self.stock_data[i]['close'] for i in range(0, self.stock_data.__len__())]
            self.stock_lows = [self.stock_data[i]['low'] for i in range(0, self.stock_data.__len__())]

            self.market_dates = [self.market_data[i]['date'] for i in range(0, self.market_data.__len__())]
            self.market_highs = [self.market_data[i]['high'] for i in range(0, self.market_data.__len__())]
            self.market_closes = [self.market_data[i]['close'] for i in range(0, self.market_data.__len__())]
            self.market_lows = [self.market_data[i]['low'] for i in range(0, self.market_data.__len__())]

            self.beta = beta

        if plot:
            self._show_plot = True

        if calculate:
            self.calculated_feature_data = []
            for method, bound in inspect.getmembers(self, predicate=inspect.ismethod):
                if method != '__init__' and method != 'values':
                    self.logger.debug(method)
                    item = {'feature_slug': method, 'value': bound()}
                    self.logger.debug(item)
                    self.calculated_feature_data.append(item)

    def values(self):
        """
        Returning all the values
        """
        return self.calculated_feature_data

    def accuracy(self):
        """
        Accuracy measure
        """
        self.logger.debug('Accuracy')
        results = []

        if self._show_plot:
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__())], 'g')
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['low']] for i in range(0, self.stock_data.__len__())], 'b')

        for target_entry in self.local_target_data:
            measure = 0
            target_date = target_entry[0]
            target_price = target_entry[1]

            try:
                start_index = next(i for i, x in enumerate(self.stock_dates) if x == target_date)
                end_index = start_index+249

                if end_index >= self.stock_dates.__len__():
                    end_index = self.stock_dates.__len__()-2

                self.logger.debug("Total length: %s" % self.stock_dates.__len__())
                self.logger.debug("Start index: %s " % start_index)
                self.logger.debug("End Index: %s" % end_index)
                self.logger.debug("From %s" % datetime.datetime.fromtimestamp(self.stock_dates[start_index]))
                self.logger.debug("To %s" % datetime.datetime.fromtimestamp(self.stock_dates[end_index]))
                self.logger.debug("Stock from: %s" % datetime.datetime.fromtimestamp(self.stock_dates[0]))
                self.logger.debug("Stock to: %s" % datetime.datetime.fromtimestamp(self.stock_dates[-1]))

                if self._show_plot:
                    self._plot.plot_continue([[self.stock_dates[start_index], target_price], [self.stock_dates[end_index], target_price]], 'b')

                for j in range(start_index, end_index):
                    if self.stock_highs[j] >= target_price and self.stock_highs[j-1] < target_price and measure is 0:
                        self.logger.debug("Bump on")
                        self.logger.debug("Target price: %d" % target_price)
                        self.logger.debug("Stock high %d %d" % (self.stock_highs[j-1], self.stock_highs[j]))
                        if self._show_plot:
                            self._plot.plot_point(self.stock_dates[j], self.stock_highs[j])
                            self._plot.plot_point(self.stock_dates[j-1], self.stock_highs[j-1])

                        measure = 1
                    elif self.stock_lows[j] >= target_price and self.stock_lows[j-1] < target_price and measure is 0:
                        self.logger.debug("Bump on")
                        self.logger.debug("Target price: %d" % target_price)
                        self.logger.debug("Low high %d %d" % (self.stock_lows[j-1], self.stock_lows[j]))
                        if self._show_plot:
                            self._plot.plot_point(self.stock_dates[j], self.stock_lows[j])
                            self._plot.plot_point(self.stock_dates[j-1], self.stock_lows[j-1])

                        measure = 1
                    elif self.stock_highs[j] <= target_price and self.stock_highs[j-1] > target_price and measure is 0:
                        self.logger.debug("Bump on")
                        self.logger.debug("Target price: %d" % target_price)
                        self.logger.debug("Stock high %d %d" % (self.stock_highs[j-1], self.stock_highs[j]))
                        if self._show_plot:
                            self._plot.plot_point(self.stock_dates[j], self.stock_highs[j])
                            self._plot.plot_point(self.stock_dates[j-1], self.stock_highs[j-1])
                        measure = 1
                    elif self.stock_lows[j] <= target_price and self.stock_lows[j-1] > target_price and measure is 0:
                        self.logger.debug("Bump on")
                        self.logger.debug("Target price: %d" % target_price)
                        self.logger.debug("Low high %d %d" % (self.stock_lows[j-1], self.stock_lows[j]))
                        if self._show_plot:
                            self._plot.plot_point(self.stock_dates[j], self.stock_lows[j])
                            self._plot.plot_point(self.stock_dates[j-1], self.stock_lows[j-1])
                        measure = 1

                results.append(float(measure))

            except StopIteration:
                """
                This happens, then target data is older, than the stock data -- NGL
                Making this kind of measure as not reached at all
                """
                self.logger.debug("Stopped iteration on %s %s" % (
                    datetime.datetime.fromtimestamp(target_date),
                    target_price
                ))
                self.logger.debug("Stock dates from %s to %s" % (
                    datetime.datetime.fromtimestamp(self.stock_dates[0]),
                    datetime.datetime.fromtimestamp(self.stock_dates[-1])
                ))
                results.append(float(0))

        result = float(sum(results)/self.local_target_data.__len__()) * 100

        self.logger.debug("Accuracy measure")
        self.logger.debug("Results: %s " % results)
        self.logger.debug("Return result: %s " % result)

        return round(result, 2)

    def proximity(self):
        """
        Proximity measure

        AKA proximity
        """
        results = []
        self.logger.debug("Proximity")

        if self._show_plot:
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__())], 'g')
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['low']] for i in range(0, self.stock_data.__len__())], 'b')

        # Looping through the target data
        for index, target_entry in enumerate(self.local_target_data):
            measure = 0
            # First field of target entry is the date
            target_date = target_entry[0]
            # Second field of target entry is the price
            target_price = target_entry[1]
            try:
                self.logger.debug('Stock dates format %s ' % self.stock_dates[1])
                self.logger.debug('Target date format %s ' % target_date)
                start_index = next(i for i, x in enumerate(self.stock_dates) if x == target_date)
                end_index = start_index+249

                if index < self.local_target_data.__len__()-1:
                    next_start_index = next(i for i, x in enumerate(self.stock_dates) if x == self.local_target_data[index+1][0])
                else:
                    next_start_index = self.stock_dates.__len__()-1

                if end_index >= next_start_index:
                    end_index = next_start_index

                self.logger.debug("Start index: %s" % start_index)
                self.logger.debug("End Index: %s" % end_index)
                self.logger.debug("Next start index: %s " % next_start_index)
                self.logger.debug("From: %s" % datetime.datetime.fromtimestamp(
                    self.stock_dates[start_index]))
                self.logger.debug("To: %s" % datetime.datetime.fromtimestamp(
                    self.stock_dates[end_index]))
                self.logger.debug("Stock from: %s" % datetime.datetime.fromtimestamp(
                    self.stock_dates[0]))
                self.logger.debug("Stock to: %s" % datetime.datetime.fromtimestamp(
                    self.stock_dates[self.stock_dates.__len__()-1]))

                if self._show_plot:
                    self._plot.plot_continue([[self.stock_dates[start_index], target_price], [self.stock_dates[end_index], target_price]])

                number_of_entries = range(start_index, end_index).__len__()
                self.logger.debug("Number of entries: %s" % number_of_entries)

                for j in range(start_index, end_index):
                    if target_price > self.stock_lows[j] and target_price > self.stock_highs[j]:
                        measure = measure + abs(float(self.stock_highs[j] - target_price))/number_of_entries
                    elif target_price < self.stock_lows[j] and target_price < self.stock_highs[j]:
                        measure = measure + abs(float(self.stock_lows[j] - target_price))/number_of_entries

                results.append(measure)
            except StopIteration:
                """
                This happens, then target data is older, than the stock data -- NGL
                Making this kind of measure as not reached at all
                """
                self.logger.debug("Stopped iteration on %s %s " % (
                    datetime.datetime.fromtimestamp(target_date), target_price
                ))
                self.logger.debug("Stock dates from %s %s " % (
                    datetime.datetime.fromtimestamp(self.stock_dates[0]),
                    datetime.datetime.fromtimestamp(self.stock_dates[-1])
                ))
                results.append(float(0))

        result = float(sum(results)/self.local_target_data.__len__())

        self.logger.debug("Proximity measure")
        self.logger.debug("Results: %s" % results)
        self.logger.debug("Return result: %s" % result)

        return round(result, 2)

    def aggressiveness(self):
        """
        Aagressiveness measure

        AKA aggression
        """
        results = []
        self.logger.debug('Aggressiveness')

        if self._show_plot:
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__())], 'g')
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['low']] for i in range(0, self.stock_data.__len__())], 'b')

        for index, target_entry in enumerate(self.local_target_data):
            measure = 0
            target_date = target_entry[0]
            target_price = target_entry[1]
            try:
                start_index = next(i for i, x in enumerate(self.stock_dates) if x == target_date)

                self.logger.debug("Analysis index: %s" % start_index)
                self.logger.debug("Analysis date: %s" % datetime.datetime.fromtimestamp(self.stock_dates[start_index]))
                self.logger.debug("Stock from: %s" % datetime.datetime.fromtimestamp(self.stock_dates[0]))
                self.logger.debug("Stock to: %s" % datetime.datetime.fromtimestamp(self.stock_dates[self.stock_dates.__len__()-1]))

                if self._show_plot:
                    self._plot.plot_point(self.stock_dates[start_index], target_price)

                measure = abs(float((target_price - self.stock_closes[start_index])/self.stock_closes[start_index]))

                results.append(measure)

            except StopIteration:
                """
                This happens, then target data is older, than the stock data -- NGL
                Making this kind of measure as not reached at all
                """
                self.logger.debug("Stopped iteration on %s %s " % (
                    datetime.datetime.fromtimestamp(target_date),
                    target_price
                ))
                self.logger.debug("Stock dates from %s to %s " % (
                    datetime.datetime.fromtimestamp(self.stock_dates[0]),
                    datetime.datetime.fromtimestamp(self.stock_dates[-1])
                ))
                results.append(float(0))

        result = float(sum(results)/self.local_target_data.__len__()) * 100

        self.logger.debug("Aggressiveness measure")
        self.logger.debug("Results: %s " % results)
        self.logger.debug("Return result: %s " % result)

        return round(result, 2)

    def profitability(self):
        """
        Profitability measure
        """
        results = []

        if self._show_plot:
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__())], 'g')
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['low']] for i in range(0, self.stock_data.__len__())], 'b')

        for target_entry in self.local_target_data:
            measure = 0
            target_date = target_entry[0]
            target_price = target_entry[1]
            try:
                start_index = next(i for i, x in enumerate(self.stock_dates) if x == target_date)
                end_index = start_index+249

                if end_index >= self.stock_dates.__len__():
                    end_index = self.stock_dates.__len__()-1

                self.logger.debug("Start index: %s " % start_index)
                self.logger.debug("End Index: %s" % end_index)
                self.logger.debug("From: %s" % datetime.datetime.fromtimestamp(self.stock_dates[start_index]))
                self.logger.debug("To: %s" % datetime.datetime.fromtimestamp(self.stock_dates[end_index]))
                self.logger.debug("Stock from: %s" % datetime.datetime.fromtimestamp(self.stock_dates[0]))
                self.logger.debug("Stock to: %s" % datetime.datetime.fromtimestamp(self.stock_dates[self.stock_dates.__len__()-1]))

                if self._show_plot:
                    self._plot.plot_continue([[self.stock_dates[start_index], target_price], [self.stock_dates[end_index], target_price]], 'b')

                start_close_price = self.stock_closes[start_index]
                end_close_price = self.stock_closes[end_index]
                if target_price > start_close_price:
                    """Long"""
                    measure = (end_close_price - start_close_price)/start_close_price
                elif target_price < start_close_price:
                    """Short"""
                    measure = (start_close_price - end_close_price)/start_close_price

                results.append(measure)
            except StopIteration:
                self.logger.debug("Stopped iteration on %s %s " % (
                    datetime.datetime.fromtimestamp(target_date),
                    target_price
                ))
                self.logger.debug("Stock dates from %s to %s" % (
                    datetime.datetime.fromtimestamp(self.stock_dates[0]),
                    datetime.datetime.fromtimestamp(self.stock_dates[-1])
                ))
                results.append(float(0))

        result = float(sum(results)/self.local_target_data.__len__()) * 100

        self.logger.debug("Profitability measure")
        self.logger.debug("Results: %s" % results)
        self.logger.debug("Return result: %s" % result)

        return round(result, 2)

    # def max_profitability(self):
    #     """
    #     Maximum profitability measure
    #     """
    #     results = []
    #     self.logger.debug("Maximum profitability")

    #     if self._show_plot:
    #         self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__())], 'g')
    #         self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['low']] for i in range(0, self.stock_data.__len__())], 'b')

    #     for target_entry in self.local_target_data:
    #         measure = 0
    #         target_date = target_entry[0]
    #         target_price = target_entry[1]
    #         try:
    #             start_index = next(i for i, x in enumerate(self.stock_dates) if x == target_date)
    #             end_index = start_index+249

    #             if end_index >= self.stock_dates.__len__():
    #                 end_index = self.stock_dates.__len__()-1

    #             self.logger.debug("\nStart index: %s" % start_index)
    #             self.logger.debug("\nEnd Index: %s" % end_index)
    #             self.logger.debug("\nFrom: %s" % datetime.datetime.fromtimestamp(self.stock_dates[start_index]))
    #             self.logger.debug("\nTo: %s" % datetime.datetime.fromtimestamp(self.stock_dates[end_index]))
    #             self.logger.debug("\nStock from: %s" % datetime.datetime.fromtimestamp(self.stock_dates[0]))
    #             self.logger.debug("\nStock to: %s" % datetime.datetime.fromtimestamp(self.stock_dates[self.stock_dates.__len__()-1]))

    #             if self._show_plot:
    #                 self._plot.plot_continue([[self.stock_dates[start_index], target_price], [self.stock_dates[end_index], target_price]])

    #             start_close_price = self.stock_closes[start_index]

    #             if target_price > start_close_price:
    #                 """Long"""
    #                 for j in range(start_index, end_index):
    #                     if measure < self.stock_highs[j]:
    #                         """Get highest high price in the time window"""
    #                         measure = self.stock_highs[j]

    #                 measure = (measure - start_close_price) / start_close_price
    #                 """Calculate the measure"""

    #             elif target_price < start_close_price:
    #                 """
    #                 Short
    #                 """
    #                 for j in range(start_index, end_index):
    #                     if measure > self.stock_lows[j]:
    #                         """Get lowest low price in the time window"""
    #                         measure = self.stock_lows[j]

    #                 measure = (start_close_price - measure) / start_close_price
    #                 """Calculate the measure"""

    #             results.append(measure)
    #         except StopIteration:
    #             self.logger.debug("Stopped iteration on %s %s" % (
    #                 datetime.datetime.fromtimestamp(target_date),
    #                 target_price
    #             ))
    #             self.logger.debug("Stock dates from %s to %s" % (
    #                 datetime.datetime.fromtimestamp(self.stock_dates[0]),
    #                 datetime.datetime.fromtimestamp(self.stock_dates[-1])
    #             ))
    #             results.append(float(0))

    #     result = float(sum(results)/self.local_target_data.__len__())

    #     self.logger.debug("\n\nMax profitability\n")
    #     self.logger.debug("Results: %s" % results)
    #     self.logger.debug("Return result: %s" % result)

    #     return round(result, 2)

    def impact_to_market(self):
        """
        Impart to the market measure

        TODO

        Problems:
        * Where to get the exchange index history ?

        """

        self.logger.debug("Impact to market")
        results = []

        if self._show_plot:
            # Plot stock data
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__())], 'g')
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['low']] for i in range(0, self.stock_data.__len__())], 'b')
            # Plot market data
            self._plot.plot_continue([[self.market_data[i]['date'], self.market_data[i]['high']] for i in range(0, self.market_data.__len__())], 'y')
            self._plot.plot_continue([[self.market_data[i]['date'], self.market_data[i]['low']] for i in range(0, self.market_data.__len__())], 'r')

        for target_entry in self.local_target_data[-1:]:
            measure = 0
            market_price_change = 0
            stock_price_change = 0
            target_date = target_entry[0]
            target_price = target_entry[1]
            try:
                start_index = next(i for i, x in enumerate(self.stock_dates) if x == target_date)
                end_index = start_index+2

                start_market_index = next(i for i, x in enumerate(self.market_dates) if x == target_date)
                end_market_index = start_market_index + 2

                if end_index >= self.stock_dates.__len__():
                    end_index = self.stock_dates.__len__()-1

                if end_market_index >= self.market_dates.__len__():
                    end_market_index = self.market_dates.__len__() - 1

                if utils.DEBUG:
                    self.logger.debug("Start index: %s" % start_index)
                    self.logger.debug("End Index: %s" % end_index)
                    self.logger.debug("From: %s" % datetime.datetime.fromtimestamp(self.stock_dates[start_index]))
                    self.logger.debug("To: %s" % datetime.datetime.fromtimestamp(self.stock_dates[end_index]))
                    self.logger.debug("Stock from: %s" % datetime.datetime.fromtimestamp(self.stock_dates[0]))
                    self.logger.debug("Stock to: %s" % datetime.datetime.fromtimestamp(self.stock_dates[self.stock_dates.__len__()-1]))

                if self._show_plot:
                    self._plot.plot_continue([[self.stock_dates[start_index], target_price], [self.stock_dates[end_index], target_price]])

                for index in range(start_index, end_index):
                    self.logger.debug("Stock date of consideration: %s" % datetime.datetime.fromtimestamp(self.stock_dates[index]))
                    stock_price_change = stock_price_change + round((self.stock_closes[index-1] - self.stock_closes[index])/self.stock_closes[index-1], 4)

                for index in range(start_market_index, end_market_index):
                    self.logger.debug("Market date of consideration: %s" % datetime.datetime.fromtimestamp(self.market_dates[index]))
                    market_price_change = market_price_change + round((self.market_closes[index-1] - self.market_closes[index])/self.market_closes[index-1], 4)

                measure = measure + abs(stock_price_change - market_price_change*self.beta)
            except StopIteration:
                """Happens, then stock data is newer than the target data"""
                measure = 0

            self.logger.debug("Beta measure: %s " % self.beta)
            self.logger.debug("Market price change: %s" % market_price_change)
            self.logger.debug("Stock price change: %s" % stock_price_change)
            self.logger.debug("Stock price should have change: %s" % float(market_price_change*self.beta))
            self.logger.debug("Measure: %s" % abs(stock_price_change - market_price_change*self.beta))

            results.append(measure)

        result = round(float(sum(results))*100, 2)

        self.logger.debug("Impact to the market measure")
        self.logger.debug("Results: %s" % results)
        self.logger.debug("Return result: %s" % result)

        return result

    def reach_time(self):
        """
        Reach time measure
        """
        self.logger.debug("Reach time")
        results = []

        if self._show_plot:
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['high']] for i in range(0, self.stock_data.__len__())], 'g')
            self._plot.plot_continue([[self.stock_data[i]['date'], self.stock_data[i]['low']] for i in range(0, self.stock_data.__len__())], 'b')

        for target_entry in self.local_target_data:
            measure = 0
            target_date = target_entry[0]
            target_price = target_entry[1]
            try:
                start_index = next(i for i, x in enumerate(self.stock_dates) if x == target_date)
                end_index = start_index+249

                if end_index >= self.stock_dates.__len__():
                    end_index = self.stock_dates.__len__()-1

                if utils.DEBUG:
                    self.logger.debug("Start index: %s" % start_index)
                    self.logger.debug("End Index: %s" % end_index)
                    self.logger.debug("From: %s" % datetime.datetime.fromtimestamp(self.stock_dates[start_index]))
                    self.logger.debug("To: %s" % datetime.datetime.fromtimestamp(self.stock_dates[end_index]))
                    self.logger.debug("Stock from: %s" % datetime.datetime.fromtimestamp(self.stock_dates[0]))
                    self.logger.debug("Stock to: %s" % datetime.datetime.fromtimestamp(self.stock_dates[-1]))

                if self._show_plot:
                    self._plot.plot_continue([[self.stock_dates[start_index], target_price], [self.stock_dates[end_index], target_price]], 'b')

                for j in range(start_index, end_index):
                    if self.stock_highs[j] >= target_price and self.stock_highs[j-1] < target_price and measure is 0:
                        if utils.DEBUG:
                            self.logger.debug("Bump")
                            self.logger.debug("Target price: %d" % target_price)
                            self.logger.debug("Stock high %d %d" % (
                                self.stock_highs[j-1],
                                self.stock_highs[j]
                            ))
                        measure = j-start_index
                    elif self.stock_lows[j] >= target_price and self.stock_lows[j-1] < target_price and measure is 0:
                        if utils.DEBUG:
                            self.logger.debug("Bump")
                            self.logger.debug("Target price: %d" % target_price)
                            self.logger.debug("Low high %d %d" % (
                                self.stock_lows[j-1],
                                self.stock_lows[j]
                            ))
                        measure = j-start_index
                    elif self.stock_highs[j] <= target_price and self.stock_highs[j-1] > target_price and measure is 0:
                        if utils.DEBUG:
                            self.logger.debug("Bump")
                            self.logger.debug("Target price: %d" % target_price)
                            self.logger.debug("Stock high %d %d" % (
                                self.stock_highs[j-1],
                                self.stock_highs[j]
                            ))
                        measure = j-start_index
                    elif self.stock_lows[j] <= target_price and self.stock_lows[j-1] > target_price and measure is 0:
                        if utils.DEBUG:
                            self.logger.debug("Bump")
                            self.logger.debug("Target price: %d" % target_price)
                            self.logger.debug("Low high %d %d" % (
                                self.stock_lows[j-1],
                                self.stock_lows[j]
                            ))
                        measure = j-start_index

                if measure is not 0:
                    results.append(float(measure)-1)
            except StopIteration:
                self.logger.debug("Stopped iteration on %s %s" % (
                    datetime.datetime.fromtimestamp(target_date),
                    target_price
                ))
                self.logger.debug("Stock dates from %s to %s " % (
                    datetime.datetime.fromtimestamp(self.stock_dates[0]),
                    datetime.datetime.fromtimestamp(self.stock_dates[-1])
                ))
                # results.append(float(0))

        try:
            result = float(sum(results)/len(results))
        except ZeroDivisionError:
            result = 0

        self.logger.debug("Reach time measure")
        self.logger.debug("Results: %s" % results)
        self.logger.debug("Return result: %s" % result)

        return round(result, 2)
