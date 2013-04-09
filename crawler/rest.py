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
        # conn = httplib.HTTPConnection("cra.baklazanas.lt")
        print "Request: ", request
        print "Params: ", params
        print "Headers: ", headers
        conn.request(request.upper(), url, params, headers)
        response = conn.getresponse()
        print response.read()
        print response.status, response.reason
        conn.close()
        # ALL_OK
        if response.status == 200 and request.upper() == 'GET':
            return True
        # CREATED
        elif response.status == 201 and request.upper() == 'POST':
            return True
        # ALL_OK
        elif response.status == 200 and request.upper() == 'PUT':
            return True
        # DELETED
        elif response.status == 204 and request.upper() == 'DELETE':
            return True
        else:
            return False
    else:
        return False
