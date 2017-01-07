import os
import yaml

from outbrain.vw.vwutil import *
from outbrain.vw.formatter import convert_csv2vw
from outbrain.vw.learn import learn_vw
from outbrain.vw.apply import VWAutoPredictor, merge_predictions
from outbrain.metrics.common import compute_metrics


__all__ = []
def export(func):
    __all__.append(func.__name__)
    return func


@export
def action__compute_feature_stats(task, mbus, use_cache=False):

    mbus.feature_stats = None
    if task.get("min_shows", 0) <= 1 and not task["create_feature_stats"]:
        return

    mbus.feature_stats = os.path.join(os.getcwd(), "feature_stats.csv")
    if use_cache and os.path.isfile(mbus.feature_stats):
        print "ouput feature stats already exists, using it from cache %s" % mbus.feature_stats
    else:
        infile = task["learn"]["learn_file"]
        create_feature_stats_file(infile, task, mbus.feature_stats)


@export
def action__compute_feature_map(task, mbus, use_cache=False):
    mbus.feature_map = None

@export
def action__prepare_log_for_vw(task, mbus, use_cache=False):

    infile = task["learn"]["learn_file"]

    outfile = os.path.join(os.getcwd(), "learn_vw.txt")
    mbus.learn_vw_file = outfile

    print "converting learn file %s into vw format" % infile
    if use_cache and os.path.isfile(outfile):
        print "learn outfile already exists, skipping operation and using cache"
    else:
        convert_csv2vw(infile,
                       mbus.learn_vw_file,
                       task,
                       feature_stats_file=mbus.feature_stats,
                       feature_map_file=mbus.feature_map
        )


    if task.get("test", {}).get("test_file", None) is not None:

        infile = task["test"]["test_file"]
        print "converting test file %s into vw format" % infile

        outfile = os.path.join(os.getcwd(), "test_vw.txt")
        mbus.test_vw_file = outfile

        if use_cache and os.path.isfile(outfile):
            print "test outfile already exists, skipping operation and using cache"
        else:
            convert_csv2vw(infile,
                           mbus.test_vw_file,
                           task,
                           feature_stats_file=mbus.feature_stats,
                           feature_map_file=mbus.feature_map
                           )


@export
def action__learn_vw(task, mbus, use_cache=False):

    print "Entering learn_vw action"
    learn_file = mbus.learn_vw_file
    print "Input learn file: %s" % learn_file

    cur_dir = os.getcwd()

    mbus.vw = {
        "model": os.path.join(cur_dir, "model"),
        "readable_model" : os.path.join(cur_dir, "readable_model")
    }

    #mbus.vw.model = os.path.join(cur_dir, "model")
    #mbus.vw.readable_model = os.path.join(cur_dir, "readable_model")
    #mbus.vw.readable_model_inverted = os.path.join(cur_dir, "readable_model_inverted")

    if use_cache and os.path.isfile(mbus.vw.model):
        print "found cached vw model in cache enabled mode, skipping learning vowpal wabbit"
    else:
        learn_vw(learn_file, task)
        print "learning vw action finished"
        print "vw models saved in %s and %s files" % (mbus.vw.model, mbus.vw.readable_model)


@export
def action__apply_vw(task, mbus, use_cache=False):

    model_path = mbus.vw.model
    predictor = VWAutoPredictor(model_path)

    mbus.predicted_learn = os.path.join(os.getcwd(), "learn_vw.predicted.txt")
    mbus.predicted_merged_learn = os.path.join(os.getcwd(), "learn_vw_merged.predicted.txt")

    if use_cache and os.path.isfile(mbus.predicted_learn) and os.path.isfile(mbus.predicted_merged_learn):
        print "found cached files with predictions %s and %s, skipping applying vw" % (
            mbus.predicted_learn, mbus.predicted_merged_learn)
    else:
        predictor.apply(mbus.learn_vw_file, mbus.predicted_learn)
        merge_predictions(task["learn"]["learn_file"], mbus.predicted_learn, mbus.predicted_merged_learn)

    if mbus.test_vw_file is not None:

        mbus.predicted_test = os.path.join(os.getcwd(), "test_vw.predicted.txt")
        mbus.predicted_merged_test = os.path.join(os.getcwd(), "test_vw_merged.predicted.txt")

        if (use_cache
            and os.path.isfile(mbus.predicted_test)
            and os.path.isfile(mbus.predicted_merged_test)
        ):
            print "found cached files with predictions %s and %s, skipping applying vw" % (
            mbus.predicted_test, mbus.predicted_merged_test)

        else:
            predictor.apply(mbus.test_vw_file, mbus.predicted_test)
            merge_predictions(task["test"]["test_file"], mbus.predicted_test, mbus.predicted_merged_test)


@export
def action__compute_metrics(task, mbus, use_cache=False):

    mbus.metrics = os.path.join(os.getcwd(), "metrics.yml")
    metrics = compute_metrics(mbus.predicted_merged_learn, task["metrics"])

    metrics = compute_metrics(mbus.predicted_merged_learn, task["metrics"])
    for name, value in metrics.iteritems():
        print "%s = %f" % (name, value)

    with open(mbus.metrics, "w") as outfile:
        yaml.dump(metrics, outfile)



@export
def action__save_message_bus(task, mbus, use_cache=False):
    with open("message_bus.yml", "w") as outfile:
        outfile.write(yaml.dump(mbus))




