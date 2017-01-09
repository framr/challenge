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
import yaml
from argparse import ArgumentParser

from outbrain.vw.pipeline.processor import run_pipeline, DEFAULT_VW_PIPELINE, read_pipeline_from_task

if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("--task", dest="task", default=None, type=str, required=True,
                           help="yaml file with task config")
    argparser.add_argument("--outdir", dest="outdir", default="./", type=str,
                       help="output directory for vw models")
    argparser.add_argument("--cache", dest="use_cache", action="store_true",
                           help="use cached files if available")

    args = argparser.parse_args()

    task = yaml.load(open(args.task).read())

    print "Processing task %s" % task["task_id"]
    work_dir = os.path.join(args.outdir, task["task_id"])
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)


    print "Setting working directory to %s" % work_dir
    os.chdir(work_dir)



    pipeline = read_pipeline_from_task(task, default_pipeline=DEFAULT_VW_PIPELINE)
    print "Processing pipeline"
    run_pipeline(pipeline, task, use_cache=args.use_cache)

