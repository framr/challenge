# XXX
# TODO: refactor - this file currently duplicates vw pipeline processor
# XXX

import time

import outbrain.pipeline.action
from .message_bus import get_message_bus
#from outbrain.vw.pipeline.action import *
#from outbrain.vw.pipeline.message_bus import get_message_bus



def read_pipeline_from_task(task, default_pipeline=None):

    if task.get("pipeline", None):
        pipeline = [getattr(outbrain.pipeline.action, stage) for stage in task["pipeline"]]
    else:
        pipeline = default_pipeline

    return pipeline


def run_pipeline(pipeline, task, use_cache=False):

    mbus = get_message_bus(task)
    mbus.timing = {}
    for action in pipeline:

        print "=" * 80
        print "Processing action %s" % action.__name__
        prev_time = time.clock()
        action(task, mbus, use_cache=use_cache)
        elapsed_time = time.clock() - prev_time

        print "executing %s action took %0.1f seconds (%0.1f mins)" % (
            action.__name__, elapsed_time, elapsed_time / 60.0)
        mbus.timing[action.__name__] = elapsed_time / 60.0

