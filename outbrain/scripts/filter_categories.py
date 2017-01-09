#!/usr/bin/env python

from argparse import ArgumentParser

from outbrain.csvutil.util import get_column_index_mapping


def filter_file(infilename, outfilename, filter_field="confidence_level",
                min_threshold=0.0, separator=","):

    with open(infilename) as infile:
        with open(outfilename, "w") as outfile:

            header = infile.readline().strip()
            filter_index = get_column_index_mapping(header.split(separator))[filter_field]

            outfile.write("%s\n" % header)
            for line in infile:
                field_value = float(line.strip().split(separator)[filter_index])
                if field_value < min_threshold:
                    continue

                outfile.write(line)



if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="infile", type=str, default=None, help="input file", required=True)
    argparser.add_argument("-o", dest="outfile", type=str, default=None, help="output file", required=True)
    argparser.add_argument("--filter-field", dest="filter_field", type=str, default="confidence_level",
                           help="field used for filtering")
    argparser.add_argument("--min", dest="min_threshold", type=float, default=None, help="min threshold",
                           required=True)
    args = argparser.parse_args()

    filter_file(args.infile, args.outfile, min_threshold=args.min_threshold, filter_field=args.filter_field)


