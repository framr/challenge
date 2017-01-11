from collections import defaultdict

from .feature_fast import FeatureEmitter
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

    #feature_stats = defaultdict(dict)
    cdef dict feature_stats = {}
    with open(filename) as infile:
        for example in csv_file_iter(infile):
            if example.namespace not in feature_stats:
                feature_stats[example.namespace] = {}
            feature_stats[example.namespace][example.feature] = int(example.shows)

    return feature_stats


def compute_feature_stats(csv_file, task, ns_join_sentinel="^"):

    emitter = FeatureEmitter(task, ns_join=True, ns_join_sentinel=ns_join_sentinel)
    feature_stats = defaultdict(dict)

    cdef list features_list
    with open(csv_file) as infile:
        for example in csv_file_iter(infile):
            features_list = emitter(example)

            for ns, features in features_list:
                for fid in features:
                    feature_stats[ns][fid] = feature_stats[ns].get(fid, 0) + 1

    return feature_stats


def create_feature_stats_file_fast(csv_file, task, outfile, ns_join_sentinel="^"):

    stats = compute_feature_stats(csv_file, task, ns_join_sentinel=ns_join_sentinel)
    with open(outfile, "w") as out:
        out.write("namespace,feature,\n")
        for ns, ns_stats in stats.iteritems():
            for feature, shows in ns_stats.iteritems():
                out.write("%s,%s,%s\n" % (ns, feature, shows))


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


def create_feature_map_file_fast(csv_file, task, outfile, ns_join_sentinel="^", min_shows=1,
                            type="enumeration"):

    if type != "enumeration":
        raise NotImplementedError

    fid = 0
    stats = compute_feature_stats(csv_file, task, ns_join_sentinel=ns_join_sentinel)
    with open(outfile, "w") as out:
        out.write("namespace,feature,fid\n")
        for ns, ns_stats in stats.iteritems():
            for feature, shows in ns_stats.iteritems():

                if shows >= min_shows:
                    out.write("%s,%s,%s\n" % (ns, feature, fid))
                    fid += 1
