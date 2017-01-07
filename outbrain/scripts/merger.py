#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from subprocess import Popen, PIPE, check_call
from tempfile import NamedTemporaryFile

import csv

CLICKED_FIELD = "clicked"

def columns_to_add_to_test(filename, separator=","):
    header = None
    with open(filename) as infile:
        header = infile.readline().strip().split(separator)

    add_fields = None
    if CLICKED_FIELD in header:
        add_fields = [["is_train", 0]]
    else:
        add_fields = [[CLICKED_FIELD, 0], ["is_train", 0]]

    return add_fields

def add_columns_and_strip_header(infilename, outfilename, add_columns=None, separator=","):
    """
    Extend csv file with new columns and remove header
    Args:
        infilename:
        outfilename:
        add_columns:
        separator:

    Returns:

    """
    if not add_columns:
        return None

    with open(infilename) as infile:
        with open(outfilename, "w") as outfile:
            header = infile.readline().strip().split(separator)

            column_names, column_values = zip(*add_columns)
            column_names = list(column_names)
            column_values = list(column_values)

#            print add_columns
#            print column_names, column_values
            header.extend(column_names)

            writer = csv.writer(outfile)
            for row in csv.reader(infile):
                writer.writerow(row + column_values)
                #print row + column_values

    return header


if __name__ == '__main__':


    argparser = ArgumentParser()
    argparser.add_argument("--train", dest="train", type=str, default=None, help="first file", required=True)
    argparser.add_argument("--test", dest="test", type=str, default=None, help="second file", required=True)
    argparser.add_argument("--out", dest="output", type=str, default=None, help="output file", required=True)
    argparser.add_argument("--key", dest="sort_column", type=str, default=None,
                           help="column used for sorting", required=True)
    argparser.add_argument("--sort-args", dest="sort_args", type=str, default="-g --stable",
                           help="additional sort arguments")
    argparser.add_argument("--separator", dest="separator", type=str, default=",",
                           help="csv file separator")

    args = argparser.parse_args()


    with NamedTemporaryFile() as train:
        with NamedTemporaryFile() as test:

            # We first convert train and test to common format with additional column identifying
            # which file example belongs to.
            # We also strip headers for unix sort to work properly
            train_header = add_columns_and_strip_header(
                args.train, train.name, add_columns=[["is_train", "1"]],
                separator=args.separator
            )

            add_columns_for_test = columns_to_add_to_test(args.test)
            test_header = add_columns_and_strip_header(
                args.test, test.name, add_columns=add_columns_for_test,
                separator=args.separator
            )

            print "Resulting train header %s" % train_header
            print "Resulting test header %s" % test_header


            if train_header != test_header:
                raise ValueError("headers mismatch %s for train vs %s for test"
                                 % (train_header, test_header))

            columns_mapping = dict((column, index + 1) for index, column in enumerate(train_header))
            sort_column_index = columns_mapping[args.sort_column]

            # Write header to output file
            with open(args.output, "w") as outfile:
                outfile.write("%s\n" % args.separator.join(train_header))


            sort_cmd = 'sort %s -k %d,%d --field-separator="%s" >> %s' % (
                args.sort_args, sort_column_index, sort_column_index, args.separator, args.output)
            print "command for sorting: %s" % sort_cmd

            # Now merge preprocessed train and test and run unix sort on it
            proc1 = Popen("cat %s %s" % (train.name, test.name), stdout=PIPE, shell=True)
            proc2 = Popen(sort_cmd, stdin=proc1.stdout, shell=True)

            proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits. WTF???
            stdout, stderr = proc2.communicate()

            print stdout
            print stderr



