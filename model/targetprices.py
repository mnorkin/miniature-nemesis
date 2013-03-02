"""
The Target Prices
"""

import rest


class TargetPrices:

    def send(self, data=None):

        if data:

            if rest.send("POST", "/api/target_prices/", data):
                """Trying to send POST"""
                return True
            else:
                if rest.send("PUT", "/api/target_prices/", data):
                    return True
                else:
                    return False
        else:
            return False
