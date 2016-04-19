#!/usr/bin/env python
"""This script simply renders a message as a pdf and saves it to a file
(out.pdf) in the working directory.
"""

import handwritingio

API_TOKEN = "<YOUR TOKEN>"
API_SECRET = "<YOUR SECRET>"
OUT_FILE = "out.pdf"

# This is the message we will turn into handwriting. It supports most
# white-space characters such as newline (\n) and tab (\t) as well as
# regular spaces.
message_to_render = "Hey man!\n\n\tI love handwriting!\n\nLove,\n\tSomeone"

# Create a client:
hwio = handwritingio.Client(API_TOKEN, API_SECRET)

# Create the image:
pdf = hwio.render_pdf({
    'text': message_to_render,
    'handwriting_id': '31SAZEF000DX', # find more IDs by calling hwio.list_handwritings()
    'handwriting_size': '15pt',
    'height': '2in',
    'width': '4in',
})

# Save the image to a file:
with open(OUT_FILE, 'wb') as f:
  f.write(pdf)
print "results written to %s" % OUT_FILE
