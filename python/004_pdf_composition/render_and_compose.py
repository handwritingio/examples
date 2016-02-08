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


def move_pdf(original, width, height, offset_x, offset_y):
  """Moves a pdf by creating a new PDF of dimensions `width` and `height`,
  then moving `original` to a new offset_x, offset_y both of which should
  be passed as integers in points.

  NOTE: the Y-axis grows from bottom to top, not top to bottom.
  The X-axis grows from left to right.

  original (string) original PDF data
  width (int) width of new PDF in points
  heigh (int) height of new PDF in points
  offset_x (int) how far to move the existing PDF on the X-axis
    in relation to the new file's origin (bottom-left)
  offset_y (int) how far to move the existing PDF on the Y-axis
    in relation to the new file's origin (bottom-left)

  Example:
    You have a file `render.pdf` that is 3inches tall by 5inches wide. You want
    to end up with the same image but centered on a 5x7in card. You would call
    this function like so:

    with open('render.pdf', 'rb') as f:
      pdf_data = f.read()
    moved = move_pdf(pdf_data, 7*72, 5*72, 72, 72)
    with open('moved.pdf', 'wb') as f:
      f.write(moved)

    `moved.pdf` would now contain the 5x7in card.
  """
  cmd = ["gs", "-q", "-sDEVICE=pdfwrite",
      "-sOutputFile=-",
      "-dBATCH", "-dNOPAUSE", "-dFIXEDMEDIA",
      "-dDEVICEWIDTHPOINTS=%s" % width,
      "-dDEVICEHEIGHTPOINTS=%s" % height,
      "-c",
      "<</PageOffset [%s %s]>>setpagedevice" % (offset_x, offset_y),
      "-"]
  p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE)
  out, err = p.communicate(original)

  if p.returncode != 0:
    print 'Error calling ghostscript:'
    print err

  return out


def make_card():
  """Render a message via the API, recenter the rendered message, then composite
  the render on top of an existing template
  """
  # render the message
  unmoved_render = render_handwritten_msg(HANDWRITING_ID, MESSAGE_TO_RENDER)
  # move the render to the right spot on the card
  moved_render = move_pdf(unmoved_render, CARD_W_POINTS, CARD_H_POINTS,
    OFFSET_X_POINTS, OFFSET_Y_POINTS)

  # wrap the render and the template files with pdfrw
  template_pdf = PdfReader('template.pdf')
  render_pdf = PdfReader(fdata=moved_render)

  # set up our render as a "stamp" to put on the template
  stamp = PageMerge().add(render_pdf.pages[0])[0]
  pm = PageMerge(template_pdf.pages[0])
  pm.add(stamp)
  pm.render()

  PdfWriter().write('out.pdf', template_pdf)

if __name__ == "__main__":
  make_card()
