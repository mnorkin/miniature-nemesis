"""
The REST 
"""
import httplib, urllib
import json

list_of_requests = ['GET', 'POST', 'PUT', 'DELETE'];

def send(request, url, data):
  if any(request.upper() in s for s in list_of_requests):
    params = json.dumps(data)
    headers = {"Content-type": "application/json"}
    conn = httplib.HTTPConnection("localhost:8000")
    if utils.DEBUG:
      print params
      print headers
    conn.request(request.upper(), url, params, headers)
    response = conn.getresponse()
    if utils.DEBUG:
      print response.read()
      print response.status, response.reason
    conn.close()
    if response.status == 200 and request.upper() == 'GET': # READ
      return True
    elif response.status == 201 and request.upper() == 'POST': # CREATED
      return True
    elif response.status == 202 and request.upper() == 'PUT': # ACCEPTED
      return True
    elif response.status == 204 and request.upper() == 'DELETE': # DELETED
      return True
    else:
      if utils.DEBUG:
        print "Not expected response status: ", response.status, " failing"
      return False
  else:
    if utils.DEBUG:
      print "Invalid request: ", request
    return False