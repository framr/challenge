#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "Usage: %s path" % os.path.basename(__file__)
        sys.exit(0)

    task_dir = sys.argv[1]
    with open("run_pipeline_%s" % os.path.basename(task_dir), "w") as outfile:
        tasks = os.listdir(task_dir)
        for task in tasks:
            outfile.write("vw_pipeline_runner.py --task %s --outdir /home/fram/kaggle/outbrain/playground/vw/models --cache\n"
                          % os.path.join(task_dir, task))

