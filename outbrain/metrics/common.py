from ..csvutil.reader import csv_file_iter, csv_file_group_iter
from .evaluator import *


class MetricsGroupAggregator(object):

    def __init__(self, evaluators=None,
                 class_field=None,
                 predictions_field=None,
                 group_field=None
                 ):
        self._evaluators = evaluators
        self._group_field = group_field
        self._class_field = class_field
        self._predictions_field = predictions_field

    def __call__(self, infilename):

        metrics = dict((ev.NAME, 0) for ev in self._evaluators)
        examples_count = 0
        with open(infilename) as infile:
            for group_key, examples_batch in csv_file_group_iter(infile,
                                                                 group_field=self._group_field):

                examples_count += len(examples_batch)
                for evaluator in self._evaluators:
                    metrics[evaluator.NAME] += evaluator(examples_batch)

        for name, value in metrics.iteritems():
            metrics["avg_%s" % evaluator.NAME] = metrics[name] / examples_count

        return metrics


def compute_metrics(infilename, config):

    evaluators = [
        LogLossEvaluator(
            config["class_field"],
            config["predictions_field"],
            group_field=config.get("group_field", None)
        ),
        MAPEvaluator(
            config["class_field"],
            config["predictions_field"],
            group_field=config.get("group_field", None)
        )
    ]

    aggregator = MetricsGroupAggregator(
        evaluators=evaluators,
        group_field=config["group_field"]
    )

    metrics = aggregator(infilename)
    return metrics


