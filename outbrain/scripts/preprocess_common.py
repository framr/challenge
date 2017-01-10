#!/usr/bin/env python

from argparse import ArgumentParser

from outbrain.preprocess.common import ReduceStreamer
from outbrain.preprocess.mapper import *


# Sorry for hardcoding, we are running out of time!
JOIN_CONF=[
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/ad_documents_categories_gt0.5.csv", "ad_category05_id", "ad_document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/ad_documents_categories_gt0.9.csv", "ad_category09_id", "ad_document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/ad_documents_entities_gt0.9.csv", "ad_entity09_id", "ad_document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/ad_documents_entities_gt0.5.csv", "ad_entity05_id", "ad_document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/ad_documents_topics_gt0.05.csv", "ad_topic005_id", "ad_document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/ad_documents_topics_gt0.1.csv", "ad_topic01_id", "ad_document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/documents_categories_gt0.5.csv", "category05_id", "document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/documents_categories_gt0.9.csv", "category09_id", "document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/documents_entities_gt0.9.csv", "entity09_id", "document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/documents_entities_gt0.5.csv", "entity05_id", "document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/documents_topics_gt0.05.csv", "topic005_id", "document_id"),
    ("/home/fram/kaggle/outbrain/playground/input/documents_meta/documents_topics_gt0.1.csv", "topic01_id", "document_id")
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


    for join_file, field, join_key in JOIN_CONF:
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
