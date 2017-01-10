from collections import defaultdict

from .feature_fast import FeatureEmitter
from ..csvutil.reader import csv_file_iter

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


def create_feature_stats_file(csv_file, task, outfile, ns_join_sentinel="^"):

    stats = compute_feature_stats(csv_file, task, ns_join_sentinel=ns_join_sentinel)
    with open(outfile, "w") as out:
        out.write("namespace,feature,shows\n")
        for ns, ns_stats in stats.iteritems():
            for feature, shows in ns_stats.iteritems():
                out.write("%s,%s,%s\n" % (ns, feature, shows))

