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

        if self._cubic:
            raise NotImplementedError

        self._separator = separator
        self._feature_separator = feature_separator

        if not ns_join:
            raise NotImplementedError
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

        cdef list result = []
        for ns in self._namespaces:
            result.append(
                (
                    ns,
                    getattr(example, ns).split()
                )
            )

        cdef list features
        cdef list first_features
        cdef list second_features
        for first, second in self._quadratic:

            #first_features = getattr(example, first).split(self._feature_separator)
            #second_features = getattr(example, second).split(self._feature_separator)

            features = [self._ns_join_sentinel.join((f, s))
                        for f in getattr(example, first).split()
                        for s in getattr(example, second).split()]
            #features = list(product(first_features, second_features))

            namespace = self._ns_join_sentinel.join((first, second))
            #features = [self._ns_join_sentinel.join(pair) for pair in features]

            result.append(
                (
                    namespace,
                    features
                ))


        if self._manual_bias:
            result.append(("bias", ["0"]))

        return result





