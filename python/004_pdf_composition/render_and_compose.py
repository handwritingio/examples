#!/usr/bin/env python
from subprocess import Popen, PIPE

import requests
from pdfrw import PdfReader, PdfWriter, PageMerge

# Get your tokens at https://handwriting.io/account/tokens
API_TOKEN = "YOUR_TOKEN"
API_SECRET = "YOUR_SECRET"

# 72 points == 1 inch
CARD_W_POINTS = 7 * 72
CARD_H_POINTS = 5 * 72
OFFSET_X_POINTS = 72
OFFSET_Y_POINTS = 1.25 * 72
HANDWRITING_ID ="5WGWVXQG00WM"

MESSAGE_TO_RENDER = """Hi Dave!

  I Hope you're enjoying my 3-DVD box set of banned dance moves! Never stop dancing!

Sincerely,
    Cynthia "Bold Moves" Smith
"""


def render_api(params):
  """This call renders a PDF according to the passed in params dict,
  returning the PDF file data upon success.
  """
  r = requests.get("https://api.handwriting.io/render/pdf",
      auth=(API_TOKEN, API_SECRET),
      params=params,
    )
  r.raise_for_status()
  return r.content


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
    'width': '%spt' % (CARD_W_POINTS - 2 * OFFSET_X_POINTS),
    'height': '%spt' % (CARD_H_POINTS - 2 * OFFSET_Y_POINTS),
  }
  return render_api(params)


def make_card():
  """Render a message via the API, then composite the render on top of an
  existing template, at the correct position.
  """
  # render the message
  message_render = render_handwritten_msg(HANDWRITING_ID, MESSAGE_TO_RENDER)

  # wrap the render and the template files with pdfrw
  template_pdf = PdfReader('template.pdf')
  message_pdf = PdfReader(fdata=message_render)

  # set up our render as a "stamp" to put on the template
  stamp = PageMerge().add(message_pdf.pages[0])[0]
  # x is the distance from the left edge of the template to the left edge of the stamp:
  stamp.x = OFFSET_X_POINTS
  # y is the distance from the bottom edge of the template to the top edge of the stamp:
  stamp.y = CARD_H_POINTS - OFFSET_Y_POINTS
  pm = PageMerge(template_pdf.pages[0])
  pm.add(stamp)
  pm.render()

  PdfWriter().write('out.pdf', template_pdf)

if __name__ == "__main__":
  make_card()
