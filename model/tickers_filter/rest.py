"""
The REST
"""
import httplib
import json

list_of_requests = ['GET', 'POST', 'PUT', 'DELETE']


def send(request, url, data):
    """
    Sending the data
    """
    if any(request.upper() in s for s in list_of_requests):
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        conn = httplib.HTTPConnection('localhost:8000')
        # conn = httplib.HTTPConnection('dev4.baklazanas.lt')
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
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
            return False
    else:
        return False
