Example 2
===============

This example demonstrates very simple API access to render a PDF of a message.
It requires a valid API token pair, which can be created for free at
https://handwriting.io. The only difference between this example and the first one
is that this one uses the popluar `requests` library. The rest of our examples will
make use of this library. Installation info can be found at 
http://docs.python-requests.org/en/latest/

After you have your token pair simply find the following two lines in
 `example002.py`

    API_TOKEN = "<YOUR TOKEN>"
    API_SECRET = "<YOUR SECRET>"

And change them to your token and secret. Be sure to keep the quotes, and don't include
any spaces.

Then, to run this script, simply invoke it...

    $ python example002.py

After it runs look for a file called `out.pdf` in the working directory and open it
