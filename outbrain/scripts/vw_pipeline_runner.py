#!/usr/bin/env python
"""
We have two posible pipelines here

1) compute feature stats [optional]
2) convert log into vw format using VWAutoFormatter [using optional feature stats fo filtering features]
3) run vw
4) compute metrics on train and test


1) compute feature stats [optional]
1) compute feature map [optionally filtering it using feature stats]
2) convert log into vw format using VWManualFormatter [using optional feature stats fo filtering features]
3) run vw
4) compute metrics on train and test
"""

import os
from argparse import ArgumentParser
import yaml


from outbrain.vw.pipeline.processor import run_pipeline, DEFAULT_VW_PIPELINE


if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("--task", dest="task", default=None, type=str, required=True,
                           help="yaml file with task config")
    argparser.add_argument("--outdir", dest="outdir", default="./", type=str,
                       help="output directory for vw models")

    args = argparser.parse_args()

    task = yaml.load(open(args.task).read())

    print "Processing task %s" % task["task_id"]
    work_dir = os.path.join(args.outdir, task["task_id"])

    print "Setting working directory to %s" % work_dir
    os.chdir(work_dir)

    print "Processing pipeline"
    run_pipeline(DEFAULT_VW_PIPELINE, task)

