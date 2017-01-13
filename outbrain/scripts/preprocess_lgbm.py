#!/usr/bin/env python

from argparse import ArgumentParser

from outbrain.preprocess.common import ReduceStreamer
from outbrain.preprocess.mapper import *


if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="input", type=str, default=None,
                           help="input file")
    argparser.add_argument("-o", dest="output", type=str, default=None,
                           help="output file")


    args = argparser.parse_args()


    reducers = [
        CountAdsInBlock(),
        ProcessTimestamp("timestamp"),
        ProcessGeoData("geo_location")
        ]


    streamer = ReduceStreamer(
        reducers=reducers,
        group_field="display_id",
        infilename=args.input,
        outfilename=args.output
    )
    streamer()
