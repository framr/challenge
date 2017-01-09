from collections import defaultdict

from ..csvutil.reader import csv_file_iter


class Mapper(object):
    @property
    def add_fields(self):
        return self._add_fields

class MapReducer(object):
    @property
    def add_fields(self):
        return self._add_fields



class Join(Mapper):
    """
    Plain old MapJoin
    """
    def __init__(self,
                 join_file=None,
                 join_key=None,
                 fields=None
                 ):
        self._join_file = join_file
        self._join_key = join_key
        self._fields = fields
        self._data = self._read_join_file(join_file)
        self._add_fields = fields

    @property
    def add_fields(self):
        return self._add_fields

    def _get_key(self, example):
        return ",".join([getattr(example, k) for k in self._join_key])

    def _read_join_file(self, filename):
        data = defaultdict(dict)
        with open(filename) as infile:
            for example in csv_file_iter(infile):
                key = self._get_key(example)
                for field in self._fields:
                    data[field][key] = data[field].get(key, []) + [getattr(example, field)]

        return data

    def __call__(self, examples):
        for example in examples:
            for field in self._add_fields:
                key = self._get_key(example)
                value = " ".join(self._data[field].get(key, []))
                setattr(example, field, value)


class ProcessGeoData(Mapper):
    """
    Mapper parsing geo data
    """
    def __init__(self, field="geo_location"):
        self._field = field
        self._add_fields = ["geo_country", "geo_state", "geo_dma"]
    def __call__(self, examples):

        for example in examples:
            geo_data = getattr(example, self._field).split(">")
            country, state, dma = '', '', ''
            if geo_data:
                country = geo_data[0]
            if len(geo_data) >= 2:
                state = geo_data[1]
            if len(geo_data) >= 3:
                dma = geo_data[2]

            setattr(example, "geo_country", country)
            setattr(example, "geo_state", state)
            setattr(example, "geo_dma", dma)

class ProcessTimestamp(Mapper):
    pass


class CountAdsInBlock(MapReducer):
    """
    This is a pure reducer, i.e. we have to guarantee
    that all examples with one key are in a batch
    """
    def __init__(self, target="ads_count"):
        self._target = target
        self._add_fields = [target]

    def __call__(self, examples_group):
        ads_count = len(examples_group)
        for example in examples_group:
            setattr(example, self._target, ads_count)
