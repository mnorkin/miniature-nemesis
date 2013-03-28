import database
import rest
import utils


class Analytics:
    """
    Analytic object
    """

    def collect_and_send(self, analytic=None):
        """
        Fetching analytics data to the server

        If analytic is defined -- sending the data of specific analytic
        """

        if not analytic:
            for analytic in database.get_analytics():
                analytic_data = self.collect(analytic)
                if analytic_data and not self.send(analytic_data):
                    return False
                """If there was error at any step -- return"""
            return True
            """If everything was ok -- return true"""
        else:
            """
            Get specific analytic data and parse it to the front-end
            """
            analytic_data = self.collect(analytic)
            if analytic_data and self.send(analytic_data):
                return True
                """If everything was okay -- return true"""
            else:
                return False
                """If something went wrong -- return false"""

    def collect(self, analytic=None):
        """
        Method to collect analytic data
        """
        if analytic:
            slug = utils.slugify(str(analytic))

            data = {
                'name': analytic.replace('"', ''),
                'slug': slug
            }

            return data
        else:
            return None

    def send(self, data=None):
        """
        Method to send analytic data
        """

        if data:
            if rest.send("POST", "/api/analytics/", data):
                return True
            else:
                if rest.send("PUT", "/api/analytics/", data):
                    return True
                else:
                    # Literally, something should be wrong on front-end side,
                    # if this does not work
                    return False
        else:
            return False
