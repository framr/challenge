from itertools import product


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





