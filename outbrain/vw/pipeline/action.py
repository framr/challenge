import os

from outbrain.vw.vwutil import *
from outbrain.vw.formatter import convert_csv2vw
from outbrain.vw.learn import learn_vw
from outbrain.vw.apply import VWAutoPredictor


__all__ = []
def export(func):
    __all__.append(func.__name__)
    return func


@export
def action__compute_feature_stats(task, mbus):

    infile = task["learn"]["learn_file"]
    mbus.feature_stats == os.path.join(os.getcwd(), "feature_stats.csv")
    create_feature_stats_file(infile, task, mbus.feature_stats)


@export
def action__compute_feature_map(task, mbus):
    mbus.feature_map = None


@export
def action__prepare_log_for_vw(task, mbus):

    infile = task["learn"]["learn_file"]
    mbus.learn_vw_file = os.path.join(os.getcwd(), "learn_vw.txt")

    convert_csv2vw(infile,
                   mbus.learn_vw_file,
                   task,
                   feature_stats_file=mbus.feature_stats,
                   feature_map_file=mbus.feature_map
    )

    mbus.learn_vw_file = None
    if task.get("test", {}).get("test_file", None) is not None:
        infile = task["test"]["test_file"]
        mbus.test_vw_file == os.path.join(os.getcwd(), "test_vw.txt")
        convert_csv2vw(infile, mbus.learn_vw_file, task)


@export
def action__learn_vw(task, mbus):

    print "Entering learn_vw action"
    learn_file = mbus.learn_vw_file
    learn_vw(learn_file, task)
    print "learning vw action finished"

    cur_dir = os.getcwd()
    mbus.vw.model = os.path.join(cur_dir, "model")
    mbus.vw.readable_model = os.path.join(cur_dir, "readable_model")
    mbus.vw.readable_model_inverted = os.path.join(cur_dir, "readable_model_inverted")

    print "vw models saved in %s, %s and %s files" % (mbus.vw.model, mbus.vw.readable_model,
        mbus.vw.readable_model_inverted)


@export
def action__apply_vw(task, mbus):

    model_path = mbus.vw.model
    predictor = VWAutoPredictor(model_path)

    mbus.predict.learn = os.path.join(os.getcwd(), "learn_vw.predicted.txt")
    predictor.apply(mbus.learn_vw_file, mbus.predict.learn, task)


    if mbus.test_vw_file is not None:
        mbus.predict.test = os.path.join(os.getcwd(), "test_vw.predicted.txt")
        predictor.apply(mbus.test_vw_file, mbus.predict.test, task)


@export
def action__compute_metrics(task, mbus):

    pass



