import pytest
#from math import log
import numpy as np


from outbrain.metrics.common import compute_metrics


def read_log(infilename):
    with open(infilename) as infile:

        header = infile.readline().strip()
        group = []
        clicked = []
        pred = []
        for row in infile:
            group_id, label, p = row.strip().split(",")
            group.append(int(group_id))
            clicked.append(int(label))
            pred.append(float(p))
    return group, clicked, pred


def logloss(predictions, labels):
    p = np.array(predictions)
    y = np.array(labels)
    logloss = y * np.log(p) + (1 - y) * np.log(1 - p)
    return logloss.sum()


@pytest.fixture()
def log_name1():
    return "./tests/fixtures/fixture_log_for_test_metrics1.csv"

@pytest.fixture()
def log_name1_config():
    return {
        "class_field": "clicked",
        "predictions_field": "sigmoid_VW",
        "group_field": "group"
    }


@pytest.fixture()
def map_for_log_name1():
    result = 0.0 + 1.0 + 1.0 / 2 + (1.0 + 2.0 / 3) / 2
    return result


def test_compute_metrics(log_name1, log_name1_config, map_for_log_name1):

    metrics = compute_metrics(log_name1, log_name1_config)
    group, clicked, predictions = read_log(log_name1)
    expected_logloss = logloss(predictions, clicked)

    assert metrics["logloss"] == pytest.approx(expected_logloss, rel=1e-5)
    assert metrics["map"] == pytest.approx(map_for_log_name1, rel=1e-5)







