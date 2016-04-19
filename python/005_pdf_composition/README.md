Example 5: PDF Composition
=============================

The example covers the use case of having pre-existing stationary, and wanting
to render handwriting on top of it for printing.

This example requires the `pdfrw` and `handwritingio` libraries to work. Install
these via pip.

We start with a run of the mill template, a 5x7" card with a company logo:

[Basic Template](template.pdf)

Run our script, then you end up with something like this:

[Final Composition](example_output.pdf)


To run this example:
- Make a new virtualenv (optional)
- Activate the virtualenv (optional)
- Install python dependencies with `pip install -r requirements.txt`
- Edit the `render_and_compose.py` script to change variables
  (your API credentials, handwriting style, size, color, etc...)
- Run `python ./render_and_compose.py`
- Open `out.png`
