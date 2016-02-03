Example 4: PDF Compositing
==========================

The example covers the use case of having pre-existing stationary,
and wanting to render handwriting on top of it for printing.

This example requires 2 PDF libraries to work
  - `pdfrw` installed via pip, this allows writing new PDFs
  - `ghostscript` is used to reformat renders and move them.

We start with a run of the mill template, a 5x7" card with a company logo

[Basic Template](template.pdf)

Run our script, then you end up with something like this

[Final Composition](example_output.pdf)


To run this example:
  - Make a new virtualenv (optional)
  - Activate the virtualenv (optional)
  - install python dependencies with `pip install -r requirements.txt`
  - install ghostscript (http://ghostscript.com/download/gsdnld.html)
  this can easily be installed via homebrew on OSX or most package
  managers on Linux distros
  - edit the `render_and_compose.py` script to change variables
  (your API credentials, handwriting style, size, color, etc...)
  - run `python ./render_and_compose.py`
  - open out.png

