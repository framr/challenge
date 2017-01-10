#!/usr/bin/env python
import os
import yaml
from argparse import ArgumentParser

from outbrain.vw.formatter_fast import convert_csv2vw_fast

if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="infile", type=str, default=None, help="input file")
    argparser.add_argument("-t", dest="task", type=str, default=None, help="task file")
    argparser.add_argument("--fstats", dest="feature_stats", type=str, default=None, help="feature stats file")

    args = argparser.parse_args()

    outfile = os.path.join(os.getcwd(), "output", "profiling_vwformatter.csv")
    task = yaml.load(open(args.task).read())

    convert_csv2vw_fast(args.infile,
                   outfile,
                   task,
                   feature_stats_file=args.feature_stats
                   #feature_map_file=mbus.feature_map
                   )





