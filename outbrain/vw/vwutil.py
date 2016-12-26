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
        for example in csv_file_iter(infile):
            feature_stats[example.namespace][example.feature] = int(example.shows)

    return feature_stats


def compute_feature_stats(csv_file, task, ns_join_sentinel="^"):

    emitter = FeatureEmitter(task)

    feature_stats = defaultdict(dict)
    with open(csv_file) as infile:
        for example in csv_file_iter(infile):
            features_list = emitter(example)

            for ns, features in features_list:

                if not isinstance(ns, tuple):
                    for fid in features:
                        feature_stats[ns][fid] = feature_stats[ns].get(fid, 0) + 1
                else: # polynomial features 
                    composite_ns = ns_join_sentinel.join(ns)
                    for fid in features:
                        composite_fid = ns_join_sentinel.join(fid)
                        feature_stats[composite_ns][composite_fid] = feature_stats[composite_ns].get(
                            composite_fid, 0) + 1

    return feature_stats


def create_feature_stats_file(csv_file, task, outfile, ns_join_sentinel="^"):

    stats = compute_feature_stats(csv_file, task, ns_join_sentinel=ns_join_sentinel)
    with open(outfile, "w") as out:
        out.write("namespace,feature,shows\n")
        for ns, ns_stats in stats.iteritems():
            for feature, shows in ns_stats.iteritems():
                outfile.write("%s,%s,%s\n" % (ns, feature, shows))



class FeatureEmitter(object):
    def __init__(self, task, separator=",", feature_separator=" ", ns_join_sentinel="^"):
        """
        Args:
            task: config describing features
        """
        self._task = task
        self._namespaces = task["learn"]["namespaces"] or []
        self._quadratic = task["learn"]["quadratic"] or []
        self._cubic = task["learn"]["cubic"] or []
        self._separator = separator
        self._feature_separator = feature_separator
        self._ns_join_sentinel = ns_join_sentinel

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
                (
                    ns,
                    getattr(example, ns).split(self._feature_separator)
                )
            )


        for first, second in self._quadratic:
            result.append(
                (
                    (first, second),
                    list(product(
                        getattr(example, first).split(self._feature_separator),
                        getattr(example, second).split(self._feature_separator)
                    ))
                )
            )

        for first, second, third in self._cubic:
            result.append(
                (
                    (first, second, third),
                    list(product(
                        product(
                            getattr(example, first).split(self._feature_separator),
                            getattr(example, second).split(self._feature_separator),
                        ),
                        getattr(example, third).split(self._feature_separator)
                    ))
                )
            )

        return result





