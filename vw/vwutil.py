from collections import namedtuple, defaultdict

from ..csvutil.reader import csv_file_iter


def read_feature_stats(filename):
    """
    assume here feature_stats format:
    namespace,feature_id,shows
    Args:
        filename:

    Returns:
        dictionary namespace -> feature_id -> shows
    """

    feature_stats = defaultdict(dict)
    with open(filename) as infile:
        for example in csv_file_iter(filename):
            feature_stats[example.namespace][example.feature_id] = example.shows

    return feature_stats


class FeatureEmitter(object):
    def __init__(self, task):
        """
        Args:
            task: config describing features
        """
        self._task = task

    def __call__(self, example):
        """
        Args:
            example: line
        Returns:
            dict {"namespace1" : [f1, f2], "namespace2,namespace3": [f3, f5]}
        """
        pass