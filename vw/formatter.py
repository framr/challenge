"""
Utils for formatting vowpal wabbit input
"""

"""
Vowpal Wabbit input file format
https://github.com/JohnLangford/vowpal_wabbit/wiki/Input-format
[Label] [Importance] [Base] [Tag]|Namespace Features |Namespace Features ... |Namespace Features
where
Namespace=String[:Value]
Features=(String[:Value] )*

Label is the real number that we are trying to predict for this example.
If the label is omitted, then no training will be performed with the corresponding example,
although VW will still compute a prediction.

Importance (importance weight) is a non-negative real number indicating the relative importance of this
example over the others. Omitting this gives a default importance of 1 to the example.

Base is used for residual regression. It is added to the prediction before computing an update.
The default value is 0.

Tag is a string that serves as an identifier for the example. It is reported back when predictions are made.
It doesn't have to be unique. The default value if it is not provided is the empty string.
If you provide a tag without a weight you need to disambiguate: either make the tag touch the |
(no trailing spaces) or mark it with a leading single-quote '.
If you don't provide a tag, you need to have a space before the |.

Namespace is an identifier of a source of information for the example optionally followed by a float
(e.g., MetricFeatures:3.28), which acts as a global scaling of all the values of the features in this namespace.
If value is omitted, the default is 1. It is important that the namespace not have a space between
the separator | as otherwise it is interpreted as a feature.

Features is a sequence of whitespace separated strings, each of which is optionally followed
by a float (e.g., NumberOfLegs:4.0 HasStripes). Each string is a feature and the value is the feature value
for that example. Omitting a feature means that its value is zero.
Including a feature but omitting its value means that its value is 1.
"""

from ..csvutil.reader import csv_file_iter
from .vwutil import FeatureEmitter, read_feature_stats
from cStringIO import StringIO


def get_vw_formatter(task):
    if task['mode'] == 'auto':
        formatter = VWAutoFormatter(task)
    else:
        formatter = VWManualFormatter(task)
    return formatter


def convert_csv2vw(infile_name, outfile_name, task, batch_size=10):

    formatter = get_vw_formatter(task)
    with open(infile_name) as infile:
        with open(outfile_name, 'w') as outfile:

            examples_batch = []
            for example in csv_file_iter(infile):

                if len(examples_batch) < batch_size:
                    examples_batch.append(example)
                else:
                    vw_formatted_lines = formatter(examples_batch)
                    outfile.write(vw_formatted_lines)

            if examples_batch:
                vw_formatted_lines = formatter(examples_batch)
                outfile.write(vw_formatted_lines)



class VWFormatter(object):
    def __init__(self, task):
        self._task = task
    def __call__(self, example):
        pass


class VWAutoFormatter(VWFormatter):
    """
    Class formatting input for vowpal wabbit.
    In the auto mode all work related to creating quadratic,
    cubic features and bias is done by vw.
    """

    def __init__(self, task):
        self._task = task
        self._click_field = task["click_field"]
        self._namespaces = task["learn"]["namespaces"]
        self._quadratic = task["learn"]["quadratic"]
        self._cubic = task["learn"]["cubic"]

        self._min_shows = task.get('min_shows', 1)
        self._feature_stats_filename = task.get("feature_stats", None)
        self._feature_stats = None
        if self._min_shows > 1:
            self._feature_stats = read_feature_stats(self._feature_stats_filename)


    def __call__(self, examples):

        buffer = StringIO()
        for example in examples:
            buffer.write("%s " % getattr(example, self._click_field))
            for ns in self._namespaces:
                features = getattr(example, ns)

                if self._min_shows > 1:
                    # optionally filter features with low statistics
                    features = [f for f in features
                                if self._feature_stats[ns].get(f, 0) >= self._min_shows]
                    buffer.write("|%s %s" % (ns, " ".join(features)))
                else:
                    buffer.write("|%s %s" % (ns, " ".join(features)))

            buffer.write("\n")

        yield buffer.getvalue()

        # in the auto mode bias we use automatic bias provided by vowpal wabbit


class VWManualFormatter(VWFormatter):
    """
    This formatter manually creates quadratic and cubic features for vowpal wabbit

    """
    def __init__(self, task):
        self._emitter = FeatureEmitter()
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        pass
