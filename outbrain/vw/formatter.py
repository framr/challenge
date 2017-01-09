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

from cStringIO import StringIO

from .feature import FeatureEmitter
from .vwhash import truncate_to_num_bits
from .vwutil import read_feature_stats, read_feature_map
from ..csvutil.reader import csv_file_iter


def get_vw_formatter(task, feature_stats_file=None, feature_map_file=None):
    if task['learn']['vw']['hashing_mode'] == 'auto':
        print "Using vowpal wabbit auto formatter"
        formatter = VWAutoFormatter(task, feature_stats_file=feature_stats_file,
                                    feature_map_file=feature_map_file)
    elif task['learn']['vw']['hashing_mode'] == 'manual':
        print "Using vowpal wabbit manual formatter"
        formatter = VWManualFormatter(task, feature_stats_file=feature_stats_file,
                                      feature_map_file=feature_map_file)
    else:
        raise NotImplementedError
    return formatter


def convert_csv2vw(infile_name, outfile_name, task,
                   feature_stats_file=None, feature_map_file=None, batch_size=10):

    formatter = get_vw_formatter(task, feature_stats_file=feature_stats_file,
                                 feature_map_file=feature_map_file)

    num_rows = 0
    with open(infile_name) as infile:
        with open(outfile_name, 'w') as outfile:

            examples_batch = []
            for example in csv_file_iter(infile):

                num_rows += 1
                if len(examples_batch) < batch_size:
                    examples_batch.append(example)
                else:
                    vw_formatted_lines = formatter(examples_batch)
                    outfile.write(vw_formatted_lines)
                    examples_batch = [example]

            if examples_batch:
                vw_formatted_lines = formatter(examples_batch)
                outfile.write(vw_formatted_lines)

            print "file %s converted into %s, %d rows read" % (infile_name, outfile_name, num_rows)


class VWFormatter(object):
    def __init__(self, task):
        self._task = task
    def __call__(self, example):
        pass


def normalize_label(label, loss):
    """
    for binary classification vowpal wabbit expects labels to be in set {-1, 1}
    Args:
        label:
        loss:
    Returns:

    """

    if loss != "logistic":
        return label

    normalized_label = int(label)
    if normalized_label < 1:
        normalized_label = -1
    return normalized_label


class VWAutoFormatter(VWFormatter):
    """
    Class formatting input for vowpal wabbit.
    In the auto mode all work related to creating quadratic,
    cubic features and bias is done by vw.
    """

    def __init__(self, task, feature_stats_file=None, feature_map_file=None):
        self._task = task
        self._click_field = task["click_field"]
        self._namespaces = task["learn"]["namespaces"]
        self._quadratic = task["learn"]["quadratic"]
        self._cubic = task["learn"]["cubic"]
        self._loss = task["learn"]["vw"]["loss"]

        self._min_shows = task.get('min_shows', 1)
        self._feature_stats_filename = feature_stats_file
        self._feature_stats = None
        if self._min_shows > 1:
            print "min_shows > 1, reading feature_stats file to be used for filtration"
            self._feature_stats = read_feature_stats(self._feature_stats_filename)

        if task["learn"]["vw"].get("manual_bias", False):
            raise NotImplementedError("manual bias currently not supported in VWAutoFormatter")

        self._feature_separator = task.get("log_config", {}).get("feature_separator", None)

    def __call__(self, examples):

        buffer = StringIO()
        for num_example, example in enumerate(examples):
            #print getattr(example, self._click_field)
            class_label = normalize_label(getattr(example, self._click_field), self._loss)
            buffer.write("%s " % class_label)
            for ns in self._namespaces:
                features = getattr(example, ns).strip().split(self._feature_separator)

                vw_ns = self._task["learn"]["ns_rename"].get(ns, ns)
                if self._min_shows > 1:
                    # optionally filter features with low statistics
                    features = [f for f in features
                                if self._feature_stats[ns].get(f, 0) >= self._min_shows]
                    buffer.write("|%s %s" % (vw_ns, " ".join(features)))
                else:
                    buffer.write("|%s %s" % (vw_ns, " ".join(features)))

            #if num_example + 1 < len(examples):
            buffer.write("\n")

        # in the auto mode bias we use automatic bias provided by vowpal wabbit
        return buffer.getvalue()



class VWManualFormatter(VWFormatter):
    """
    This formatter manually creates quadratic and cubic features for vowpal wabbit
    and puts them into anonymous namespace

    The rare filtering feature works different than in the case of automatic regime:
    here we accept feature if it is present in feature map, otherwise it is rejected
    """

    def __init__(self, task, feature_stats_file=None, feature_map_file=None):
        self._feature_emitter = FeatureEmitter(task, ns_join=True)
        self._feature_map_file = feature_map_file

        print "reading feature map file from %s" % self._feature_map_file
        self._feature_map = read_feature_map(self._feature_map_file)

        self._task = task
        self._click_field = task["click_field"]

        self._loss = task["learn"]["vw"]["loss"]
        self._num_bits = task["learn"]["vw"]["num_bits"]
        #self._namespaces = task["learn"]["namespaces"]
        #self._quadratic = task["learn"]["quadratic"]
        #self._cubic = task["learn"]["cubic"]

        if task["learn"]["vw"].get("auto_bias", False):
            raise NotImplementedError("Automatic bias is not supported in VWAutoFormatter")

        if task["learn"]["vw"]["hashing_mode"] != "manual":
            raise ValueError("Manual formatter supports hashing_mode = manual only")

        self._feature_separator = task.get("log_config", {}).get("feature_separator", None)

    def _process_example(self, example):
        """
        get vw line for single example
        Args:
            example:
        Returns:
        """

        buffer = StringIO()
        example_features = self._feature_emitter(example)
        print example_features
        for namespace, ns_features in example_features:
            # truncation to num_bits is somewhat excessive here
            # we use it here for clarity (?)
            features = [str(truncate_to_num_bits(int(self._feature_map[namespace][feature]), self._num_bits))
                        for feature in ns_features
                            if feature in self._feature_map[namespace]
            ]

            if features:
                buffer.write(" %s" % " ".join(features))

        return buffer.getvalue()

    def __call__(self, examples):

        buffer = StringIO(  )
        for num_example, example in enumerate(examples):
            example_vw_line = self._process_example(example)

            class_label = normalize_label(getattr(example, self._click_field), self._loss)
            buffer.write("%s |%s" % (class_label, example_vw_line))

            #buffer.write(" %s" % self._feature_map["bias"][""])
            #if num_example + 1 < len(examples): # write EOL always except for the last example
            buffer.write("\n")

        return buffer.getvalue()


class VWCRRManualFormatter(object):

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

        self._crr_alpha = task["learn"]["crr"]["crr_alpha"]
        self._crr_key = task["learn"]["crr"]["group_key"]

        if task["learn"]["vw"]["hashing_mode"] != "manual":
            raise ValueError("")


    def __call__(self, examples):
        """
        Args:
            self:
            examples: A group of examples

        Returns:
        # Create vw lines for normal examples
        # using FeatureEmitter

        # Create vw lines for
        """

        # Use manual formatter as a stub

        pass


