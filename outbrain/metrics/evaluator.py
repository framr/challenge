from math import log


__all__ = []
def export(func):
    __all__.append(func.__name__)
    return func


class MetricEvaluator(object):
    def __init__(self):
        pass
    def __call__(self, examples):
        pass


@export
class LogLossEvaluator(MetricEvaluator):
    """
    labels should be in {0, 1}
    """
    NAME = "logloss"
    GROUP_METRICS = False

    def __init__(self, class_field, predictions_field, group_field=None):
        self._group_field = group_field
        self._class_field = class_field
        self._predictions_field = predictions_field
        self._total_examples = 0

    def __call__(self, examples):

        loss = 0
        self._total_examples += len(examples)

        for example in examples:
            label = int(getattr(example, self._class_field))
            pred = float(getattr(example, self._predictions_field))

            if label == 0:
                loss += log(1.0 - pred)
            elif label == 1:
                loss += log(pred)
            else:
                raise ValueError("Class labels should be 0 or 1, while we've got %s" % label)

        return loss


@export
class MAPEvaluator(MetricEvaluator):
    """
        labels should be in {0, 1}
        """

    NAME = "map"
    GROUP_METRICS = True

    def __init__(self, class_field, predictions_field, group_field=None,
                 sort_by_prediction=True):
        self._group_field = group_field
        self._class_field = class_field
        self._predictions_field = predictions_field
        self._sort_by_prediction = sort_by_prediction

    def __call__(self, examples):

        loss = 0
        if self._sort_by_prediction:
            sorted_examples = sorted(examples,
                                     key=lambda e: float(getattr(e,self._predictions_field)),
                                     reverse=True
                                     )

        else:
            sorted_examples = list(examples)

        result = 0
        cumulative_clicks = 0
        for i, example in enumerate(sorted_examples):
            label = int(getattr(example, self._class_field))
            cumulative_clicks += label
            #pred = float(getattr(example, self._predictions_field))

            if label == 1:
                result += float(cumulative_clicks) / (i + 1)

        if cumulative_clicks > 0:
            result /= float(cumulative_clicks)

        return result
