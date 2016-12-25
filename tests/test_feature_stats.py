import pytest
import unittest

from outbrain.vw.vwutil import compute_feature_stats, read_feature_stats


@pytest.fixture()
def log_and_feature_stats_t1():
    return ("./fixtures/fixture_log_for_feature_stats1.csv",
            read_feature_stats("./fixtures/fixture_log_for_feature_stats1.csv_feature_stats")
            )



def test_compute_feature_stats(log_and_feature_stats1_t1):
    log, expected_fstats = log_and_feature_stats1_t1
    feature_stats = compute_feature_stats(log)

    unittest.TestCase.assertDictEqual(expected_fstats, feature_stats)
