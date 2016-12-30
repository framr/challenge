from itertools import product


class FeatureEmitter(object):
    def __init__(self, task, separator=",", feature_separator=" ",
                 ns_join=False, ns_join_sentinel="^"):
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

        self._join_ns = ns_join
        self._ns_join_sentinel = ns_join_sentinel

        self._manual_bias = task["learn"]["vw"]["manual_bias"]


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

            namespace = [first, second]
            features = list(product(
                        getattr(example, first).split(self._feature_separator),
                        getattr(example, second).split(self._feature_separator)
            ))

            if self._join_ns:
                namespace = self._ns_join_sentinel.join(namespace)
                features = [self._ns_join_sentinel.join(pair) for pair in features]

            result.append(
                (
                    namespace,
                    features
                ))

        for first, second, third in self._cubic:
            namespace = [first, second, third]
            features = list(product(
                    product(
                        getattr(example, first).split(self._feature_separator),
                        getattr(example, second).split(self._feature_separator),
                    ),
                    getattr(example, third).split(self._feature_separator)
            ))


            if self._join_ns:
                namespace = self._ns_join_sentinel.join(namespace)
                features = [self._ns_join_sentinel.join(triplet) for triplet in features]

            result.append(
                (
                    namespace,
                    features
                )
            )

        if self._manual_bias:
            result.append(("bias", ["0"]))

        return result





