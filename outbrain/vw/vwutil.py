from collections import namedtuple, defaultdict
from itertools import product

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


def compute_feature_stats(csv_file, task):

    emitter = FeatureEmitter(task)

    feature_stats = defaultdict(dict)
    with open(csv_file) as infile:
        for example in csv_file_iter(csv_file):
            features_list = emitter(example)

            for ns, features in features_list:
                for fid in features:
                    feature_stats[ns][fid] = feature_stats[ns].get(fid, 0) + 1


def create_feature_stats_file(csv_file, task, outfile):

    stats = compute_feature_stats(csv_file, task)
    with open(outfile, "w") as out:
        out.write("namespace,feature,shows\n")
        for ns, ns_stats in stats.iteritems():
            for feature, shows in ns_stats.iteritems():
                outfile.write("%s,%s,%s\n" % (ns, feature, shows))



class FeatureEmitter(object):
    def __init__(self, task, separator=","):
        """
        Args:
            task: config describing features
        """
        self._task = task
        self._namespaces = task["learn"]["namespaces"]
        self._quadratic = task["learn"]["quadratic"]
        self._cubic = task["learn"]["cubic"]
        self._separator = ","

    def __call__(self, example):
        """
        Args:
            example: line
        Returns:
            dict {"namespace1" : [f1, f2], "namespace2,namespace3": [f3, f5]}
            list [("namespace1", [f1, f2, f3]), ()]?
        """

        result = []
        for ns in self._namespaces:
            result.append(
                tuple(
                    ns,
                    getattr(example, ns).split(self._separator)
                )
            )


        for first, second in self._quadratic:
            result.append(
                tuple(
                    self._separator.join([first, second]),
                    list(product(
                        getattr(example, first).split(self._separator),
                        getattr(example, second).split(self._separator)
                    ))
                )
            )


        for first, second, third in self._cubic:
            result.append(
                tuple(
                    self._separator.join([first, second, third]),
                    list(product(
                        product(
                            getattr(example, first).split(self._separator),
                            getattr(example, second).split(self._separator),
                        ),
                        getattr(example, third).split(self._separator)
                    ))
                )
            )

        return result





