Example 1
===============

This example demonstrates reading a CSV file, and generating a
custom message as a PDF for each row and downloading it to a
directory.  It requires a valid API token pair, which can be created
for free at https://handwriting.io

After you have your token pair simply find the following two lines in
 `example003.py`

    API_TOKEN = "<YOUR TOKEN>"
    API_SECRET = "<YOUR SECRET>"

And change them to your token and secret. Be sure to keep the quotes,
and don't include any spaces.

This script has a few command line options, to see them run it
without arguments or with `-h` or `--help`

    usage: example003.py [-h] [-i ID] [-o ./out] [-v]
                         yourfile.csv [yourfile.csv ...]

    renders a handwritten pdf for each person in the input file

    positional arguments:
      yourfile.csv          the file(s) to process as input. These should be CSVs
                            in the same format as fakepeople.csv found in the
                            parent directory

    optional arguments:
      -h, --help            show this help message and exit
      -i ID, --handwriting-id ID
                            which handwriting style to use, by ID. IDs can be
                            found by hitting the /handwritings endpoint of our API
      -o ./out, --output-dir ./out
                            the directory in which to place renders
      -v, --verbose         Set this flag to enable more verbose logging

To run this script, you'll need a folder to dump the output into
and a valid CSV file with a column called 'first' (we've provided
a sample csv in the folder above called `fakepeople.csv`)

    $ mkdir renders
    $ python example003.py somefile.csv

After it runs, look for your renders in the `renders` directory
