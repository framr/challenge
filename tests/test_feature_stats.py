import pytest
import unittest
import os
import yaml


from outbrain.vw.vwutil import compute_feature_stats, read_feature_stats


@pytest.fixture()
def task1():
    return yaml.load(open("./tests/fixtures/fixture_log_for_feature_stats1.csv_task.yml"))


@pytest.fixture()
def task2():
    return yaml.load(open("./tests/fixtures/fixture_log_for_feature_stats1.csv_task2.yml"))


@pytest.fixture()
def log_and_feature_stats_t1():
    return ("./tests/fixtures/fixture_log_for_feature_stats1.csv",
            read_feature_stats("./tests/fixtures/fixture_log_for_feature_stats1.csv_feature_stats")
            )

@pytest.fixture()
def log_and_feature_stats_t2():
    return ("./tests/fixtures/fixture_log_for_feature_stats1.csv",
            read_feature_stats("./tests/fixtures/fixture_log_for_feature_stats1.csv_feature_stats_task2")
            )


def test_compute_feature_stats1(log_and_feature_stats_t1, task1):
    log, expected_fstats = log_and_feature_stats_t1
    feature_stats = compute_feature_stats(log, task1)

    #unittest.TestCase.assertDictEqual(expected_fstats, feature_stats)
    assert expected_fstats == feature_stats


def test_compute_feature_stats2(log_and_feature_stats_t2, task2):
    log, expected_fstats = log_and_feature_stats_t2
    feature_stats = compute_feature_stats(log, task2)

    print expected_fstats, feature_stats
    #unittest.TestCase.assertDictEqual(expected_fstats, feature_stats)
    assert expected_fstats == feature_stats
