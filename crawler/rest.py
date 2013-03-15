"""
The REST
"""
import httplib
import json

list_of_requests = ['GET', 'POST', 'PUT', 'DELETE']


def send(request, url, data):
    if any(request.upper() in s for s in list_of_requests):
        params = json.dumps(data)
        headers = {"Content-type": "application/json"}
        # conn = httplib.HTTPConnection("185.5.55.178")
        conn = httplib.HTTPConnection("localhost:8000")
        print "Request: ", request
        print "Params: ", params
        print "Headers: ", headers
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        print response.read()
        print response.status, response.reason
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
