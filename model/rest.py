"""
The REST
"""
import httplib
import json
import utils
import logging
import os
from datetime import date

list_of_requests = ['GET', 'POST', 'PUT', 'DELETE']

logging_file = os.path.dirname(os.path.realpath(__file__)) + '/logs/' + date.today().isoformat() + '.log'
logging_level = logging.DEBUG

logging.basicConfig(
    filename=logging_file,
    level=logging_level, format='%(asctime)s %(message)s')


def send(request, url, data):
    if any(request.upper() in s for s in list_of_requests):
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        # conn = httplib.HTTPConnection("185.5.55.178")
        conn = httplib.HTTPConnection("localhost:8000")
        logging.debug("Request: %s" % request)
        logging.debug("Params: %s" % params)
        logging.debug("Headers: %s " % headers)
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        logging.debug("Response status: %s" % response.status)
        logging.debug("Response reason: %s" % response.reason)
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
            logging.debug("Not expected response status: %s, failing" % response.status)
            return False
    else:
        if utils.DEBUG:
            logging.debug("Invalid request: %s" % request)
        return False
