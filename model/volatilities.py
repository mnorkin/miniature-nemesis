from database import database
import rest
import utils


class volatilities():
    """
    Volatility calculations
    """
    def __init__(self, arg):
        super(volatilities, self).__init__()
        self.database = database()

    def collect_and_send(self, analytic=None, ticker=None):
        pass

    def collect(self, analytic=None, ticker=None):
        pass

    def send(self, data=None):
        if data:
            if rest.send("POST", "/api/volatility/", data):
                return True
            else:
                if rest.send("PUT", "/api/volatility/", data):
                    return True
                else:
                    return False
        else:
            return False
