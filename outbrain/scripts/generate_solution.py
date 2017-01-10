#!/usr/bin/env python

from argparse import ArgumentParser

from outbrain.csvutil.reader import csv_file_group_iter


def write_group_to_stream(examples_group, group_key, pred_field, outstream):

    sorted_examples = sorted(examples_group,
                             key=lambda e: float(getattr(e, pred_field)),
                             reverse=True)

    display_id = group_key
    outline = "%s,%s\n" % (
        display_id,
        " ".join([ex.ad_id for ex in sorted_examples])
    )
    outstream.write(outline)


if __name__ == "__main__":


    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="input", type=str, default=None, required=True,
                           help="input file")
    argparser.add_argument("-o", dest="output", type=str, default=None, required=True,
                           help="output file")
    argparser.add_argument("--pred", dest="prediction", type=str, default="sigmoid_vw",
                           help="field with prediction")

    args = argparser.parse_args()


    with open(args.output, "w") as outfile:
        outfile.write("display_id,ad_id\n")

        with open(args.input) as infile:
            group_counter = 0
            counter = 0
            for group_key, examples_group in csv_file_group_iter(
                infile,
                group_field="display_id"
                ):

                write_group_to_stream(examples_group, group_key, args.prediction, outfile)
                counter += len(examples_group)
                group_counter += 1

            print "%d examples processed, %d groups in total" % (counter, group_counter)




