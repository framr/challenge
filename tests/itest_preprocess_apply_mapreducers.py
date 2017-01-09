#!/usr/bin/env python

from outbrain.preprocess.common import ReduceStreamer
from outbrain.preprocess.mapper import *



if __name__ == "__main__":

    infile = "./fixtures/fixture_log_for_preprocess_apply_mappers1.csv"
    outfile = "./fixtures/fixture_log_for_preprocess_apply_mappers1.csv_preprocessed"
    join_file = "./fixtures/fixture_document_categories_for_preprocess_apply_mappers1.csv"

    reducers = [
        CountAdsInBlock(),
        ProcessTimestamp("timestamp"),
        ProcessGeoData("geo_location"),
        Join(
            join_file=join_file,
            join_key=["document_id"],
            fields=["category_id", "entity_id"]
        )
    ]

    streamer = ReduceStreamer(
        reducers=reducers,
        group_field="display_id",
        infilename=infile,
        outfilename=outfile
    )
    streamer()
