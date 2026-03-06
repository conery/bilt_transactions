#
# bilt_transactions
#
# A command line application, written in Python, that extracts transactions
# from a MHTML file downloaded from bilt.com and prints them in CSV format.
#

import argparse
import csv
import logging
from pathlib import Path
import sys

from .parser import parse_file, extract_paragraphs
from .util import setup_logging, console

def init_cli():
    '''
    Read the command line arguments, return them in a namespace object
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='F', help='input file name')
    parser.add_argument('--log', metavar='X', choices=['quiet','info','debug'], default='quiet')
    parser.add_argument('--tokens', action='store_true')

    args = parser.parse_args()

    if len(sys.argv) == 0:
        args.print_usage()
        exit(1)

    return args

def print_tokens(fn:str):
    for p in extract_paragraphs(fn):
        console.print(p)

def csv_transactions(fn: str):
    '''
    Verify the input file exists, call the parser, return the set
    of dictionaries made by the parser.

    Arguments:
        fn:  the name of the input file
    '''
    p = Path(fn)
    if not p.is_file():
        logging.error(f'file does not exist: {fn}')
        exit(1)

    return parse_file(fn)

def write_records(recs):
    '''
    Convert each dictionary in the list into a CSV record, write the
    records to stdout.

    Arguments:
        recs: a list of dictionaries returned by the parser
    '''
    cols = list(recs[0].keys())
    writer = csv.DictWriter(sys.stdout, fieldnames=cols)
    writer.writeheader()
    for rec in recs:
        writer.writerow(rec)

def main():
    args = init_cli()
    setup_logging(args.log)
    logging.info('bilt_transactions')
    if args.tokens:
        print_tokens(args.file)
    else:
        recs = csv_transactions(args.file)
        logging.info(f'{len(recs)} transactions')
        write_records(recs)



