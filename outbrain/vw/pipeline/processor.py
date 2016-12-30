

from outbrain.vw.pipeline.action import *
from outbrain.vw.pipeline.message_bus import get_message_bus


DEFAULT_VW_PIPELINE = [
    action__compute_feature_stats,
    action__compute_feature_map,
    action__prepare_log_for_vw,
    action__learn_vw,
    action__apply_vw
]


def run_pipeline(pipeline, task):

    mbus = get_message_bus()
    for action in pipeline:

        print "Processing action %s" % action.__name__
        action(task, mbus)

