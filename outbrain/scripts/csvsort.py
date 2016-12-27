#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from subprocess import Popen, PIPE, check_call
from tempfile import NamedTemporaryFile
import csv


from outbrain.csvutil.util import get_column_indices_from_header


if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="input", type=str, default=None, help="input file", required=True)
    argparser.add_argument("-o", dest="output", type=str, default=None, help="output file", required=True)
    argparser.add_argument("--key", dest="sort_column", type=str, default=None,
                           help="column used for sorting", required=True)
    argparser.add_argument("--sort-args", dest="sort_args", type=str, default="-g",
                           help="additional sort arguments")
    argparser.add_argument("--separator", dest="separator", type=str, default=",",
                           help="csv file separator")

    args = argparser.parse_args()

    #with NamedTemporaryFile() as tmp_file:


    header = None
    with open(args.input) as infile:
        with open(args.output, "w") as outfile:
            header = infile.readline()
            outfile.write("%s" % header)



    sort_column_index = 1 + get_column_indices_from_header(
        [args.sort_column],
        header.strip().split(args.separator))[0]
    sort_cmd = 'sort %s -k %d,%d --field-separator="%s" >> %s' % (
            args.sort_args, sort_column_index, sort_column_index, args.separator, args.output)
    print "command for sorting: %s" % sort_cmd

    # Remove header
    proc1 = Popen(
        "cat %s | tail -n +2" % args.input,
        stdout=PIPE,
        shell=True
    )

    proc2 = Popen(
        sort_cmd,
        stdin=proc1.stdout,
        shell=True
    )

    proc1.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits. WTF???
    stdout, stderr = proc2.communicate()
    print stdout
    print stderr



