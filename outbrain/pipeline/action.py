import os
import yaml

from outbrain.metrics.common import compute_metrics


__all__ = []
def export(func):
    __all__.append(func.__name__)
    return func


@export
def action__prepare_log_for_lightgbm(task, mbus, use_cache=False):
    pass

@export
def action__learn_lightgbm(task, mbus, use_cache=False):
    pass

@export
def action__apply_lightgbm(task, mbus, use_cache=False):
    pass


@export
def action__compute_metrics(task, mbus, use_cache=False):

    mbus.metrics_learn = os.path.join(os.getcwd(), "metrics_learn.yml")
    metrics_learn = compute_metrics(mbus.predicted_merged_learn, task["metrics"])

    for name, value in metrics_learn.iteritems():
        print "%s = %f" % (name, value)
    with open(mbus.metrics_learn, "w") as outfile:
        yaml.dump(metrics_learn, outfile)

    if not mbus.predicted_merged_test:
        return

    mbus.metrics_test = os.path.join(os.getcwd(), "metrics_test.yml")
    metrics_test = compute_metrics(mbus.predicted_merged_test, task["metrics"])

    for name, value in metrics_test.iteritems():
        print "%s = %f" % (name, value)
    with open(mbus.metrics_test, "w") as outfile:
        yaml.dump(metrics_test, outfile)
