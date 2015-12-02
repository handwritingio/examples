#!/usr/bin/env python
"""This script simply renders a message as a pdf and saves it to a file
(out.pdf) in the working directory
"""

import base64
import urllib
import urllib2

BASE_URL = "https://api.handwriting.io"
API_TOKEN = "<YOUR TOKEN>"
API_SECRET = "<YOUR SECRET>"
OUT_FILE = "out.pdf"

# this is the message we will turn into handwriting. It supports most
# white-space characters such as newline (\n) and tab (\t) as well as
# regular spaces
message_to_render = "Hey man!\n\n\tI love handwriting!\n\nLove,\n\tSomeone"

# now encode the params to go in the URL
params = urllib.urlencode({
  'text': message_to_render,
  'handwriting_id': '31SAZEF000DX', # find more ids at /handwritings
  'handwriting_size': '15pt',
  'height': '2in',
  'width': '4in'
})

# this is the actual rendering request for a PDF.
url = BASE_URL + '/render/pdf?' + params
req = urllib2.Request(url)

# now add our auth header
base64string = base64.b64encode('%s:%s' % (API_TOKEN, API_SECRET))
req.add_header("Authorization", "Basic %s" % base64string)

# make the request
resp = urllib2.urlopen(req)

# save the response
with open(OUT_FILE, 'wb') as f:
  for chunk in resp:
    f.write(chunk)
print "results written to %s" % OUT_FILE
