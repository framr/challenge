import os
from attrdict import AttrDict


DEFAULT_VW_BUS = {
    "learn_vw_file": None,
    "test_vw_file": None,
    "feature_stats": None,
    "feature_map": None,
    "learn": None,
    "test": None,
    "vw": {
        "model": None,
        "readable_model": None
    },
    "predicted_learn": None,
    "predicted_merged_learn": None,
    "predicted_merged_test": None,
    "predicted_test": None,
    "metrics_learn": None,
    "metrics_test": None,
    "timing": None
}


DEFAULT_XGBOOST_BUS = {}

DEFAULT_LGBM_BUS = {
    "learn_formatted": None,
    "test_formatted": None,
    "learn": None,
    "test": None,
    "metrics_learn": None,
    "metrics_test": None
}


def get_message_bus(task, path=None):
    #if not path:
    #    path = os.getcwd()

    if task["engine"] == "vw":
        return AttrDict(DEFAULT_VW_BUS)
    elif task["engine"] == "xgboost":
        return AttrDict(DEFAULT_XGBOOST_BUS)
    elif task["engine"] == "lightgbm":
        return AttrDict(DEFAULT_LGBM_BUS)
    else:
        raise NotImplementedError("unknown engine %s" % task["engine"])



