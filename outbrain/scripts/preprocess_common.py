#!/usr/bin/env python

from argparse import ArgumentParser

from outbrain.preprocess.common import ReduceStreamer
from outbrain.preprocess.mapper import *


# Sorry for hardcode, we are running out of time!
JOIN_FILES=[
    ("documents_categories.csv", "document_id", "category_id"),
    ("documents_entities.csv", "document_id", "entity_id"),
    ("documents_topics", "document_id", "topic_id"),
]

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

    for join_file, join_key, field in JOIN_FILES:
        reducers.append(
            Join(
                join_file=join_file,
                join_key=[join_key],
                fields=[field]
                )
        )

    streamer = ReduceStreamer(
        reducers=reducers,
        group_field="display_id",
        infilename=args.input,
        outfilename=args.output
    )
    streamer()
