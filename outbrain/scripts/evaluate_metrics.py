#!/usr/bin/env python

from argparse import ArgumentParser

from outbrain.metrics.common import compute_metrics



if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="infile", default=None, help="input filename")
    argparser.add_argument("--click", dest="click_field", default="clicked",
                           help="column with class label (click)")
    argparser.add_argument("--pred", dest="pred_field", default="sigmoid_VW",
                           help="column with predictions (click probability)")
    argparser.add_argument("-g", dest="group_field", default=None,
                           help="column with group field")


    args = argparser.parse_args()

    config = {
        "class_field": args.click_field,
        "predictions_field": args.pred_field,
        "group_field": args.group_field
    }

    metrics = compute_metrics(args.infile, config)
    print metrics
