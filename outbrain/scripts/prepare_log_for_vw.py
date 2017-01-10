#!/usr/bin/env python
import os
import yaml
from argparse import ArgumentParser

from outbrain.vw.formatter_fast import convert_csv2vw_fast


def get_task(args):

    task = None
    if args.task:
        print "using task from file %s" % args.task
        task = yaml.load(open(args.task).read())
    elif args.model_path:
        task_file = os.path.join(args.model_path, "task.yml")
        print "using task from file %s" % task_file
        task = yaml.load(open(task_file).read())
    else:
        raise ValueError("Task file not specified, abort")

    return task


def get_feature_stats(args):

    feature_stats = None
    if args.feature_stats:
        print "using feature stats from file %s" % args.feature_stats
        feature_stats = args.feature_stats
    elif args.model_path:
        print "looking for feature_stats.csv in path %s" % args.model_path
        candidate = os.path.join(args.model_path, "feature_stats.csv")
        if os.path.isfile(candidate):
            print "success"
            feature_stats = candidate
        else:
            print "not found, assuming no feature_stats is needed"

    else:
        print "no location for feature_stats.csv provided"

    return feature_stats


def get_feature_map(args):

    feature_map = None
    if args.feature_map:
        print "using feature map from file %s" % args.feature_map
        feature_map = args.feature_map
    elif args.model_path:
        print "looking for feature_map.csv in path %s" % args.model_path
        candidate = os.path.join(args.model_path, "feature_map.csv")
        if os.path.isfile(candidate):
            print "success"
            feature_map = candidate
        else:
            print "not found, assuming no feature_map is needed"

    else:
        print "no location for feature_map.csv provided"

    return feature_map


if __name__ == "__main__":


    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="input", type=str, default=None, help="input file")
    argparser.add_argument("-o", dest="output", type=str, default=None, help="output file")
    argparser.add_argument("--model", dest="model_path", type=str, default=None, help="path with vw model")
    argparser.add_argument("--task", dest="task", type=str, default=None, help="task yml")
    argparser.add_argument("--fstats", dest="feature_stats", type=str, default=None, help="feature_stats file")
    argparser.add_argument("--fmap", dest="feature_map", type=str, default=None, help="feature_map file")

    args = argparser.parse_args()

    task = get_task(args)
    feature_stats_file = get_feature_stats(args)
    feature_map_file = get_feature_map(args)

    convert_csv2vw_fast(
        args.input,
        args.output,
        task,
        feature_stats_file=feature_stats_file,
        feature_map_file=feature_map_file,
        test_mode=True
    )

    infile = task["learn"]["learn_file"]
