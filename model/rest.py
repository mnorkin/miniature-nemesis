"""
The REST
"""
import httplib
import json
import utils
from logger import logger
from settings import rest_url

list_of_requests = ['GET', 'POST', 'PUT', 'DELETE']

logger = logger('rest')


def send(request, url, data):
    """
    Sending the data
    """
    if any(request.upper() in s for s in list_of_requests):
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        # conn = httplib.HTTPConnection("185.5.55.178")
        conn = httplib.HTTPConnection(rest_url)
        logger.debug("Request: %s" % request)
        logger.debug("Params: %s" % params)
        logger.debug("Headers: %s " % headers)
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        logger.debug("Response status: %s" % response.status)
        logger.debug("Response reason: %s" % response.reason)
        conn.close()
        if response.status == 200 and request.upper() == 'GET':  # ALL_OK
            return True
        elif response.status == 201 and request.upper() == 'POST':  # CREATED
            return True
        elif response.status == 200 and request.upper() == 'PUT':  # ALL_OK
            return True
        elif response.status == 204 and request.upper() == 'DELETE':  # DELETED
            return True
        else:
            logger.debug("Not expected response status: %s, failing" % response.status)
            return False
    else:
        if utils.DEBUG:
            logger.debug("Invalid request: %s" % request)
        return False
