from collections import namedtuple, defaultdict
from itertools import product

from ..csvutil.reader import csv_file_iter
from .feature import FeatureEmitter


def read_feature_map(filename):
    """
    feature_map format:
    namespace,feature,fid

    fid is some feature id, for instance it could be a hash of (namespace, feature)
    """
    feature_map = defaultdict(dict)
    with open(filename) as infile:
        for example in csv_file_iter(infile):
            feature_map[example.namespace][example.feature] = int(example.fid)

    return feature_map


def filter_feature_map(filename):
    raise NotImplementedError


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


def create_feature_map(csv_file, task):
    raise NotImplementedError

