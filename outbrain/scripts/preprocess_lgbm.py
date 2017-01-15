#!/usr/bin/env python

import yaml
from argparse import ArgumentParser

from outbrain.preprocess.common import ReduceStreamer
from outbrain.preprocess.mapper_fast import *

CTR0 = 1.0 / 5.0

# Sorry for hardcoding, we are running out of time!
JOIN_CONF=[
#    ("/mnt/diomed/home/fram/kaggle/outbrain/playground/input/geomapping/geomapping_country", "geo_country_fid", "geo_country"),
#    ("/mnt/diomed/home/fram/kaggle/outbrain/playground/input/geomapping/geomapping_state", "geo_state_fid", "geo_state"),
#    ("/mnt/diomed/home/fram/kaggle/outbrain/playground/input/geomapping/geomapping_dma", "geo_dma_fid", "geo_dma")
    ("/home/fram/kaggle/outbrain/playground/input/geomapping/geomapping_country", "geo_country_fid", "geo_country"),
    ("/home/fram/kaggle/outbrain/playground/input/geomapping/geomapping_state", "geo_state_fid", "geo_state"),
    ("/home/fram/kaggle/outbrain/playground/input/geomapping/geomapping_dma", "geo_dma_fid", "geo_dma")

]



if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="input", type=str, default=None,
                           help="input file")
    argparser.add_argument("-o", dest="output", type=str, default=None,
                           help="output file")
    args = argparser.add_argument("--task", dest="task", type=str, default=None, required=True,
                                help="yml config for stats keys")

    args = argparser.parse_args()


    task = yaml.load(open(args.task).read())
    stat_conf = yaml.load(open(task["stat_conf"]).read())

    reducers = [
        CountAdsInBlock(),
        ProcessTimestamp("timestamp"),
        ProcessGeoData("geo_location"),
        ComputeStatFactors(
            stat_conf["stat_factors"]["keys"],
            smooth_conf=stat_conf["stat_factors"]["smooth_conf"],
            ctr0=CTR0
        ),
        ComputeStatFactors(
            stat_conf["online_stat_factors"]["keys"],
            smooth_conf=stat_conf["online_stat_factors"]["smooth_conf"],
            ctr0=CTR0,
            online=True
        ),
        ComputeRelCTR()
    ]

    for join_file, field, join_key in JOIN_CONF:
        reducers.append(
            Join(
                join_file=join_file,
                join_key=[join_key],
                fields=[field],
                missing_key="-1"
                )
        )

    reducers.append(
        ProcessMissing()
    )

    streamer = ReduceStreamer(
        reducers=reducers,
        group_field="display_id",
        infilename=args.input,
        outfilename=args.output
    )

    streamer()
