#!/usr/bin/env python
import csv
import multiprocessing
import pprint
import random
import subprocess
import sys
import tempfile
from collections import Counter

import pypb
import requests
from pdfrw import PdfReader, PdfWriter, PageMerge

API_TOKEN = "ARMGYAP2S4MYA6WC"
API_SECRET = "SR3VNCE7F5BDJ22A"

# 72 points == 1 inch
CARD_W_POINTS = 7 * 72
CARD_H_POINTS = 5 * 72
TMP_DIR = "./tmp"
HANDWRITING_ID ="5WGWVXQG00WM"

MESSAGE_TO_RENDER = """Hi Dave!

  I Hope you're enjoying my 3-DVD box set of banned dance moves! Never stop dancing!

Sincerely,
    Cynthia "Bold Moves" Smith
"""


def render_api(params):
  """This call renders a PDF according to the passed in params dict,
  saves the resulting PDF as a temporary file and returns the filename
  """
  r = requests.get("https://api.handwriting.io/render/pdf",
      auth=(API_TOKEN, API_SECRET),
      params=params,
    )
  r.raise_for_status()
  # mktemp, return filename
  with tempfile.NamedTemporaryFile(suffix=".pdf", prefix="render-",
      dir=TMP_DIR, delete=False) as f:
    f.write(r.content)
  return f.name


def render_handwritten_msg(hw_id, msg):
  """Render a given messages (msg) in a handwriting_id
  other params are hard coded for brevity
  """
  params = {
    'text': msg,
    'handwriting_id': hw_id,
    'handwriting_size': '14pt',
    'handwriting_color': "(1.0,0.5,0.0,0.2)", #blue
    'line_spacing': 1.6,
    'height': '3in',
    'width': '5in'
  }
  return render_api(params)


def move_pdf(infile, width, height, offset_x, offset_y):
  """Moves a pdf by creating a new PDF of dimensions `width` and `height`,
  then moving `infile` to a new offset_x, offset_y both of which should
  be passed as integers in points.

  NOTE: the Y-axis grows from bottom to top, not top to bottom.
  The X-axis grows from left to right.

  infile (string) path to PDF to move
  width (int) width of new PDF in points
  heigh (int) height of new PDF in points
  offset_x (int) how far to move the existing PDF on the X-axis
    in relation to the new file's origin (bottom-left)
  offset_y (int) how far to move the existing PDF on the Y-axis
    in relation to the new file's origin (bottom-left)

  Example:
    You have a file `render.pdf` that is 3inches tall by 5inches wide. You want
    to end up with the same image but centered on a 5x7" card. You would call
    this function like so

    moved = move_pdf('render.pdf', 7*72, 5*72, 72, 72)

    `moved` would now contain the filename of the temporary file containing the
    5x7" card.
  """
  with tempfile.NamedTemporaryFile(suffix=".pdf", prefix="moved-",
      dir=TMP_DIR, delete=False) as f:
    try:
      subprocess.check_call(
          "gs -q -sDEVICE=pdfwrite "
          "-sOutputFile=- " +
          "-dBATCH -dNOPAUSE -dFIXEDMEDIA "
          "-dDEVICEWIDTHPOINTS=%s " % width +
          "-dDEVICEHEIGHTPOINTS=%s " % height +
          "-c '<</PageOffset [%s %s]>>setpagedevice' " % (offset_x, offset_y) +
          "-f %s" % infile,
          stdout=f,
          stderr=open('/dev/null', 'w'),
          shell=True)
    except subprocess.CalledProcessError as e:
      print "subprocess error"
      print e.returncode
      print e.message
      print e.output
  return f.name


def make_card():
  """Render a message via the API, recenter the rendered message, then composite
  the render on top of an existing template
  """
  # render the message
  unmoved_render = render_handwritten_msg(HANDWRITING_ID, MESSAGE_TO_RENDER)
  # move the render to the right spot on the card
  moved_render = move_pdf(unmoved_render, CARD_W_POINTS, CARD_H_POINTS, 72,
      0.75 * 72)

  # wrap the render and the template files with pdfrw
  template_pdf = PdfReader('template.pdf')
  main_msg_pdf = PdfReader(moved_render)

  # set up our render as a "stamp" to put on the template
  stamp_main = PageMerge().add(main_msg_pdf.pages[0])[0]
  for page in template_pdf.pages:
    pm = PageMerge(page)
    pm.add(stamp_main)
    pm.render()

  PdfWriter().write('out.pdf', template_pdf)

if __name__ == "__main__":
  make_card()
