import time

from outbrain.vw.pipeline.action import *
from outbrain.vw.pipeline.message_bus import get_message_bus


DEFAULT_VW_PIPELINE = [
    action__compute_feature_stats,
    action__compute_feature_map,
    action__prepare_log_for_vw,
    action__learn_vw,
    action__apply_vw,
    action__save_message_bus
]


def run_pipeline(pipeline, task, use_cache=False):

    mbus = get_message_bus()
    for action in pipeline:

        print "Processing action %s" % action.__name__
        prev_time = time.clock()
        action(task, mbus, use_cache=use_cache)
        elapsed_time = time.clock() - prev_time

        print "executing %s action took %s seconds (%s hours)" % (
            action.__name__, elapsed_time, elapsed_time / 3600.0)
