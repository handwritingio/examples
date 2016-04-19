#!/usr/bin/env python

import argparse
import csv
import logging
import os

import handwritingio

API_TOKEN = "<YOUR TOKEN>"
API_SECRET = "<YOUR SECRET>"

def _readable_file(path):
  """Intended for use with argparse's `type` argument. If `path` isn't a
  readable file, this will throw an error that stops argument parsing
  """
  if not os.path.isfile(path):
    raise argparse.ArgumentTypeError("path '%s' does not exist" % path)
  elif not os.access(path, os.R_OK):
    raise argparse.ArgumentTypeError("path '%s' does not allow reads" % path)
  return path


def _writable_directory(path):
  """Intended for use with argparse's `type` argument. If `path` isn't a
  writable directory, this will throw an error that stops argument parsing
  """
  if not os.path.isdir(path):
    raise argparse.ArgumentTypeError("path '%s' does not exist" % path)
  elif not os.access(path, os.W_OK):
    raise argparse.ArgumentTypeError("path '%s' does not allow writes" % path)
  return path


def render_pdf(msg, outfile):
  """This method accepts a string `msg` to render via the api, and saves
  successful downloads to the path `outfile`
  """
  log.debug("rendering to %s", outfile)
  pdf = client.render_pdf({
    'text': msg,
    'handwriting_id': args.handwriting_id,
    'handwriting_size': '14pt',
    'height': 'auto',
    'width': '3in'
  })
  with open(outfile, 'wb') as f:
    f.write(pdf)


def process_csv(filename, output_dir):
  """Opens `filename` as a csv file and then renders a custom message for each
  row as a pdf in `output_dir`
  """
  log.info("processing %s...", filename)
  with open(filename, 'rb') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
      # we're going to build a custom message for each user, using their name.
      first_name = row['first'].title()
      msg = "Hi %s,\nThanks for everything!\n\nLove,\nUs" % first_name
      outfile = os.path.join(args.output_dir, "%04d.pdf" % idx)
      try:
        render_pdf(msg, outfile)
      except handwritingio.APIError as e:
        log.error("Could not render row %04d: %s", idx, e)


if __name__ == "__main__":
  # setup the argument parser
  parser = argparse.ArgumentParser(description="renders a handwritten pdf for "
      "each person in the input file")
  parser.add_argument("inputs", metavar="yourfile.csv", nargs="+", help="the "
      "file(s) to process as input. These should be CSVs in the same format "
      "as fakepeople.csv found in the parent directory")
  parser.add_argument("-i", "--handwriting-id", metavar="ID",
      default="31SAZEF000DX", help="which handwriting style to use, by ID. IDs "
      "can be found by hitting the /handwritings endpoint of our API")
  parser.add_argument("-o", "--output-dir", metavar="./out",
      default="./renders", type=_writable_directory, help="the directory in "
      "which to place renders")
  parser.add_argument("-v", "--verbose", action="store_true", help="Set this "
      "flag to enable more verbose logging")

  # parse our args and freak out if anything looks wrong
  args = parser.parse_args()

  # setup our logging
  level = logging.INFO
  if args.verbose:
    level = logging.DEBUG
  logging.basicConfig(level=level)
  log = logging.getLogger(__name__)

  # create a client that we will reuse for each render
  client = handwritingio.Client(API_TOKEN, API_SECRET)

  # iterate over all passed in files
  for f in args.inputs:
    process_csv(f, args.output_dir)
