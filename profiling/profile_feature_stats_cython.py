#!/usr/bin/env python
import os
import yaml
from argparse import ArgumentParser

from outbrain.vw.vwutil_fast import create_feature_stats_file_fast

if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="infile", type=str, default=None, help="input file")
    argparser.add_argument("-t", dest="task", type=str, default=None, help="task file")
    args = argparser.parse_args()

    feature_stats = os.path.join(os.getcwd(), "output", "profiling_feature_stats.csv")
    task = yaml.load(open(args.task).read())


    create_feature_stats_file_fast(args.infile, task, feature_stats)

