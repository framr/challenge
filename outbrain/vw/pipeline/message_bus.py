import os

from attrdict import AttrDict

DEFAULT_CONFIG = {
    "learn_vw_file": None,
    "test_vw_file": None,
    "feature_stats": None,
    "feature_map": None,
    "learn": None,
    "test": None,
    "vw": {
        "model": None,
        "readable_model": None
#        "readable_model_inverted": None
    },
    "predicted_learn": None,
    "predicted_merged_learn": None,
    "predicted_merged_test": None,
    "predicted_test": None,
    "metrics_learn": None,
    "metrics_test": None,
    "timing": None
}


def get_message_bus(path=None):
    if not path:
        path = os.getcwd()
    return AttrDict(DEFAULT_CONFIG)
