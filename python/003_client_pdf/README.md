Example 3: Using the Handwriting.io Client
===============================================

This example demonstrates very simple API access to render a PDF of a message.
It requires a valid API token pair, which can be created for free at
https://handwriting.io.

While the previous examples used the `requests` library to call the API, this
example uses our official Python client:
https://github.com/handwritingio/python-client

After you have your token pair simply find the following two lines in
`render_pdf.py`

    API_TOKEN = "<YOUR TOKEN>"
    API_SECRET = "<YOUR SECRET>"

And change them to your token and secret. Be sure to keep the quotes, and don't
include any spaces.

Then, to run this script, simply invoke it:

    $ python render_pdf.py

After it runs look for a file called `out.pdf` in the working directory and open
it.
