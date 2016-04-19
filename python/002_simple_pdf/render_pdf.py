#!/usr/bin/env python
"""This script simply renders a message as a pdf and saves it to a file
(out.pdf) in the working directory
"""

import requests

BASE_URL = "https://api.handwriting.io"
API_TOKEN = "<YOUR TOKEN>"
API_SECRET = "<YOUR SECRET>"
OUT_FILE = "out.pdf"

# this is the message we will turn into handwriting. It supports most
# white-space characters such as newline (\n) and tab (\t) as well as
# regular spaces
message_to_render = "Hey man!\n\n\tI love handwriting!\n\nLove,\n\tSomeone"

# this is the actual rendering request for a PDF.
r = requests.get("%s%s" % (BASE_URL, "/render/pdf"),
    auth=(API_TOKEN, API_SECRET),
    params={
      'text': message_to_render,
      'handwriting_id': '31SAZEF000DX', # find more ids at /handwritings
      'handwriting_size': '15pt',
      'height': '2in',
      'width': '4in'
    },
    stream=True # to prevent in-memory buffering of the image
  )
r.raise_for_status()
with open(OUT_FILE, 'wb') as f:
  for chunk in r.iter_content(chunk_size=4096):
    f.write(chunk)
print "results written to %s" % OUT_FILE
